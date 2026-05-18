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


def command_namespace(process_id: str) -> str:
    return slug(process_id.replace("_process", "").replace("_", "-")).split("-", 1)[0]


def lane_command(namespace: str, lane_name: str) -> str:
    return f"/{namespace}:{slug(lane_name)}"


def skill_name(process_id: str, lane_name: str) -> str:
    return f"{slug(process_id)}-{slug(lane_name)}"


def output_base(output_root: Path, process_id: str, adopt: bool) -> Path:
    if adopt:
        return output_root
    return output_root / "gaps" / "generated" / process_id


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


def render_implementation(process: dict[str, Any], namespace: str) -> str:
    process_id = process["process"]["id"]
    lines = [
        'schemaVersion: "0.1"',
        f"processSpec: gaps/examples/{process_id}/ga-process.yml",
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


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate(process_path: Path, output_root: Path, adopt: bool) -> list[Path]:
    process = load_yaml(process_path)
    if not isinstance(process, dict) or not isinstance(process.get("process"), dict):
        raise GenerateError(f"{process_path}: missing process object")
    process_id = process["process"].get("id")
    if not isinstance(process_id, str) or not process_id:
        raise GenerateError(f"{process_path}: process.id is required")
    namespace = command_namespace(process_id)
    base = output_base(output_root, process_id, adopt)
    written: list[Path] = []

    if not adopt and base.exists():
        shutil.rmtree(base)

    for lane_name, lane in process.get("lanes", {}).items():
        if not isinstance(lane, dict):
            continue
        command = lane_command(namespace, lane_name)
        skill = skill_name(process_id, lane_name)
        skill_root = base / "skills" / skill
        command_root = base / "commands" / namespace
        artifacts = {
            skill_root / "SKILL.md": render_skill(process, lane_name, lane, command),
            skill_root / "agents" / "openai.yaml": render_openai_yaml(process, lane_name, command),
            command_root / f"{slug(lane_name)}.md": render_command_md(skill, command),
            command_root / f"{slug(lane_name)}.toml": render_command_toml(skill, command),
        }
        for path, content in artifacts.items():
            write_text(path, content)
            written.append(path)

    top_level = {
        base / "README.generated.md": render_generated_readme(process, adopt),
        base / "implementation.yml": render_implementation(process, namespace),
        base / "agent-skills.patch.json": render_manifest_patch(process, namespace),
        base / "validation-checklist.md": render_checklist(process, namespace),
    }
    for path, content in top_level.items():
        write_text(path, content)
        written.append(path)
    return written


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
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.adopt_output and not args.write:
        print("--adopt-output requires --write", file=sys.stderr)
        return 2

    process_path = args.process if args.process.is_absolute() else ROOT / args.process
    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    try:
        written = generate(process_path, output_root, args.adopt_output)
    except GenerateError as error:
        print(f"GAPS generation failed: {error}", file=sys.stderr)
        return 1

    mode = "adopted" if args.adopt_output else "preview"
    print(f"GAPS skill package generation completed ({mode}, {len(written)} files)")
    print(f"Output root: {output_base(output_root, load_yaml(process_path)['process']['id'], args.adopt_output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
