#!/usr/bin/env python3
"""Validate GAPS reference process files.

The validator intentionally avoids third-party dependencies. YAML is parsed by
Ruby's stdlib YAML parser and converted to JSON, then Python performs a small
JSON Schema subset plus GAPS-specific semantic checks.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "gaps" / "schema" / "ga-process.schema.json"
DEFAULT_EXAMPLES = ROOT / "gaps" / "examples"


class ValidationError(Exception):
    pass


def json_type(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, str):
        return "string"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        return "number"
    if value is None:
        return "null"
    return type(value).__name__


def schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
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


def load_process(path: Path) -> Any:
    if path.suffix == ".json":
        return load_json(path)
    return load_yaml(path)


def validate_schema(value: Any, schema: dict[str, Any], path: str, errors: list[str]) -> None:
    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        if not any(schema_type_matches(value, candidate) for candidate in expected_type):
            errors.append(f"{path}: expected one of {expected_type}, got {json_type(value)}")
            return
    elif isinstance(expected_type, str) and not schema_type_matches(value, expected_type):
        errors.append(f"{path}: expected {expected_type}, got {json_type(value)}")
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} is not one of {schema['enum']!r}")
        return

    if isinstance(value, dict):
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{path}.{required}: missing required field")

        properties = schema.get("properties", {})
        for key, child_schema in properties.items():
            if key in value:
                validate_schema(value[key], child_schema, child_path(path, key), errors)

        additional = schema.get("additionalProperties", True)
        if additional is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{child_path(path, key)}: unexpected field")
        elif isinstance(additional, dict):
            for key, child_value in value.items():
                if key not in properties:
                    validate_schema(child_value, additional, child_path(path, key), errors)

    if isinstance(value, list) and "items" in schema:
        for index, item in enumerate(value):
            validate_schema(item, schema["items"], child_path(path, str(index)), errors)


def child_path(parent: str, child: str) -> str:
    if parent == "$":
        return f"$.{child}"
    return f"{parent}.{child}"


def require_non_empty_list(spec: dict[str, Any], path: str, errors: list[str]) -> None:
    value = get_path(spec, path)
    if not isinstance(value, list) or not value:
        errors.append(f"$.{path}: must be a non-empty list")


def require_non_empty_object(spec: dict[str, Any], path: str, errors: list[str]) -> None:
    value = get_path(spec, path)
    if not isinstance(value, dict) or not value:
        errors.append(f"$.{path}: must be a non-empty object")


def get_path(data: Any, dotted_path: str) -> Any:
    current = data
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def semantic_checks(spec: Any, source: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(spec, dict):
        return [f"$: expected object, got {json_type(spec)}"]

    if "standardsAlignment" in spec:
        errors.append("$.standardsAlignment: stale field; use standards_alignment")
    if "standards_alignment" not in spec:
        errors.append("$.standards_alignment: missing required field")
    elif "standard_aliases" not in spec["standards_alignment"]:
        errors.append("$.standards_alignment.standard_aliases: missing required field")

    require_non_empty_object(spec, "roles", errors)
    require_non_empty_object(spec, "lanes", errors)
    require_non_empty_object(spec, "governedAutonomyRiskPatterns", errors)
    require_non_empty_list(spec, "controlMappings", errors)
    require_non_empty_list(spec, "knownGaps", errors)

    vocabulary = get_path(spec, "autonomyVocabulary")
    gate_types = set(vocabulary.get("gateTypes", [])) if isinstance(vocabulary, dict) else set()
    authority_planes = set(vocabulary.get("authorityPlanes", [])) if isinstance(vocabulary, dict) else set()
    autonomy_tiers = set(vocabulary.get("tiers", [])) if isinstance(vocabulary, dict) else set()
    risk_tiers = set(vocabulary.get("riskTiers", [])) if isinstance(vocabulary, dict) else set()

    lanes = spec.get("lanes")
    if isinstance(lanes, dict):
        for lane_name, lane in lanes.items():
            lane_path = f"$.lanes.{lane_name}"
            if not isinstance(lane, dict):
                errors.append(f"{lane_path}: expected object")
                continue
            if not lane.get("purpose"):
                errors.append(f"{lane_path}.purpose: missing required field")
            validate_lane_authority(lane, lane_path, authority_planes, autonomy_tiers, risk_tiers, errors)
            validate_lane_evidence(lane, lane_path, errors)
            validate_lane_gates(lane, lane_path, gate_types, errors)

    mappings = spec.get("controlMappings")
    if isinstance(mappings, list):
        for index, mapping in enumerate(mappings):
            mapping_path = f"$.controlMappings.{index}"
            if not isinstance(mapping, dict):
                errors.append(f"{mapping_path}: expected object")
                continue
            if mapping.get("mappingStatus") not in {"unmapped", "candidate", "reviewed"}:
                errors.append(f"{mapping_path}.mappingStatus: invalid mapping status")
            if not isinstance(mapping.get("evidenceReferences"), list):
                errors.append(f"{mapping_path}.evidenceReferences: expected array")

    text = source.read_text(encoding="utf-8") if source.is_file() else ""
    blocked_claims = [
        "certification support: true",
        "regulatory compliant",
        "legally sufficient",
        "is certified",
        "is compliant",
    ]
    lowered = text.lower()
    for phrase in blocked_claims:
        if phrase in lowered:
            errors.append(f"$: prohibited overclaiming phrase {phrase!r}")

    return errors


def validate_lane_authority(
    lane: dict[str, Any],
    lane_path: str,
    authority_planes: set[str],
    autonomy_tiers: set[str],
    risk_tiers: set[str],
    errors: list[str],
) -> None:
    authority = lane.get("authority")
    if not isinstance(authority, dict):
        errors.append(f"{lane_path}.authority: missing required object")
        return
    if authority.get("plane") not in authority_planes:
        errors.append(f"{lane_path}.authority.plane: invalid authority plane")
    if authority.get("autonomyTier") not in autonomy_tiers:
        errors.append(f"{lane_path}.authority.autonomyTier: invalid autonomy tier")
    if authority.get("riskTier") not in risk_tiers:
        errors.append(f"{lane_path}.authority.riskTier: invalid risk tier")
    for field in ("allowed", "prohibited"):
        if not isinstance(authority.get(field), list) or not authority[field]:
            errors.append(f"{lane_path}.authority.{field}: must be a non-empty list")


def validate_lane_evidence(lane: dict[str, Any], lane_path: str, errors: list[str]) -> None:
    evidence = lane.get("evidence")
    if not isinstance(evidence, dict):
        errors.append(f"{lane_path}.evidence: missing required object")
        return
    for field in ("input", "completion"):
        if not isinstance(evidence.get(field), list) or not evidence[field]:
            errors.append(f"{lane_path}.evidence.{field}: must be a non-empty list")


def validate_lane_gates(
    lane: dict[str, Any], lane_path: str, gate_types: set[str], errors: list[str]
) -> None:
    gates = lane.get("gates")
    if not isinstance(gates, list) or not gates:
        errors.append(f"{lane_path}.gates: must be a non-empty list")
        return
    for index, gate in enumerate(gates):
        gate_path = f"{lane_path}.gates.{index}"
        if not isinstance(gate, dict):
            errors.append(f"{gate_path}: expected object")
            continue
        if gate.get("gateType") not in gate_types:
            errors.append(f"{gate_path}.gateType: invalid gate type")
        for field in ("id", "approvalRole", "approvalCondition", "escalationCondition"):
            if not gate.get(field):
                errors.append(f"{gate_path}.{field}: missing required field")


def discover_examples() -> list[Path]:
    return sorted(DEFAULT_EXAMPLES.glob("*/ga-process.yml"))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Process files to validate")
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help=f"Schema path (default: {DEFAULT_SCHEMA})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    schema = load_json(args.schema)
    paths = args.paths or discover_examples()
    if not paths:
        print("GAPS validation failed: no ga-process.yml files found", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for path in paths:
        process_path = path if path.is_absolute() else ROOT / path
        try:
            spec = load_process(process_path)
        except ValidationError as error:
            all_errors.append(str(error))
            continue

        schema_errors: list[str] = []
        validate_schema(spec, schema, "$", schema_errors)
        semantic_errors = semantic_checks(spec, process_path)
        for error in [*schema_errors, *semantic_errors]:
            all_errors.append(f"{process_path}: {error}")

    if all_errors:
        print("GAPS validation failed:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"GAPS validation passed ({len(paths)} process specs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
