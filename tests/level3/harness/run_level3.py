from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys

from tests.level3.harness.agent_adapter import AdapterRegistry, AgentExecutionRequest
from tests.level3.harness.assertions import evaluate_expectations
from tests.level3.harness.github_tracker import GitHubTracker, load_github_tracker_config
from tests.level3.harness.local_tracker import LocalIssue, LocalTracker
from tests.level3.harness.sandbox import create_sandbox
from tests.level3.harness.scripted_adapter import ScriptedAgentAdapter
from scripts.gadd_generated_contracts import validate_command_contract


ROOT = Path(__file__).resolve().parents[3]
SCENARIOS = ROOT / "tests" / "level3" / "scenarios"
RUNS_DIR = ROOT / "tests" / "level3" / ".runs"


@dataclass(frozen=True)
class Config:
    adapter: str
    tracker: str
    run_id: str
    strict_adapter: bool
    strict_tracker: bool


class Level3Error(Exception):
    pass


def load_config(env: dict[str, str] | None = None) -> Config:
    values = dict(os.environ if env is None else env)
    adapter = values.get("GADD_L3_ADAPTER", "scripted")
    tracker = values.get("GADD_L3_TRACKER", "local")
    if tracker not in {"local", "github"}:
        raise ValueError("GADD_L3_TRACKER must be one of: local, github")
    run_id = values.get("GADD_L3_RUN_ID", f"gadd-l3-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}")
    return Config(
        adapter=adapter,
        tracker=tracker,
        run_id=run_id,
        strict_adapter=values.get("GADD_L3_STRICT_ADAPTER", "false").lower() == "true",
        strict_tracker=values.get("GADD_L3_STRICT_TRACKER", "false").lower() == "true",
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run GADD Level 3 agent end-to-end scenarios.")
    parser.add_argument("--adapter", choices=["scripted", "codex"], help="Agent adapter to use.")
    parser.add_argument("--tracker", choices=["local", "github"], help="Tracker mode to use.")
    parser.add_argument("--case", help="Scenario file stem or name to run.")
    parser.add_argument("--runs-dir", type=Path, default=RUNS_DIR, help="Directory for Level 3 run artifacts.")
    parser.add_argument("--strict-adapter", action="store_true", help="Fail when the requested adapter is unavailable.")
    parser.add_argument("--strict-tracker", action="store_true", help="Fail when the requested tracker is unavailable.")
    return parser.parse_args(argv)


def summarize_findings(findings: list) -> str:
    count = len(findings)
    if count == 0:
        return "0 Level 3 findings"
    if count == 1:
        return "1 Level 3 finding"
    return f"{count} Level 3 findings"


def load_level1_module():
    script_path = ROOT / "scripts" / "validate-gadd-level1.py"
    spec = importlib.util.spec_from_file_location("gadd_level1", script_path)
    if not spec or not spec.loader:
        raise Level3Error(f"unable to load Level 1 validator from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LEVEL1 = load_level1_module()


def load_scenarios(case: str | None) -> list[dict]:
    paths = sorted(SCENARIOS.glob("*.json"))
    if case:
        paths = [path for path in paths if path.stem == case or path.name == case]
    if not paths:
        raise Level3Error(f"no Level 3 scenarios found for case {case!r}")
    scenarios = []
    for path in paths:
        scenario = json.loads(path.read_text(encoding="utf-8"))
        for required in ("id", "steps"):
            if required not in scenario:
                raise Level3Error(f"{path}: missing required field {required}")
        scenarios.append(scenario)
    return scenarios


def build_registry() -> AdapterRegistry:
    registry = AdapterRegistry()
    registry.register("scripted", ScriptedAgentAdapter)
    try:
        from tests.level3.harness.codex_adapter import CodexAgentAdapter

        registry.register("codex", CodexAgentAdapter)
    except ImportError:
        pass
    return registry


def write_manifest(path: Path, manifest: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _create_scripted_issues(step: dict, tracker) -> None:
    for issue in step.get("scripted_issues", []):
        tracker.create_issue(
            LocalIssue(
                role=str(issue["role"]),
                title=str(issue["title"]),
                body=str(issue["body"]),
                labels=[str(label) for label in issue.get("labels", [])],
            )
        )


def _create_tracker(config: Config, sandbox_path: Path):
    if config.tracker == "local":
        return LocalTracker(sandbox_path), None
    github_config = load_github_tracker_config(env=None, run_id=config.run_id, strict=config.strict_tracker)
    if github_config.skip_live:
        return None, "Skipping Level 3 GitHub tracker run: set GADD_L3_GITHUB_REPO or GADD_L2_GITHUB_REPO."
    return GitHubTracker(github_config), None


def run_scenario(config: Config, scenario: dict, runs_dir: Path, adapter_name: str, tracker_mode: str) -> list[str]:
    run_root = runs_dir / config.run_id / scenario["id"]
    sandbox = create_sandbox(run_root, scenario["id"], scenario.get("seed_files", {}))
    tracker, skip_message = _create_tracker(config, sandbox.path)
    if skip_message:
        print(skip_message)
        return []
    if tracker is None:
        raise Level3Error("tracker was not initialized")
    adapter = build_registry().create(adapter_name)
    findings: list[str] = []
    step_results = []

    for index, step in enumerate(scenario["steps"], start=1):
        step_name = str(step.get("name", index)).replace("/", "-").replace(" ", "-")
        if os.environ.get("GADD_PACKAGE_ROOT"):
            contract_findings: list[str] = []
            for command in step.get("contract_commands", []):
                contract_errors = validate_command_contract(sandbox.path, str(command))
                contract_findings.extend(
                    f"{scenario['id']} / {step_name}: generated package contract failed: {error}"
                    for error in contract_errors
                )
            findings.extend(contract_findings)
            if contract_findings:
                break
        request = AgentExecutionRequest(
            run_id=config.run_id,
            scenario_id=str(scenario["id"]),
            step_name=step_name,
            sandbox_path=sandbox.path,
            prompt=str(step.get("prompt", "")),
            step=step,
            timeout_seconds=int(step.get("timeout_seconds", 120)),
            transcript_dir=run_root / "transcripts",
        )
        result = adapter.run(request)
        _create_scripted_issues(step, tracker)
        step_findings = evaluate_expectations(sandbox.path, result, step.get("expect", []), tracker)
        findings.extend(f"{scenario['id']} / {step_name}: {finding.message}" for finding in step_findings)
        step_results.append(
            {
                "name": step_name,
                "exit_status": result.exit_status,
                "transcript": str(result.transcript_path),
                "files_changed": result.files_changed,
                "findings": [finding.message for finding in step_findings],
            }
        )

    write_manifest(
        run_root / "manifest.json",
        {
            "run_id": config.run_id,
            "scenario": scenario["id"],
            "adapter": adapter_name,
            "tracker": tracker_mode,
            "steps": step_results,
            "findings": findings,
        },
    )
    return findings


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        base_config = load_config()
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    config = Config(
        adapter=args.adapter or base_config.adapter,
        tracker=args.tracker or base_config.tracker,
        run_id=base_config.run_id,
        strict_adapter=args.strict_adapter or base_config.strict_adapter,
        strict_tracker=args.strict_tracker or base_config.strict_tracker,
    )
    try:
        scenarios = load_scenarios(args.case)
        findings: list[str] = []
        for scenario in scenarios:
            findings.extend(run_scenario(config, scenario, args.runs_dir, config.adapter, config.tracker))
    except (Level3Error, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1

    for finding in findings:
        print(finding, file=sys.stderr)
    print(f"GADD Level 3 scenarios evaluated: {summarize_findings(findings)}")
    print(f"Artifacts: {args.runs_dir / config.run_id}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
