#!/usr/bin/env python3
"""Generate a reviewable skill-package skeleton from a GAPS process spec."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
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


@dataclass
class GeneratedSkill:
    name: str
    commands: list[str] = field(default_factory=list)
    lanes: list[str] = field(default_factory=list)
    lane_purposes: list[str] = field(default_factory=list)
    control_reasons: list[str] = field(default_factory=list)
    reads: list[str] = field(default_factory=list)
    writes: list[str] = field(default_factory=list)
    gates: list[dict[str, Any]] = field(default_factory=list)
    authority_blocks: list[dict[str, Any]] = field(default_factory=list)
    required_sections: list[str] = field(default_factory=list)
    required_phrases: list[str] = field(default_factory=list)


@dataclass
class GeneratedPackage:
    process: dict[str, Any]
    namespace: str
    skills: dict[str, GeneratedSkill]
    command_to_skill: dict[str, str]
    implementation: dict[str, Any] | None = None
    implementation_path: Path | None = None


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


def safe_path_segment(value: str, label: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value):
        raise GenerateError(f"{label} {value!r} must be a single safe path segment")
    return value


def safe_command_parts(command: str) -> tuple[str, str]:
    if not command.startswith("/") or command.count(":") != 1:
        raise GenerateError(f"command name {command!r} must use /namespace:name format")
    namespace, name = command[1:].split(":", 1)
    return (
        safe_path_segment(namespace, "command namespace"),
        safe_path_segment(name, "command name"),
    )


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


def unique_append(items: list[Any], item: Any) -> None:
    if item not in items:
        items.append(item)


def extend_unique(items: list[Any], additions: list[Any]) -> None:
    for item in additions:
        unique_append(items, item)


def command_leaf(command: str) -> str:
    return safe_command_parts(command)[1]


def command_namespace(process_id: str) -> str:
    return slug(process_id.replace("_process", "").replace("_", "-")).split("-", 1)[0]


def lane_command(namespace: str, lane_name: str) -> str:
    return f"/{namespace}:{slug(lane_name)}"


def skill_name(process_id: str, lane_name: str) -> str:
    return f"{slug(process_id)}-{slug(lane_name)}"


def adjacent_implementation_path(process_path: Path) -> Path | None:
    candidate = process_path.parent / "implementation.yml"
    return candidate if candidate.is_file() else None


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


def render_generated_skill(process: dict[str, Any], skill: GeneratedSkill) -> str:
    process_name = process["process"]["name"]
    command_list = ", ".join(f"`{command}`" for command in skill.commands)
    primary_command = skill.commands[0] if skill.commands else f"/{skill.name}"
    reads = "\n".join(f"- {item}" for item in skill.reads)
    writes = "\n".join(f"- {item}" for item in skill.writes)
    lane_lines = "\n".join(
        f"- `{lane}`: {purpose}" for lane, purpose in zip(skill.lanes, skill.lane_purposes)
    )
    control_lines = "\n".join(f"- {reason}" for reason in skill.control_reasons)
    gate_lines = "\n".join(
        f"- `{gate.get('id')}` ({gate.get('gateType')}): {gate.get('approvalCondition')}"
        for gate in skill.gates
    )
    authority_lines: list[str] = []
    for authority in skill.authority_blocks:
        plane = authority.get("plane")
        autonomy = authority.get("autonomyTier")
        risk = authority.get("riskTier")
        authority_lines.append(f"- plane: `{plane}`, autonomy tier: `{autonomy}`, risk tier: `{risk}`")
        for item in authority.get("allowed", []):
            authority_lines.append(f"  - allowed: {item}")
        for item in authority.get("prohibited", []):
            authority_lines.append(f"  - prohibited: {item}")
    required_phrase_lines = "\n".join(f"- {phrase}" for phrase in skill.required_phrases)
    extra_sections = []
    standard_sections = {"Input Quality Gate", "Rules", "Stop Conditions"}
    for section in skill.required_sections:
        if section in standard_sections:
            continue
        if section == "Built-in TDD Loop":
            extra_sections.append(
                """## Built-in TDD Loop

For each approved behavior:

1. Identify the next acceptance criterion or verification point.
2. Write the smallest focused test that proves the behavior is missing.
3. Run the focused test and confirm it fails for the expected reason.
4. Implement the smallest change that makes the test pass.
5. Run the focused test and confirm it passes.
6. Update documentation when required or record why it is not needed.
7. Rerun the relevant broader check before moving on.
"""
            )
        else:
            extra_sections.append(
                f"""## {section}

- This section is required by the GAPS implementation map.
- Apply the command authority, evidence, gates, and stop conditions in this generated skill.
"""
            )
    extra_section_text = "\n".join(extra_sections)
    return f"""---
name: {skill.name}
description: Use when the user says {command_list}, asks to run generated GAPS command-level skill `{skill.name}`, or needs a generated skill skeleton for {process_name}.
---

# {primary_command}

Generated command-level skill skeleton for `{skill.name}` in `{process['process']['id']}`.

This file is generated from a GAPS process specification and implementation map. It must be reviewed by a human process owner before production use.

## Inputs

Run against one governed work item or case:

```text
{primary_command} <work-id>
```

Mapped commands:

{chr(10).join(f"- `{command}`" for command in skill.commands)}

## Reads

{reads or "- Process-specific input evidence from the GAPS spec"}

## Writes

{writes or "- Process-specific completion evidence from the GAPS spec"}

## Input Quality Gate

- Confirm the requested work is inside the mapped GAPS lane or control-plane action.
- Confirm required input evidence is present.
- Stop when authority, scope, evidence, or approval is insufficient.
- Repo-local ledger is canonical.
- External mutations require human confirmation.

## Lane Scope

{lane_lines or "- No data-plane lane mapping declared."}

## Control Plane Scope

{control_lines or "- No control-plane action mapping declared."}

## Authority

{chr(10).join(authority_lines) or "- No authority block declared in source spec."}

## Gates

{gate_lines or "- No gates declared in source spec."}

{extra_section_text}
## Required Implementation Map Phrases

{required_phrase_lines or "- No extra required phrases declared."}

## Rules

- Treat the GAPS process spec and implementation map as the source for command scope, authority, gates, evidence, and known gaps.
- Repo-local ledger is canonical.
- External mutations require human confirmation.
- Do not claim regulatory compliance, certification, legal sufficiency, runtime execution, or standards export.
- Do not approve work assigned to a human role.
- Preserve explicit known gaps rather than filling them with assumptions.

## Stop Conditions

Stop without mutation when:

- required evidence is missing
- approval authority is unclear
- the requested action exceeds the command authority boundary
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


def render_generated_openai_yaml(process: dict[str, Any], skill: GeneratedSkill) -> str:
    commands = ", ".join(skill.commands)
    return f"""interface:
  display_name: "{process['process']['name']} {skill.name}"
  short_description: "Generated GAPS command-level skill for {commands}"
  default_prompt: "Use ${skill.name} to run {skill.commands[0] if skill.commands else skill.name}."

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


def yaml_scalar(value: Any) -> str:
    return json.dumps(str(value))


def yaml_lines(value: Any, indent: int = 0) -> list[str]:
    prefix = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, child in value.items():
            if isinstance(child, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(yaml_lines(child, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {yaml_scalar(child)}")
        return lines
    if isinstance(value, list):
        lines = []
        for child in value:
            if isinstance(child, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(yaml_lines(child, indent + 2))
            else:
                lines.append(f"{prefix}- {yaml_scalar(child)}")
        return lines
    return [f"{prefix}{yaml_scalar(value)}"]


def render_yaml(value: dict[str, Any]) -> str:
    return "\n".join(yaml_lines(value)) + "\n"


def generated_implementation_map(
    package: GeneratedPackage,
    process_path: Path,
    generated_base: Path,
    package_base: Path,
    adopt: bool,
) -> dict[str, Any]:
    process_id = package.process["process"]["id"]
    if package.implementation is None:
        return {}

    implementation = package.implementation
    if adopt:
        package_manifest = "agent-skills.json"
        skills_root = "skills"
        commands_root = "commands"
        claude_manifest = ".claude-plugin/plugin.json"
        gemini_manifest = "gemini-extension.json"
    else:
        package_manifest = str(generated_base / "agent-skills.json")
        skills_root = str(package_base / "skills")
        commands_root = str(package_base / "commands")
        claude_manifest = str(generated_base / ".claude-plugin" / "plugin.json")
        gemini_manifest = str(generated_base / "gemini-extension.json")

    result: dict[str, Any] = {
        "schemaVersion": str(implementation.get("schemaVersion", "0.1")),
        "processSpec": display_path(process_path),
        "processId": process_id,
        "implementationType": implementation.get("implementationType", "agent_skill_package"),
        "packageManifest": package_manifest,
        "skillsRoot": skills_root,
        "commandsRoot": commands_root,
        "adapterManifests": {
            "claude": claude_manifest,
            "gemini": gemini_manifest,
        },
        "validators": implementation.get(
            "validators",
            ["scripts/validate-gaps.py", "scripts/validate-gaps-implementation.py"],
        ),
    }
    for optional in ["globalSkillContract", "laneImplementations", "controlPlaneImplementations"]:
        if optional in implementation:
            result[optional] = implementation[optional]
    result["conformance"] = {
        "status": "generated_preview",
        "claim": "Generated implementation map requires human review before adoption.",
        "nonClaims": [
            "regulatory compliance",
            "certification",
            "legal sufficiency",
            "runtime execution",
            "standards export",
        ],
    }
    return result


def manifest_commands_for_package(package: GeneratedPackage) -> list[dict[str, str]]:
    commands = []
    for command, skill in sorted(package.command_to_skill.items()):
        commands.append(
            {
                "command": command,
                "skill": skill,
                "path": f"skills/{skill}",
                "purpose": f"Generated GAPS skill for {command}.",
            }
        )
    return commands


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


def render_full_agent_manifest(package: GeneratedPackage) -> str:
    data = {
        "schemaVersion": "1.0",
        "name": package.process["process"]["id"],
        "displayName": package.process["process"]["name"],
        "version": "0.1.0-generated",
        "description": "Generated GAPS command-level skill package preview.",
        "canonicalSkillRoot": "skills",
        "commands": manifest_commands_for_package(package),
    }
    return json.dumps(data, indent=2) + "\n"


def render_claude_manifest(package: GeneratedPackage) -> str:
    commands = []
    for command in sorted(package.command_to_skill):
        namespace, name = safe_command_parts(command)
        commands.append(f"./commands/{namespace}/{name}.md")
    data = {
        "name": package.process["process"]["id"],
        "version": "0.1.0-generated",
        "description": "Generated GAPS command-level skill package preview.",
        "commands": commands,
    }
    return json.dumps(data, indent=2) + "\n"


def render_gemini_manifest(package: GeneratedPackage) -> str:
    data = {
        "name": package.process["process"]["id"],
        "version": "0.1.0-generated",
        "contextFileName": "GEMINI.md",
        "commands": sorted(package.command_to_skill),
    }
    return json.dumps(data, indent=2) + "\n"


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


def render_package_checklist(package: GeneratedPackage) -> str:
    lines = [
        f"# Validation Checklist: {package.process['process']['name']}",
        "",
        "- [ ] Review every generated command-level skill with the process owner.",
        "- [ ] Confirm generated skills preserve the implementation-map required sections and phrases.",
        "- [ ] Confirm no generated skill claims compliance, certification, legal sufficiency, runtime execution, or standards export.",
        "- [ ] Run `python3 scripts/validate-gaps.py <ga-process.yml>`.",
        "- [ ] Run `python3 scripts/validate-gaps-implementation.py <generated implementation.yml>`.",
        "",
        "Generated commands:",
    ]
    for command in sorted(package.command_to_skill):
        lines.append(f"- `{command}` -> `{package.command_to_skill[command]}`")
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


def lane_package(process: dict[str, Any], namespace: str) -> GeneratedPackage:
    command_to_skill: dict[str, str] = {}
    skills: dict[str, GeneratedSkill] = {}
    process_id = process["process"]["id"]
    for lane_name, lane in process.get("lanes", {}).items():
        if not isinstance(lane, dict):
            continue
        command = lane_command(namespace, lane_name)
        skill = skill_name(process_id, lane_name)
        command_to_skill[command] = skill
        skills[skill] = GeneratedSkill(
            name=skill,
            commands=[command],
            lanes=[lane_name],
            lane_purposes=[str(lane.get("purpose", "not specified"))],
            reads=[item for item in lane.get("evidence", {}).get("input", []) if isinstance(item, str)],
            writes=[
                item for item in lane.get("evidence", {}).get("completion", []) if isinstance(item, str)
            ],
            gates=[gate for gate in lane.get("gates", []) if isinstance(gate, dict)],
            authority_blocks=[lane.get("authority", {})]
            if isinstance(lane.get("authority"), dict)
            else [],
            required_sections=["Input Quality Gate", "Rules", "Stop Conditions"],
        )
    return GeneratedPackage(process=process, namespace=namespace, skills=skills, command_to_skill=command_to_skill)


def implementation_package(
    process: dict[str, Any],
    namespace: str,
    implementation: dict[str, Any],
    implementation_path: Path,
) -> GeneratedPackage:
    skills: dict[str, GeneratedSkill] = {}
    command_to_skill: dict[str, str] = {}
    lanes = process.get("lanes", {})
    global_contract = implementation.get("globalSkillContract", {})
    global_sections = []
    global_phrases = []
    if isinstance(global_contract, dict):
        global_sections = [item for item in global_contract.get("requiredSections", []) if isinstance(item, str)]
        global_phrases = [item for item in global_contract.get("requiredPhrases", []) if isinstance(item, str)]

    lane_implementations = implementation.get("laneImplementations", {})
    if isinstance(lane_implementations, dict):
        for lane_name, lane_impl in lane_implementations.items():
            if not isinstance(lane_impl, dict):
                continue
            lane = lanes.get(lane_name, {}) if isinstance(lanes, dict) else {}
            commands = [item for item in lane_impl.get("commands", []) if isinstance(item, str)]
            mapped_skills = [item for item in lane_impl.get("skills", []) if isinstance(item, str)]
            for command in commands:
                safe_command_parts(command)
            for mapped_skill in mapped_skills:
                safe_path_segment(mapped_skill, "skill name")
            for index, command in enumerate(commands):
                skill_name_value = (
                    mapped_skills[index]
                    if index < len(mapped_skills)
                    else f"{namespace}-{slug(command_leaf(command))}"
                )
                command_to_skill[command] = skill_name_value
                skill = skills.setdefault(skill_name_value, GeneratedSkill(name=skill_name_value))
                unique_append(skill.commands, command)
                unique_append(skill.lanes, str(lane_name))
                unique_append(skill.lane_purposes, str(lane.get("purpose", "not specified")))
                evidence = lane.get("evidence", {}) if isinstance(lane, dict) else {}
                if isinstance(evidence, dict):
                    extend_unique(skill.reads, [item for item in evidence.get("input", []) if isinstance(item, str)])
                    extend_unique(
                        skill.writes,
                        [item for item in evidence.get("completion", []) if isinstance(item, str)],
                    )
                extend_unique(skill.gates, [gate for gate in lane.get("gates", []) if isinstance(gate, dict)])
                if isinstance(lane.get("authority"), dict):
                    unique_append(skill.authority_blocks, lane["authority"])
                extend_unique(skill.required_sections, global_sections)
                extend_unique(
                    skill.required_sections,
                    [item for item in lane_impl.get("requiredSkillSections", []) if isinstance(item, str)],
                )
                extend_unique(skill.required_phrases, global_phrases)
                extend_unique(
                    skill.required_phrases,
                    [item for item in lane_impl.get("authorityPhrases", []) if isinstance(item, str)],
                )
                extend_unique(
                    skill.required_phrases,
                    [item for item in lane_impl.get("evidencePhrases", []) if isinstance(item, str)],
                )

    control_plane = implementation.get("controlPlaneImplementations", [])
    if isinstance(control_plane, list):
        for action in control_plane:
            if not isinstance(action, dict):
                continue
            command = action.get("command")
            skill_name_value = action.get("skill")
            if not isinstance(command, str) or not isinstance(skill_name_value, str):
                continue
            safe_command_parts(command)
            safe_path_segment(skill_name_value, "skill name")
            command_to_skill[command] = skill_name_value
            skill = skills.setdefault(skill_name_value, GeneratedSkill(name=skill_name_value))
            unique_append(skill.commands, command)
            if isinstance(action.get("action"), str):
                unique_append(skill.control_reasons, str(action["action"]))
            if isinstance(action.get("reason"), str):
                unique_append(skill.control_reasons, str(action["reason"]))
            extend_unique(skill.required_sections, global_sections)
            extend_unique(skill.required_phrases, global_phrases)
            extend_unique(
                skill.required_phrases,
                [item for item in action.get("requiredPhrases", []) if isinstance(item, str)],
            )
            unique_append(skill.reads, "repo-local ledger state")
            unique_append(skill.writes, "governed control-plane ledger event")

    for skill in skills.values():
        extend_unique(skill.required_sections, ["Input Quality Gate", "Rules", "Stop Conditions"])

    return GeneratedPackage(
        process=process,
        namespace=namespace,
        skills=skills,
        command_to_skill=command_to_skill,
        implementation=implementation,
        implementation_path=implementation_path,
    )


def load_implementation_package(
    process: dict[str, Any],
    namespace: str,
    implementation_path: Path | None,
) -> GeneratedPackage:
    if implementation_path is None:
        return lane_package(process, namespace)
    implementation = load_yaml(implementation_path)
    if not isinstance(implementation, dict):
        raise GenerateError(f"{implementation_path}: expected implementation map object")
    return implementation_package(process, namespace, implementation, implementation_path)


def generate(
    process_path: Path,
    output_root: Path,
    adopt: bool,
    overwrite: bool,
    implementation_path: Path | None = None,
) -> tuple[Path, list[Path]]:
    process = load_yaml(process_path)
    if not isinstance(process, dict) or not isinstance(process.get("process"), dict):
        raise GenerateError(f"{process_path}: missing process object")
    process_id = process["process"].get("id")
    if not isinstance(process_id, str) or not process_id:
        raise GenerateError(f"{process_path}: process.id is required")
    namespace = command_namespace(process_id)
    package = load_implementation_package(process, namespace, implementation_path)
    generated_base = review_base(output_root, process_id)
    package_base = output_root if adopt else generated_base
    written: list[Path] = []

    if not adopt and generated_base.exists():
        shutil.rmtree(generated_base)

    artifacts: dict[Path, str] = {}
    if implementation_path is None:
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
    else:
        for skill_name_value, skill in package.skills.items():
            skill_root = package_base / "skills" / skill_name_value
            artifacts.update(
                {
                    skill_root / "SKILL.md": render_generated_skill(process, skill),
                    skill_root / "agents" / "openai.yaml": render_generated_openai_yaml(
                        process, skill
                    ),
                }
            )
        for command, skill_name_value in package.command_to_skill.items():
            namespace_value, command_value = safe_command_parts(command)
            command_root = package_base / "commands" / namespace_value
            artifacts.update(
                {
                    command_root / f"{command_value}.md": render_command_md(
                        skill_name_value, command
                    ),
                    command_root / f"{command_value}.toml": render_command_toml(
                        skill_name_value, command
                    ),
                }
            )
        artifacts.update(
            {
                generated_base / "agent-skills.json": render_full_agent_manifest(package),
                generated_base / ".claude-plugin" / "plugin.json": render_claude_manifest(package),
                generated_base / "gemini-extension.json": render_gemini_manifest(package),
            }
        )

    if implementation_path is None:
        implementation_content = render_implementation(process, namespace, process_path)
        manifest_patch_content = render_manifest_patch(process, namespace)
        checklist_content = render_checklist(process, namespace)
    else:
        implementation_content = render_yaml(
            generated_implementation_map(package, process_path, generated_base, package_base, adopt)
        )
        manifest_patch_content = json.dumps(
            {"commands": manifest_commands_for_package(package)}, indent=2
        ) + "\n"
        checklist_content = render_package_checklist(package)

    artifacts.update({
        generated_base / "README.generated.md": render_generated_readme(process, adopt),
        generated_base / "implementation.yml": implementation_content,
        generated_base / "agent-skills.patch.json": manifest_patch_content,
        generated_base / "validation-checklist.md": checklist_content,
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
    parser.add_argument(
        "--implementation-map",
        type=Path,
        help="Implementation map to use for command-level generation. Defaults to adjacent implementation.yml when present.",
    )
    parser.add_argument(
        "--no-implementation-map",
        action="store_true",
        help="Disable adjacent implementation.yml discovery and force lane-level generation.",
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
    if args.implementation_map and args.no_implementation_map:
        print("--implementation-map cannot be combined with --no-implementation-map", file=sys.stderr)
        return 2
    if args.implementation_map:
        implementation_path = (
            args.implementation_map
            if args.implementation_map.is_absolute()
            else ROOT / args.implementation_map
        )
    elif args.no_implementation_map:
        implementation_path = None
    else:
        implementation_path = adjacent_implementation_path(process_path)
    try:
        base, written = generate(
            process_path, output_root, args.adopt_output, args.overwrite, implementation_path
        )
    except GenerateError as error:
        print(f"GAPS generation failed: {error}", file=sys.stderr)
        return 1

    mode = "adopted" if args.adopt_output else "preview"
    print(f"GAPS skill package generation completed ({mode}, {len(written)} files)")
    print(f"Output root: {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
