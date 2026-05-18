"""Contract checks for generated GADD package command surfaces."""

from __future__ import annotations

import json
from pathlib import Path
import re


COMMAND_PATTERN = re.compile(r"/[A-Za-z0-9][A-Za-z0-9_-]*:[A-Za-z0-9][A-Za-z0-9_-]*")


def command_from_text(value: str) -> str | None:
    match = COMMAND_PATTERN.search(value)
    return match.group(0) if match else None


def command_parts(command: str) -> tuple[str, str]:
    if not COMMAND_PATTERN.fullmatch(command):
        raise ValueError(f"invalid command name: {command}")
    namespace, name = command[1:].split(":", 1)
    return namespace, name


def _load_json(path: Path) -> tuple[object | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except OSError as error:
        return None, [f"{path}: unable to read JSON: {error}"]
    except json.JSONDecodeError as error:
        return None, [f"{path}: invalid JSON: {error}"]


def _manifest_command(package_root: Path, command: str) -> tuple[dict | None, list[str]]:
    manifest_path = package_root / "agent-skills.json"
    manifest, errors = _load_json(manifest_path)
    if errors:
        return None, errors
    commands = manifest.get("commands") if isinstance(manifest, dict) else None
    if not isinstance(commands, list):
        return None, [f"{manifest_path}: commands must be a list"]
    for item in commands:
        if isinstance(item, dict) and item.get("command") == command:
            return item, []
    return None, [f"{manifest_path}: command {command} missing from manifest"]


def _section_text(content: str, heading: str) -> str | None:
    lines = content.splitlines()
    heading_line = f"## {heading}".strip()
    start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == heading_line:
            start = index + 1
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end])


def _contains(value: str, phrase: str) -> bool:
    return phrase.lower() in value.lower()


def _frontmatter(content: str) -> dict[str, str] | None:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return None


def validate_command_contract(
    package_root: Path,
    command: str,
    required_sections: list[str] | None = None,
    required_section_phrases: dict[str, list[str]] | None = None,
) -> list[str]:
    errors: list[str] = []
    try:
        namespace, command_name = command_parts(command)
    except ValueError as error:
        return [str(error)]

    manifest_entry, manifest_errors = _manifest_command(package_root, command)
    errors.extend(manifest_errors)
    if manifest_entry is None:
        return errors

    skill_name = manifest_entry.get("skill")
    skill_path_value = manifest_entry.get("path")
    if not isinstance(skill_name, str) or not skill_name:
        errors.append(f"{command}: manifest entry missing skill")
        skill_name = ""
    if not isinstance(skill_path_value, str) or not skill_path_value:
        errors.append(f"{command}: manifest entry missing path")
        skill_path_value = f"skills/{skill_name}"

    adapter_path = package_root / "commands" / namespace / f"{command_name}.md"
    if not adapter_path.is_file():
        errors.append(f"{command}: command adapter missing: {adapter_path}")
    else:
        adapter_content = adapter_path.read_text(encoding="utf-8")
        if skill_name and not _contains(adapter_content, skill_name):
            errors.append(f"{command}: command adapter does not reference skill {skill_name}")
        if not _contains(adapter_content, command):
            errors.append(f"{command}: command adapter does not reference command")
        if skill_path_value and not _contains(adapter_content, f"{skill_path_value}/SKILL.md"):
            errors.append(f"{command}: command adapter does not reference canonical skill file")

    skill_file = package_root / skill_path_value / "SKILL.md"
    if not skill_file.is_file():
        errors.append(f"{command}: generated skill missing: {skill_file}")
        return errors

    skill_content = skill_file.read_text(encoding="utf-8")
    frontmatter = _frontmatter(skill_content)
    if frontmatter is None:
        errors.append(f"{command}: generated skill frontmatter missing")
    elif skill_name and frontmatter.get("name") != skill_name:
        errors.append(f"{command}: generated skill frontmatter missing name {skill_name}")
    if not _contains(skill_content, f"# {command}"):
        errors.append(f"{command}: generated skill heading missing")
    if not _contains(skill_content, f"- `{command}`"):
        errors.append(f"{command}: generated skill mapped command missing")

    for section in required_sections or []:
        if _section_text(skill_content, section) is None:
            errors.append(f"{command}: generated skill missing section {section}")

    for section, phrases in (required_section_phrases or {}).items():
        section_content = _section_text(skill_content, section)
        if section_content is None:
            errors.append(f"{command}: generated skill missing section {section}")
            continue
        for phrase in phrases:
            if not _contains(section_content, phrase):
                errors.append(f"{command}: section {section} missing phrase {phrase!r}")

    return errors
