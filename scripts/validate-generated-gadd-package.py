#!/usr/bin/env python3
"""Validate generated GADD package output against available behavior harnesses."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile

from gadd_generated_contracts import validate_command_contract

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]


BEHAVIOR_CONTRACTS = {
    "gadd-next": [
        "/gadd:research",
        "/gadd:scope",
        "/gadd:elaborate",
        "/gadd:refine",
        "/gadd:design",
        "/gadd:plan",
        "/gadd:decompose",
        "/gadd:implement",
        "/gadd:verify",
        "/gadd:close",
        "/gadd:archive",
        "next command",
    ],
    "gadd-implement": [
        "approved boundary",
        "Do not close external Work Item projections",
        "Do not archive Work Items",
        "documentation impact",
    ],
    "gadd-approve": [
        "Approve exactly one PRD, SDD, or plan gate",
        "exactly one approval gate is active",
        "approved PRD",
        "approved SDD",
        "approved plan",
    ],
    "gadd-verify": [
        "verification.md",
        "Work Item closure",
        "human-approved closure",
    ],
}

REQUIRED_SECTIONS = {
    "gadd-implement": ["Built-in TDD Loop"],
}


def run(command: list[str], env: dict[str, str] | None = None) -> None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        env={**os.environ, **(env or {})},
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def validate_behavior_contracts(package_root: Path) -> None:
    errors: list[str] = []
    for skill, phrases in BEHAVIOR_CONTRACTS.items():
        command = f"/gadd:{skill.removeprefix('gadd-')}"
        errors.extend(
            validate_command_contract(
                package_root,
                command,
                required_sections=REQUIRED_SECTIONS.get(skill, []),
                required_section_phrases={"Required Implementation Map Phrases": phrases},
            )
        )
        skill_file = package_root / "skills" / skill / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{skill}: generated skill missing")
            continue
        content = skill_file.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in content:
                errors.append(f"{skill}: missing behavior phrase {phrase!r}")
    if errors:
        print("Generated GADD package behavior contract failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="gaps-generated-gadd-") as temp_dir:
        output_root = Path(temp_dir)
        run(
            [
                "python3",
                "scripts/generate-gaps-skill-package.py",
                "gaps/examples/gadd/ga-process.yml",
                "--output-root",
                str(output_root),
            ]
        )
        package_root = output_root / "gaps" / "generated" / "gadd"
        skill_count = len(list((package_root / "skills").glob("*/SKILL.md")))
        if skill_count != 15:
            print(
                f"Generated GADD package expected 15 command skills, found {skill_count}",
                file=sys.stderr,
            )
            return 1

        run(["python3", "scripts/validate-gaps-implementation.py", str(package_root / "implementation.yml")])
        validate_behavior_contracts(package_root)
        run(["python3", "scripts/validate-gadd-level1.py"])

        generated_env = {"GADD_PACKAGE_ROOT": str(package_root)}
        run(["python3", "scripts/run-gadd-level2.py", "--runner", "fixture-next"], env=generated_env)
        run(
            [
                "python3",
                "scripts/run-gadd-level3.py",
                "--adapter",
                "scripted",
                "--tracker",
                "local",
                "--case",
                "approval-gate-stop",
            ],
            env=generated_env,
        )
        print("Generated GADD package behavior validation passed")
        print(f"Package root: {package_root}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
