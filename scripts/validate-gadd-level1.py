#!/usr/bin/env python3
"""Validate deterministic GADD Level 1 workflow scenarios.

Level 1 tests exercise repo-local workflow state only. They do not invoke an
agent and do not contact external trackers.
"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "level1" / "scenarios"
FIXTURES = ROOT / "tests" / "level1" / "fixtures"


class ScenarioError(Exception):
    pass


def parse_scalar(value: str):
    value = value.strip()
    if value == "":
        return None
    if value == "null":
        return None
    if value == "none":
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "[]":
        return []
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def line_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def parse_yaml_subset(path: Path):
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    lines = []
    for line in raw_lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        lines.append(line.rstrip())
    if not lines:
        return {}
    value, index = parse_block(lines, 0, line_indent(lines[0]))
    if index != len(lines):
        raise ScenarioError(f"{path}: could not parse line {index + 1}: {lines[index]}")
    return value


def parse_block(lines: list[str], index: int, indent: int):
    if index >= len(lines):
        return {}, index
    if line_indent(lines[index]) < indent:
        return {}, index
    if lines[index].lstrip().startswith("- "):
        return parse_list(lines, index, indent)
    return parse_mapping(lines, index, indent)


def parse_list(lines: list[str], index: int, indent: int):
    result = []
    while index < len(lines):
        line = lines[index]
        current_indent = line_indent(line)
        if current_indent < indent:
            break
        if current_indent != indent or not line.lstrip().startswith("- "):
            break
        content = line.strip()[2:].strip()
        index += 1
        if not content:
            item, index = parse_block(lines, index, indent + 2)
            result.append(item)
            continue
        if ":" in content:
            key, value = content.split(":", 1)
            item = {key.strip(): parse_scalar(value)}
            if index < len(lines) and line_indent(lines[index]) > indent:
                child, index = parse_block(lines, index, indent + 2)
                if isinstance(child, dict):
                    item.update(child)
                else:
                    raise ScenarioError("list item continuation must be a mapping")
            result.append(item)
        else:
            result.append(parse_scalar(content))
    return result, index


def parse_mapping(lines: list[str], index: int, indent: int):
    result = {}
    while index < len(lines):
        line = lines[index]
        current_indent = line_indent(line)
        if current_indent < indent:
            break
        if current_indent != indent:
            break
        if line.lstrip().startswith("- "):
            break
        if ":" not in line:
            raise ScenarioError(f"expected mapping line, got: {line}")
        key, value = line.strip().split(":", 1)
        index += 1
        if value.strip():
            result[key] = parse_scalar(value)
            continue
        if index < len(lines) and line_indent(lines[index]) > current_indent:
            child, index = parse_block(lines, index, current_indent + 2)
            result[key] = child
        else:
            result[key] = None
    return result, index


def get(data, dotted_path: str):
    current = data
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def command(command_name: str, work_item_id: str) -> str:
    return f"/gadd:{command_name} {work_item_id}"


def approved_triage(ledger: dict) -> bool:
    return bool(
        get(ledger, "triage.approved_outcome.status") == "approved"
        and get(ledger, "triage.approved_outcome.approved_hash")
        and get(ledger, "triage.approved_outcome.boundary_source")
    )


def closure_status(ledger: dict) -> str | None:
    return get(ledger, "closure.status")


def implemented(ledger: dict) -> bool:
    return get(ledger, "artifacts.implementation.status") == "completed"


def verification_passed(ledger: dict) -> bool:
    return get(ledger, "artifacts.verification.status") == "passed"


def closeable(ledger: dict) -> bool:
    return verification_passed(ledger) and closure_status(ledger) == "verified"


def closed(ledger: dict) -> bool:
    return closure_status(ledger) in {"closed", "externally_closed", "archived"}


def archive_cleanup_available(ledger: dict) -> bool:
    return closure_status(ledger) in {"closed", "externally_closed"}


def derive_child_next(children: list[dict]) -> dict | None:
    active_children = [child for child in children if not closed(child)]
    if not active_children:
        return None
    if children and all(closed(child) or closeable(child) for child in children):
        return None
    for child in active_children:
        if closeable(child):
            return {
                "next_command": command("close", get(child, "work_item.id")),
                "next_human_action": "human-approved closure",
            }
    for child in active_children:
        if implemented(child) and not verification_passed(child):
            return {
                "next_command": command("verify", get(child, "work_item.id")),
                "next_human_action": "none",
            }
    for child in active_children:
        if get(child, "work_item.state") == "ready_for_implementation" and approved_triage(child):
            return {
                "next_command": command("implement", get(child, "work_item.id")),
                "next_human_action": "none",
            }
    return None


def derive_next(parent: dict, children: list[dict]) -> dict:
    parent_id = get(parent, "work_item.id")
    if not parent_id:
        raise ScenarioError("parent ledger is missing work_item.id")

    if closed(parent):
        result = {
            "next_command": "done",
            "next_human_action": "none",
        }
        if archive_cleanup_available(parent):
            result["optional_cleanup_command"] = command("archive", parent_id)
        return result

    if children and all(closed(child) or closeable(child) for child in children):
        return {
            "next_command": command("close", parent_id),
            "next_human_action": "human-approved parent roll-up closure",
        }

    child_next = derive_child_next(children)
    if child_next:
        return child_next

    if closeable(parent):
        return {
            "next_command": command("close", parent_id),
            "next_human_action": "human-approved closure",
        }
    if implemented(parent) and not verification_passed(parent):
        return {
            "next_command": command("verify", parent_id),
            "next_human_action": "none",
        }

    if get(parent, "artifacts.plan.status") == "approved" and not children:
        return {
            "next_command": command("decompose", parent_id),
            "next_human_action": "none",
        }
    if get(parent, "artifacts.plan.status") == "draft":
        return {
            "next_command": command("approve", parent_id),
            "next_human_action": command("approve", parent_id),
        }
    if get(parent, "artifacts.sdd.status") == "approved":
        if (
            get(parent, "work_item.type") == "engineering_change"
            and get(parent, "artifacts.sdd.implementation_route") == "single"
        ):
            return {
                "next_command": command("implement", parent_id),
                "next_human_action": "none",
            }
        return {
            "next_command": command("plan", parent_id),
            "next_human_action": "none",
        }
    if get(parent, "artifacts.sdd.status") == "draft":
        return {
            "next_command": command("approve", parent_id),
            "next_human_action": command("approve", parent_id),
        }
    if get(parent, "artifacts.prd.status") == "approved":
        return {
            "next_command": command("design", parent_id),
            "next_human_action": "none",
        }

    phase = get(parent, "execution_context.phase")
    gate = get(parent, "execution_context.current_gate")
    if phase == "refine" and gate == "prd_approval":
        return {
            "next_command": command("approve", parent_id),
            "next_human_action": command("approve", parent_id),
        }
    if phase == "scope":
        return {
            "next_command": command("elaborate", parent_id),
            "next_human_action": "none",
        }
    if phase == "elaborate":
        return {
            "next_command": command("refine", parent_id),
            "next_human_action": "none",
        }

    state = get(parent, "work_item.state")
    if state in {"ready_for_implementation", "needs_sdd", "needs_prd"} and not approved_triage(parent):
        return {
            "next_command": command("triage", parent_id),
            "next_human_action": "approve or repair the triage outcome boundary",
        }
    if state == "ready_for_implementation":
        return {
            "next_command": command("implement", parent_id),
            "next_human_action": "none",
        }
    if state == "needs_sdd":
        return {
            "next_command": command("design", parent_id),
            "next_human_action": "none",
        }
    if state == "needs_prd":
        if get(parent, "artifacts.research.status") in {"ready_for_scope", "completed"}:
            return {
                "next_command": command("scope", parent_id),
                "next_human_action": "none",
            }
        return {
            "next_command": command("research", parent_id),
            "next_human_action": "none",
        }
    if state in {"duplicate", "out_of_scope", "not_gadd_work"}:
        return {
            "next_command": "blocked",
            "next_human_action": get(parent, "execution_context.next_human_action") or "terminal triage outcome",
        }
    if state == "blocked_on_human_decision":
        return {
            "next_command": "blocked",
            "next_human_action": get(parent, "execution_context.next_human_action") or "human decision required",
        }
    return {
        "next_command": command("next", parent_id),
        "next_human_action": "inspect ambiguous workflow state",
    }


def load_fixture(scenario: dict, step: dict) -> tuple[dict, list[dict]]:
    fixture_dir = FIXTURES / scenario["id"] / step["fixture"]
    parent_path = fixture_dir / "gadd" / "work-items" / scenario["work_item"] / "ledger.yml"
    if not parent_path.is_file():
        raise ScenarioError(f"missing fixture ledger: {parent_path}")
    parent = parse_yaml_subset(parent_path)
    children = []
    work_items_dir = fixture_dir / "gadd" / "work-items" / scenario["work_item"] / "children"
    if work_items_dir.is_dir():
        for child_path in sorted(work_items_dir.glob("*/ledger.yml")):
            children.append(parse_yaml_subset(child_path))
    return parent, children


def assert_step(scenario_path: Path, scenario: dict, step: dict) -> list[str]:
    errors = []
    if "expect_next_command" not in step:
        return [f"{scenario_path.name} / {step.get('name', '<unnamed>')}: missing expect_next_command"]
    parent, children = load_fixture(scenario, step)
    actual = derive_next(parent, children)
    expected = {
        "next_command": step.get("expect_next_command"),
        "next_human_action": step.get("expect_next_human_action", "none"),
        "optional_cleanup_command": step.get("expect_optional_cleanup_command"),
    }
    for key, expected_value in expected.items():
        if expected_value is None:
            continue
        actual_value = actual.get(key)
        if key == "optional_cleanup_command" and expected_value == "absent":
            if key in actual:
                errors.append(
                    f"{scenario_path.name} / {step['name']}: expected {key} to be absent, got {actual_value!r}"
                )
            continue
        if actual_value != expected_value:
            errors.append(
                f"{scenario_path.name} / {step['name']}: expected {key}={expected_value!r}, got {actual_value!r}"
            )
    return errors


def main() -> int:
    errors = []
    scenario_paths = sorted(SCENARIOS.glob("*.yml"))
    if not scenario_paths:
        print("no Level 1 scenarios found", file=sys.stderr)
        return 1
    for scenario_path in scenario_paths:
        scenario = parse_yaml_subset(scenario_path)
        for required in ("id", "work_item", "steps"):
            if required not in scenario:
                errors.append(f"{scenario_path}: missing required field {required}")
        if errors:
            continue
        for step in scenario["steps"]:
            errors.extend(assert_step(scenario_path, scenario, step))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"GADD Level 1 workflow scenarios validated ({len(scenario_paths)} scenarios)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
