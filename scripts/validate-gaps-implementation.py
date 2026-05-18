#!/usr/bin/env python3
"""Validate GAPS implementation maps against concrete repository files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAP = ROOT / "gaps" / "examples" / "gadd" / "implementation.yml"


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ValidationError(f"{path}: unable to read JSON: {error}") from error
    except json.JSONDecodeError as error:
        raise ValidationError(f"{path}: invalid JSON: {error}") from error


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
        raise ValidationError(f"{path}: {message}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise ValidationError(f"{path}: YAML parser returned invalid JSON: {error}") from error


def load_structured(path: Path) -> Any:
    if path.suffix == ".json":
        return load_json(path)
    return load_yaml(path)


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return ROOT / path


def required_string(data: dict[str, Any], field: str, location: str, errors: list[str]) -> str | None:
    value = data.get(field)
    if not isinstance(value, str) or not value:
        errors.append(f"{location}.{field}: missing required string field")
        return None
    return value


def required_object(data: dict[str, Any], field: str, location: str, errors: list[str]) -> dict[str, Any] | None:
    value = data.get(field)
    if not isinstance(value, dict):
        errors.append(f"{location}.{field}: missing required object field")
        return None
    return value


def command_name(command: str) -> str:
    return command_parts(command)[1]


def safe_path_segment(value: str, label: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value):
        raise ValidationError(f"invalid {label} {value!r}")
    return value


def command_parts(command: str) -> tuple[str, str]:
    if not command.startswith("/") or command.count(":") != 1:
        raise ValidationError(f"invalid command name {command!r}")
    namespace, name = command[1:].split(":", 1)
    return safe_path_segment(namespace, "command namespace"), safe_path_segment(name, "command name")


def command_adapter_paths(commands_root: Path, command: str) -> tuple[Path, Path]:
    namespace, name = command_parts(command)
    return commands_root / namespace / f"{name}.md", commands_root / namespace / f"{name}.toml"


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def command_manifest_path(md_path: Path, commands_root: Path) -> str:
    package_root = commands_root.parent
    try:
        return f"./{md_path.relative_to(package_root).as_posix()}"
    except ValueError:
        return f"./{display_path(md_path)}"


def file_contains(path: Path, phrase: str) -> bool:
    return phrase.lower() in path.read_text(encoding="utf-8").lower()


def combined_contains(paths: list[Path], phrase: str) -> bool:
    needle = phrase.lower()
    return any(needle in path.read_text(encoding="utf-8").lower() for path in paths)


def load_manifest_commands(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    commands = manifest.get("commands", [])
    if not isinstance(commands, list):
        return {}
    return {
        command["command"]: command
        for command in commands
        if isinstance(command, dict) and isinstance(command.get("command"), str)
    }


def validate_map(path: Path) -> list[str]:
    errors: list[str] = []
    implementation = load_structured(path)
    if not isinstance(implementation, dict):
        return [f"{path}: expected implementation map object"]

    process_spec = required_string(implementation, "processSpec", str(path), errors)
    package_manifest = required_string(implementation, "packageManifest", str(path), errors)
    skills_root_value = required_string(implementation, "skillsRoot", str(path), errors)
    commands_root_value = required_string(implementation, "commandsRoot", str(path), errors)
    adapter_manifests = required_object(implementation, "adapterManifests", str(path), errors)
    if adapter_manifests is not None:
        required_string(adapter_manifests, "claude", f"{path}.adapterManifests", errors)
        required_string(adapter_manifests, "gemini", f"{path}.adapterManifests", errors)
    if errors:
        return errors

    process_path = resolve_repo_path(process_spec or "")
    process = load_structured(process_path)
    manifest_path = resolve_repo_path(package_manifest or "")
    manifest = load_json(manifest_path)

    process_id = process.get("process", {}).get("id") if isinstance(process, dict) else None
    if implementation.get("processId") != process_id:
        errors.append(f"{path}: processId {implementation.get('processId')!r} does not match {process_id!r}")

    skills_root = resolve_repo_path(skills_root_value or "")
    commands_root = resolve_repo_path(commands_root_value or "")
    manifest_commands = load_manifest_commands(manifest)
    claude_commands = load_claude_commands(adapter_manifests or {})
    gemini_commands = load_gemini_commands(adapter_manifests or {})

    lanes = process.get("lanes", {}) if isinstance(process, dict) else {}
    lane_implementations = implementation.get("laneImplementations", {})
    if not isinstance(lanes, dict) or not lanes:
        errors.append(f"{process_path}: process.lanes must be a non-empty object")
        lanes = {}
    if not isinstance(lane_implementations, dict):
        errors.append(f"{path}: laneImplementations must be an object")
        lane_implementations = {}

    for lane_name, lane in lanes.items():
        if lane_name not in lane_implementations:
            errors.append(f"{path}: laneImplementations.{lane_name} missing for process lane")
            continue
        validate_lane(
            lane_name,
            lane,
            lane_implementations[lane_name],
            skills_root,
            commands_root,
            manifest_commands,
            claude_commands,
            gemini_commands,
            errors,
        )

    for lane_name in lane_implementations:
        if lane_name not in lanes:
            errors.append(f"{path}: laneImplementations.{lane_name} has no matching process lane")

    validate_global_skill_contract(implementation, skills_root, errors)

    validate_control_plane(
        implementation,
        process,
        skills_root,
        commands_root,
        manifest_commands,
        claude_commands,
        gemini_commands,
        errors,
    )

    for validator in implementation.get("validators", []):
        validator_path = resolve_repo_path(str(validator))
        if not validator_path.is_file():
            errors.append(f"{path}: validator path missing: {validator}")

    conformance = implementation.get("conformance", {})
    if isinstance(conformance, dict):
        claim = str(conformance.get("claim", "")).lower()
        prohibited = ["is compliant", "is certified", "legally sufficient", "regulatory compliant"]
        for phrase in prohibited:
            if phrase in claim:
                errors.append(f"{path}: prohibited conformance overclaim {phrase!r}")

    return errors


def load_claude_commands(implementation: dict[str, Any]) -> set[str]:
    path = resolve_repo_path(str(implementation.get("claude", "")))
    data = load_json(path)
    commands = data.get("commands", [])
    return {str(command) for command in commands if isinstance(command, str)}


def load_gemini_commands(implementation: dict[str, Any]) -> set[str]:
    path = resolve_repo_path(str(implementation.get("gemini", "")))
    data = load_json(path)
    commands = data.get("commands", [])
    return {str(command) for command in commands if isinstance(command, str)}


def validate_lane(
    lane_name: str,
    lane: dict[str, Any],
    implementation: Any,
    skills_root: Path,
    commands_root: Path,
    manifest_commands: dict[str, dict[str, Any]],
    claude_commands: set[str],
    gemini_commands: set[str],
    errors: list[str],
) -> None:
    lane_path = f"laneImplementations.{lane_name}"
    if not isinstance(implementation, dict):
        errors.append(f"{lane_path}: must be an object")
        return

    skill_paths = validate_skill_references(lane_path, implementation, skills_root, errors)
    validate_process_command_coverage(lane_path, lane, implementation, errors)
    validate_command_references(
        lane_path,
        implementation,
        commands_root,
        manifest_commands,
        claude_commands,
        gemini_commands,
        errors,
    )
    validate_gate_references(lane_path, lane, implementation, errors)

    for section in implementation.get("requiredSkillSections", []):
        if not combined_contains(skill_paths, f"## {section}"):
            errors.append(f"{lane_path}: required section missing from mapped skills: {section}")

    for phrase in implementation.get("authorityPhrases", []):
        if not combined_contains(skill_paths, str(phrase)):
            errors.append(f"{lane_path}: authority phrase missing from mapped skills: {phrase}")

    for phrase in implementation.get("evidencePhrases", []):
        if not combined_contains(skill_paths, str(phrase)):
            errors.append(f"{lane_path}: evidence phrase missing from mapped skills: {phrase}")

    for phrase in implementation.get("behaviorPhrases", []):
        if not combined_contains(skill_paths, str(phrase)):
            errors.append(f"{lane_path}: behavior phrase missing from mapped skills: {phrase}")


def validate_skill_references(
    location: str, implementation: dict[str, Any], skills_root: Path, errors: list[str]
) -> list[Path]:
    skill_paths: list[Path] = []
    for skill in implementation.get("skills", []):
        skill_value = str(skill)
        try:
            safe_path_segment(skill_value, "skill name")
        except ValidationError as error:
            errors.append(f"{location}: {error}")
            continue
        skill_dir = skills_root / skill_value
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{location}: skill file missing for {skill}")
            continue
        skill_paths.append(skill_file)
    return skill_paths


def mapped_skill_files(implementation: dict[str, Any], skills_root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    lane_implementations = implementation.get("laneImplementations", {})
    if isinstance(lane_implementations, dict):
        for lane in lane_implementations.values():
            if isinstance(lane, dict):
                for skill in lane.get("skills", []):
                    if isinstance(skill, str):
                        files[skill] = skills_root / skill / "SKILL.md"
    control_plane = implementation.get("controlPlaneImplementations", [])
    if isinstance(control_plane, list):
        for action in control_plane:
            if isinstance(action, dict) and isinstance(action.get("skill"), str):
                files[action["skill"]] = skills_root / action["skill"] / "SKILL.md"
    return files


def validate_global_skill_contract(
    implementation: dict[str, Any], skills_root: Path, errors: list[str]
) -> None:
    contract = implementation.get("globalSkillContract", {})
    if not isinstance(contract, dict):
        return
    skill_files = mapped_skill_files(implementation, skills_root)
    for skill, skill_file in sorted(skill_files.items()):
        if not skill_file.is_file():
            continue
        for section in contract.get("requiredSections", []):
            if not file_contains(skill_file, f"## {section}"):
                errors.append(
                    f"globalSkillContract.requiredSections: {skill} missing section {section}"
                )
        for phrase in contract.get("requiredPhrases", []):
            if not file_contains(skill_file, str(phrase)):
                errors.append(
                    f"globalSkillContract.requiredPhrases: {skill} missing phrase {phrase}"
                )


def validate_command_references(
    location: str,
    implementation: dict[str, Any],
    commands_root: Path,
    manifest_commands: dict[str, dict[str, Any]],
    claude_commands: set[str],
    gemini_commands: set[str],
    errors: list[str],
) -> None:
    for command in implementation.get("commands", []):
        command = str(command)
        try:
            md_path, toml_path = command_adapter_paths(commands_root, command)
        except ValidationError as error:
            errors.append(f"{location}: {error}")
            continue
        if command not in manifest_commands:
            errors.append(f"{location}: command missing from agent-skills.json: {command}")
        if not md_path.is_file():
            errors.append(f"{location}: command markdown adapter missing: {display_path(md_path)}")
        if not toml_path.is_file():
            errors.append(f"{location}: command TOML adapter missing: {display_path(toml_path)}")
        claude_path = command_manifest_path(md_path, commands_root)
        if claude_path not in claude_commands:
            errors.append(f"{location}: command missing from Claude plugin: {claude_path}")
        if command not in gemini_commands:
            errors.append(f"{location}: command missing from Gemini extension: {command}")


def validate_gate_references(
    location: str, lane: dict[str, Any], implementation: dict[str, Any], errors: list[str]
) -> None:
    gates = lane.get("gates", [])
    gate_ids = {gate.get("id") for gate in gates if isinstance(gate, dict)}
    for gate in implementation.get("gates", []):
        if gate not in gate_ids:
            errors.append(f"{location}: gate {gate} missing from process lane")


def validate_process_command_coverage(
    location: str, lane: dict[str, Any], implementation: dict[str, Any], errors: list[str]
) -> None:
    process_commands = {command for command in lane.get("skills", []) if isinstance(command, str)}
    implementation_commands = {
        command for command in implementation.get("commands", []) if isinstance(command, str)
    }
    for command in sorted(process_commands - implementation_commands):
        errors.append(f"{location}: process command {command} missing from implementation commands")
    for command in sorted(implementation_commands - process_commands):
        errors.append(f"{location}: implementation command {command} not declared in process lane skills")


def validate_control_plane(
    implementation: dict[str, Any],
    process: dict[str, Any],
    skills_root: Path,
    commands_root: Path,
    manifest_commands: dict[str, dict[str, Any]],
    claude_commands: set[str],
    gemini_commands: set[str],
    errors: list[str],
) -> None:
    process_actions = {
        action.get("command")
        for action in process.get("controlPlaneActions", [])
        if isinstance(action, dict)
    }
    implementation_actions = {
        action.get("command")
        for action in implementation.get("controlPlaneImplementations", [])
        if isinstance(action, dict)
    }
    for command in sorted(process_actions - implementation_actions):
        errors.append(f"controlPlaneImplementations: process command {command} missing from controlPlaneImplementations")
    for command in sorted(implementation_actions - process_actions):
        errors.append(f"controlPlaneImplementations: implementation command {command} not declared in process controlPlaneActions")

    for index, action in enumerate(implementation.get("controlPlaneImplementations", [])):
        location = f"controlPlaneImplementations.{index}"
        if not isinstance(action, dict):
            errors.append(f"{location}: must be an object")
            continue
        command = str(action.get("command", ""))
        if action.get("action") not in process_actions:
            errors.append(f"{location}: action {action.get('action')} missing from process controlPlaneActions")
        validate_skill_references(location, {"skills": [action.get("skill")]}, skills_root, errors)
        validate_command_references(
            location,
            {"commands": [command]},
            commands_root,
            manifest_commands,
            claude_commands,
            gemini_commands,
            errors,
        )
        skill_file = skills_root / str(action.get("skill")) / "SKILL.md"
        if skill_file.is_file():
            for phrase in action.get("requiredPhrases", []):
                if not file_contains(skill_file, str(phrase)):
                    errors.append(f"{location}: required phrase missing from {action.get('skill')}: {phrase}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Implementation maps to validate")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    paths = args.paths or [DEFAULT_MAP]

    all_errors: list[str] = []
    for path in paths:
        map_path = path if path.is_absolute() else ROOT / path
        try:
            all_errors.extend(validate_map(map_path))
        except ValidationError as error:
            all_errors.append(str(error))

    if all_errors:
        print("GAPS implementation validation failed:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"GAPS implementation validation passed ({len(paths)} implementation maps)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
