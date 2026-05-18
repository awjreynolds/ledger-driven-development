#!/usr/bin/env python3
"""Generate a reviewable skill-package skeleton from a GAPS process spec."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = Path("gaps") / "generated"


class GenerateError(Exception):
    pass


def load_yaml(path: Path) -> Any:
    result = subprocess.run(
        [
            "ruby",
            "-ryaml",
            "-rjson",
            "-e",
            "puts JSON.generate(YAML.load_file(ARGV[0]))",
            str(path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "YAML parser failed"
        raise GenerateError(f"{path}: {message}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise GenerateError(f"{path}: YAML parser returned invalid JSON: {error}") from error


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized or "process"


def safe_process_dir(process_id: str) -> str:
    if "/" in process_id or "\\" in process_id or ".." in process_id:
        raise GenerateError(
            f"process.id {process_id!r} must not contain path separators or parent traversal"
        )
    return slug(process_id)


def ensure_under(path: Path, parent: Path, label: str) -> Path:
    resolved_path = path.resolve()
    resolved_parent = parent.resolve()
    try:
        resolved_path.relative_to(resolved_parent)
    except ValueError as error:
        raise GenerateError(f"{label} escapes expected output root: {path}") from error
    return path


def display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT.resolve()))
    except ValueError:
        return str(resolved)


def command_namespace(process_id: str) -> str:
    return slug(process_id.replace("_process", "").replace("_", "-")).split("-", 1)[0]


def lane_command(namespace: str, lane_name: str) -> str:
    return f"/{namespace}:{slug(lane_name)}"


def skill_name(process_id: str, lane_name: str) -> str:
    return f"{slug(process_id)}-{slug(lane_name)}"


def review_base(output_root: Path, process_id: str) -> Path:
    generated_root = output_root / GENERATED_DIR
    return ensure_under(generated_root / safe_process_dir(process_id), generated_root, "generated output")


def render_skill(process: dict[str, Any], lane_name: str, lane: dict[str, Any], command: str) -> str:
    process_name = process["process"]["name"]
    lane_title = lane_name.replace("_", " ").title()
    gates = lane.get("gates", [])
    gate_lines = "\n".join(
        f"- `{gate.get('id')}` ({gate.get('gateType')}): {gate.get('approvalCondition')}"
        for gate in gates
        if isinstance(gate, dict)
    )
    evidence_input = "\n".join(f"- {item}" for item in lane.get("evidence", {}).get("input", []))
    evidence_completion = "\n".join(
        f"- {item}" for item in lane.get("evidence", {}).get("completion", [])
    )
    return f"""---
name: {skill_name(process['process']['id'], lane_name)}
description: Use when the user says {command}, asks to work the {lane_title} lane, or needs a generated GAPS skill skeleton for {process_name}.
---

# {command}

Generated skill skeleton for the `{lane_name}` lane in `{process['process']['id']}`.

This file is generated from a GAPS process specification and must be reviewed by a human process owner before production use.

## Inputs

Run against one governed work item or case:

```text
{command} <work-id>
```

## Reads

{evidence_input or "- Process-specific input evidence from the GAPS spec"}

## Writes

{evidence_completion or "- Process-specific completion evidence from the GAPS spec"}

## Input Quality Gate

- Confirm the requested work is inside the lane purpose: {lane.get('purpose', 'not specified')}
- Confirm required input evidence is present.
- Stop when authority, scope, evidence, or approval is insufficient.

## Gates

{gate_lines or "- No gates declared in source spec."}

## Rules

- Treat the GAPS process spec as the source for lane scope, authority, gates, evidence, and known gaps.
- Do not claim regulatory compliance, certification, legal sufficiency, runtime execution, or standards export.
- Do not approve work assigned to a human role.
- Preserve explicit known gaps rather than filling them with assumptions.

## Stop Conditions

Stop without mutation when:

- required evidence is missing
- approval authority is unclear
- the requested action exceeds the lane authority boundary
- generated instructions have not been reviewed for the target organization
"""


def render_openai_yaml(process: dict[str, Any], lane_name: str, command: str) -> str:
    lane_title = lane_name.replace("_", " ").title()
    return f"""interface:
  display_name: "{process['process']['name']} {lane_title}"
  short_description: "Generated GAPS skill for {lane_title}"
  default_prompt: "Use ${skill_name(process['process']['id'], lane_name)} to run {command}."

policy:
  allow_implicit_invocation: false
"""


def render_command_md(skill: str, command: str) -> str:
    return f"""Use the `{skill}` skill to run `{command}`.

Treat `skills/{skill}/SKILL.md` as canonical. This file is only a slash-command adapter.
"""


def render_command_toml(skill: str, command: str) -> str:
    return f'''description = "Generated GAPS command adapter for {command}."
prompt = """
Run `{command}` using the `{skill}` Agent Skill.

If the `{skill}` skill is available, activate it and follow its `SKILL.md` exactly. Treat the skill as canonical; this TOML file is only a command router.

User arguments:
{{{{args}}}}
"""
'''


def render_implementation(process: dict[str, Any], namespace: str, process_path: Path) -> str:
    process_id = process["process"]["id"]
    lines = [
        'schemaVersion: "0.1"',
        f"processSpec: {display_path(process_path)}",
        f"processId: {process_id}",
        "implementationType: agent_skill_package",
        "packageManifest: agent-skills.json",
        "skillsRoot: skills",
        "commandsRoot: commands",
        "",
        "adapterManifests:",
        "  claude: .claude-plugin/plugin.json",
        "  gemini: gemini-extension.json",
        "",
        "validators:",
        "  - scripts/validate-gaps.py",
        "  - scripts/validate-gaps-implementation.py",
        "",
        "laneImplementations:",
    ]
    for lane_name, lane in process.get("lanes", {}).items():
        command = lane_command(namespace, lane_name)
        skill = skill_name(process_id, lane_name)
        lines.extend(
            [
                f"  {lane_name}:",
                "    commands:",
                f"      - {command}",
                "    skills:",
                f"      - {skill}",
                "    gates:",
            ]
        )
        for gate in lane.get("gates", []):
            if isinstance(gate, dict):
                lines.append(f"      - {gate.get('id')}")
    lines.extend(
        [
            "",
            "conformance:",
            "  status: generated_preview",
            '  claim: "Generated implementation map requires human review before adoption."',
            "  nonClaims:",
            "    - regulatory compliance",
            "    - certification",
            "    - legal sufficiency",
            "    - runtime execution",
            "    - standards export",
        ]
    )
    return "\n".join(lines) + "\n"


def render_manifest_patch(process: dict[str, Any], namespace: str) -> str:
    commands = []
    for lane_name in process.get("lanes", {}):
        command = lane_command(namespace, lane_name)
        skill = skill_name(process["process"]["id"], lane_name)
        commands.append(
            {
                "command": command,
                "skill": skill,
                "path": f"skills/{skill}",
                "purpose": f"Generated GAPS skill for the {lane_name} lane.",
            }
        )
    return json.dumps({"commands": commands}, indent=2) + "\n"


def render_checklist(process: dict[str, Any], namespace: str) -> str:
    lines = [
        f"# Validation Checklist: {process['process']['name']}",
        "",
        "- [ ] Review every generated skill with the process owner.",
        "- [ ] Replace generated placeholders with organization-specific authority rules.",
        "- [ ] Confirm no generated skill claims compliance, certification, legal sufficiency, runtime execution, or standards export.",
        "- [ ] Add or review `implementation.yml` before adopting generated package files.",
        "- [ ] Run `python3 scripts/validate-gaps.py <ga-process.yml>`.",
        "- [ ] Run `python3 scripts/validate-gaps-implementation.py <implementation.yml>` after adoption.",
        "",
        "Generated lane commands:",
    ]
    for lane_name in process.get("lanes", {}):
        lines.append(f"- `{lane_command(namespace, lane_name)}`")
    return "\n".join(lines) + "\n"


def write_text(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise GenerateError(f"{path}: already exists; pass --overwrite to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def preflight_writes(artifacts: dict[Path, str], overwrite: bool) -> None:
    directory_targets = sorted([path for path in artifacts if path.is_dir()], key=str)
    if directory_targets:
        target_list = "\n".join(f"- {path}" for path in directory_targets[:10])
        if len(directory_targets) > 10:
            target_list += f"\n- ... and {len(directory_targets) - 10} more"
        raise GenerateError("generated output target is a directory:\n" f"{target_list}")

    blockers = sorted(
        {
            ancestor
            for path in artifacts
            for ancestor in [*path.parents]
            if ancestor.exists() and not ancestor.is_dir()
        },
        key=str,
    )
    if blockers:
        blocker_list = "\n".join(f"- {path}" for path in blockers[:10])
        if len(blockers) > 10:
            blocker_list += f"\n- ... and {len(blockers) - 10} more"
        raise GenerateError(
            "generated output parent path is not a directory:\n" f"{blocker_list}"
        )

    if overwrite:
        return
    collisions = [path for path in artifacts if path.exists()]
    if collisions:
        collision_list = "\n".join(f"- {path}" for path in collisions[:10])
        if len(collisions) > 10:
            collision_list += f"\n- ... and {len(collisions) - 10} more"
        raise GenerateError(
            "generated output would replace existing files; pass --overwrite to replace them:\n"
            f"{collision_list}"
        )


def generate(process_path: Path, output_root: Path, adopt: bool, overwrite: bool) -> tuple[Path, list[Path]]:
    process = load_yaml(process_path)
    if not isinstance(process, dict) or not isinstance(process.get("process"), dict):
        raise GenerateError(f"{process_path}: missing process object")
    process_id = process["process"].get("id")
    if not isinstance(process_id, str) or not process_id:
        raise GenerateError(f"{process_path}: process.id is required")
    namespace = command_namespace(process_id)
    generated_base = review_base(output_root, process_id)
    package_base = output_root if adopt else generated_base
    written: list[Path] = []

    if not adopt and generated_base.exists():
        shutil.rmtree(generated_base)

    artifacts: dict[Path, str] = {}
    for lane_name, lane in process.get("lanes", {}).items():
        if not isinstance(lane, dict):
            continue
        command = lane_command(namespace, lane_name)
        skill = skill_name(process_id, lane_name)
        skill_root = package_base / "skills" / skill
        command_root = package_base / "commands" / namespace
        artifacts.update(
            {
                skill_root / "SKILL.md": render_skill(process, lane_name, lane, command),
                skill_root / "agents" / "openai.yaml": render_openai_yaml(
                    process, lane_name, command
                ),
                command_root / f"{slug(lane_name)}.md": render_command_md(skill, command),
                command_root / f"{slug(lane_name)}.toml": render_command_toml(skill, command),
            }
        )

    artifacts.update({
        generated_base / "README.generated.md": render_generated_readme(process, adopt),
        generated_base / "implementation.yml": render_implementation(process, namespace, process_path),
        generated_base / "agent-skills.patch.json": render_manifest_patch(process, namespace),
        generated_base / "validation-checklist.md": render_checklist(process, namespace),
    })

    preflight_writes(artifacts, overwrite)
    for path, content in artifacts.items():
        write_text(path, content, overwrite)
        written.append(path)
    return generated_base, written


def render_generated_readme(process: dict[str, Any], adopt: bool) -> str:
    mode = "adopted package output" if adopt else "dry-run preview"
    return f"""# Generated GAPS Skill Package: {process['process']['name']}

Mode: {mode}

This output was generated from a GAPS process specification. It is a starting point for human review, not a production-ready package.

Non-claims:

- no regulatory compliance
- no certification
- no legal sufficiency
- no runtime execution guarantee
- no BPMN/CMMN/DMN/OSCAL export
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("process", type=Path, help="Path to ga-process.yml")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT,
        help="Root directory for generated output. Defaults to repository root.",
    )
    parser.add_argument("--write", action="store_true", help="Allow writing adopted package output")
    parser.add_argument(
        "--adopt-output",
        action="store_true",
        help="Write directly under package roots instead of gaps/generated/<process-id>",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow adopted output to replace existing generated files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.adopt_output and not args.write:
        print("--adopt-output requires --write", file=sys.stderr)
        return 2
    if args.write and not args.adopt_output:
        print("--write is only valid with --adopt-output", file=sys.stderr)
        return 2
    if args.overwrite and not args.adopt_output:
        print("--overwrite is only valid with --adopt-output", file=sys.stderr)
        return 2

    process_path = args.process if args.process.is_absolute() else ROOT / args.process
    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    try:
        base, written = generate(process_path, output_root, args.adopt_output, args.overwrite)
    except GenerateError as error:
        print(f"GAPS generation failed: {error}", file=sys.stderr)
        return 1

    mode = "adopted" if args.adopt_output else "preview"
    print(f"GAPS skill package generation completed ({mode}, {len(written)} files)")
    print(f"Output root: {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
