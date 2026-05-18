#!/usr/bin/env python3
"""Run automated GADD Level 2 live-style scenarios.

Level 2 scenarios seed disposable target repositories from Level 1 fixtures and
run a pluggable command runner against the seeded repo. The initial
``fixture-next`` runner is deterministic and read-only: it exercises the Level 2
harness without requiring a specific agent CLI.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import sys
import tempfile


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SCENARIOS = ROOT / "tests" / "level2" / "scenarios"
LEVEL1_FIXTURES = ROOT / "tests" / "level1" / "fixtures"
ARTIFACTS = Path(tempfile.gettempdir()) / "gadd-level2-artifacts"

PACKAGE_PATHS = [
    "skills",
    "commands",
    "agent-skills.json",
    "GEMINI.md",
    "README.md",
    "CONTEXT.md",
    "docs/skills.md",
]
REQUIRED_OVERRIDE_PACKAGE_PATHS = {"skills", "commands", "agent-skills.json"}


class Level2Error(Exception):
    pass


def load_level1_module():
    script_path = ROOT / "scripts" / "validate-gadd-level1.py"
    spec = importlib.util.spec_from_file_location("gadd_level1", script_path)
    if not spec or not spec.loader:
        raise Level2Error(f"unable to load Level 1 validator from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LEVEL1 = load_level1_module()

from gadd_generated_contracts import command_from_text, validate_command_contract


def copy_path(source: Path, target: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def package_source(relative_path: str, package_root: Path | None) -> Path:
    if package_root is not None:
        generated_source = package_root / relative_path
        if generated_source.exists():
            return generated_source
        if relative_path in REQUIRED_OVERRIDE_PACKAGE_PATHS:
            raise Level2Error(f"generated package missing required path: {generated_source}")
    source = ROOT / relative_path
    if not source.exists():
        raise Level2Error(f"missing package path: {source}")
    return source


def seed_repo(step: dict, repo_dir: Path) -> None:
    source_scenario = step.get("source_scenario")
    fixture = step.get("fixture")
    if not source_scenario or not fixture:
        raise Level2Error("step must include source_scenario and fixture")

    fixture_dir = LEVEL1_FIXTURES / source_scenario / fixture
    if not fixture_dir.is_dir():
        raise Level2Error(f"missing Level 1 fixture: {fixture_dir}")

    shutil.copytree(fixture_dir, repo_dir, dirs_exist_ok=True)
    package_root = Path(os.environ["GADD_PACKAGE_ROOT"]) if os.environ.get("GADD_PACKAGE_ROOT") else None
    for relative_path in PACKAGE_PATHS:
        source = package_source(relative_path, package_root)
        copy_path(source, repo_dir / relative_path)


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 64), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot_files(repo_dir: Path) -> dict[str, str]:
    snapshot = {}
    for path in sorted(repo_dir.rglob("*")):
        if path.is_file():
            snapshot[str(path.relative_to(repo_dir))] = file_digest(path)
    return snapshot


def changed_files(before: dict[str, str], after: dict[str, str]) -> list[str]:
    paths = sorted(set(before) | set(after))
    return [path for path in paths if before.get(path) != after.get(path)]


def expected_text(value) -> str:
    if isinstance(value, dict) and "text" in value:
        return str(value["text"])
    return str(value)


def load_parent_and_children(repo_dir: Path, work_item: str) -> tuple[dict, list[dict]]:
    parent_path = repo_dir / "gadd" / "work-items" / work_item / "ledger.yml"
    if not parent_path.is_file():
        raise Level2Error(f"missing seeded ledger: {parent_path}")

    parent = LEVEL1.parse_yaml_subset(parent_path)
    children = []
    children_dir = parent_path.parent / "children"
    if children_dir.is_dir():
        for child_path in sorted(children_dir.glob("*/ledger.yml")):
            children.append(LEVEL1.parse_yaml_subset(child_path))
    return parent, children


def run_fixture_next(step: dict, repo_dir: Path) -> tuple[str, bool]:
    work_item = step.get("work_item")
    if not work_item:
        raise Level2Error("fixture-next step must include work_item")

    parent, children = load_parent_and_children(repo_dir, work_item)
    actual = LEVEL1.derive_next(parent, children)
    output_lines = [
        f"prompt: {step.get('prompt')}",
        f"runner_command: {step.get('runner_command')}",
        f"next_command: {actual.get('next_command')}",
        f"next_human_action: {actual.get('next_human_action')}",
    ]
    if "optional_cleanup_command" in actual:
        output_lines.append(f"optional_cleanup_command: {actual.get('optional_cleanup_command')}")
    return "\n".join(output_lines) + "\n", False


def run_step(runner: str, scenario: dict, step: dict, step_index: int, artifacts_dir: Path) -> list[str]:
    errors = []
    with tempfile.TemporaryDirectory(prefix="gadd-level2-") as temp_root:
        repo_dir = Path(temp_root) / "repo"
        repo_dir.mkdir(parents=True)
        seed_repo(step, repo_dir)

        if os.environ.get("GADD_PACKAGE_ROOT"):
            command = command_from_text(str(step.get("runner_command", "")))
            if command:
                contract_errors = validate_command_contract(repo_dir, command)
                errors.extend(
                    f"{scenario.get('id', 'scenario')} / {step.get('name')}: "
                    f"generated package contract failed: {error}"
                    for error in contract_errors
                )
                if contract_errors:
                    return errors

        before = snapshot_files(repo_dir)
        if runner == "fixture-next":
            output, external_mutation = run_fixture_next(step, repo_dir)
        else:
            raise Level2Error(f"unsupported Level 2 runner: {runner}")
        after = snapshot_files(repo_dir)

        scenario_id = scenario.get("id", "scenario")
        safe_step_name = str(step.get("name", step_index)).replace("/", "-").replace(" ", "-")
        transcript = artifacts_dir / f"{scenario_id}-{step_index:02d}-{safe_step_name}.txt"
        transcript.parent.mkdir(parents=True, exist_ok=True)
        transcript.write_text(output, encoding="utf-8")

        for raw_expected in step.get("expect_output_contains", []):
            expected = expected_text(raw_expected)
            if expected not in output:
                errors.append(
                    f"{scenario_id} / {step.get('name')}: output did not contain {expected!r}; "
                    f"see {transcript}"
                )

        expected_changed = step.get("expect_changed_files")
        actual_changed = changed_files(before, after)
        if expected_changed is not None and actual_changed != expected_changed:
            errors.append(
                f"{scenario_id} / {step.get('name')}: expected changed files "
                f"{expected_changed!r}, got {actual_changed!r}; see {transcript}"
            )

        if step.get("expect_no_external_mutation") and external_mutation:
            errors.append(f"{scenario_id} / {step.get('name')}: runner reported external mutation")

    return errors


def load_scenarios(case: str | None) -> list[tuple[Path, dict]]:
    scenario_paths = sorted(SCENARIOS.glob("*.yml"))
    if case:
        scenario_paths = [path for path in scenario_paths if path.stem == case or path.name == case]
    if not scenario_paths:
        raise Level2Error(f"no Level 2 scenarios found for case {case!r}")

    scenarios = []
    for scenario_path in scenario_paths:
        scenario = LEVEL1.parse_yaml_subset(scenario_path)
        for required in ("id", "steps"):
            if required not in scenario:
                raise Level2Error(f"{scenario_path}: missing required field {required}")
        scenarios.append((scenario_path, scenario))
    return scenarios


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runner", required=True, help="Level 2 runner adapter, currently: fixture-next")
    parser.add_argument("--case", help="Scenario file stem or name to run")
    parser.add_argument(
        "--artifacts-dir",
        type=Path,
        default=ARTIFACTS,
        help=f"Directory for transcripts and failure artifacts (default: {ARTIFACTS})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    artifacts_dir = args.artifacts_dir
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    errors = []
    try:
        scenarios = load_scenarios(args.case)
        step_count = 0
        for _scenario_path, scenario in scenarios:
            for index, step in enumerate(scenario["steps"], start=1):
                step_count += 1
                errors.extend(run_step(args.runner, scenario, step, index, artifacts_dir))
    except Level2Error as error:
        print(str(error), file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(
        f"GADD Level 2 live-style scenarios validated "
        f"({len(scenarios)} scenarios, {step_count} steps, runner={args.runner})"
    )
    print(f"Artifacts: {artifacts_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
