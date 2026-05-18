#!/usr/bin/env python3
"""Validate GADD documentation freshness.

This check keeps the public README, workflow docs, and shareable workflow image
aligned with the canonical skill contracts and regenerated assets.
"""

from __future__ import annotations

from pathlib import Path
import filecmp
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SVG = ROOT / "docs" / "assets" / "gadd-sdlc-workflow.source.svg"
EXPORTED_SVG = ROOT / "docs" / "assets" / "gadd-sdlc-workflow.svg"
EXPORTED_PNG = ROOT / "docs" / "assets" / "gadd-sdlc-workflow.png"


REQUIRED_TEXT = {
    "README.md": [
        "GADD is a software-delivery methodology built on [Governed Autonomy]",
        "repo-local ledgers remain canonical workflow state",
        "docs/governed-autonomy/README.md",
        "/gadd:next",
        "/gadd:triage",
        "/gadd:verify",
        "/gadd:close",
        "/gadd:archive",
        "docs/assets/gadd-sdlc-workflow.png",
    ],
    "docs/workflow.md": [
        "ready_for_implementation",
        "needs_sdd",
        "needs_prd",
        "terminal handling",
        "/gadd:next",
        "/gadd:approve",
        "Close applies verified closure",
        "Archive is optional storage cleanup",
        "Linear and Jira remain follow-on optional collaboration surfaces",
    ],
    "docs/skills.md": [
        "/gadd:triage",
        "/gadd:next",
        "/gadd:approve",
        "/gadd:verify",
        "/gadd:close",
        "/gadd:archive",
        "Product Requirement lane commands reject non-product Work Item types",
    ],
    "docs/assets/gadd-sdlc-workflow.source.svg": [
        "GADD (Governed Autonomy)",
        "Direct implementation, SDD-only engineering change, Product Requirement lane, or terminal handling",
        "/gadd:archive optional",
        "SDD and plan approval gates",
        "verification + closure gates",
        "child Work Items",
        "/gadd:next reads it",
    ],
}


STALE_TEXT = {
    "docs/assets/gadd-sdlc-workflow.source.svg": [
        "requirements-to-verified-implementation slice",
        "SDD + plan approval gate",
        ">verification gate<",
        "<text x=\"1365\" y=\"823\" class=\"mono\">/gadd:archive</text>",
        "plan.md + plan.html",
    ],
    "docs/assets/gadd-sdlc-workflow.svg": [
        "requirements-to-verified-implementation slice",
        "SDD + plan approval gate",
        ">verification gate<",
        "<text x=\"1365\" y=\"823\" class=\"mono\">/gadd:archive</text>",
        "plan.md + plan.html",
    ],
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_text(errors: list[str]) -> None:
    for relative_path, snippets in REQUIRED_TEXT.items():
        path = ROOT / relative_path
        if not path.is_file():
            errors.append(f"missing documented surface: {relative_path}")
            continue
        text = read(path)
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{relative_path}: missing required current text: {snippet!r}")


def reject_stale_text(errors: list[str]) -> None:
    for relative_path, snippets in STALE_TEXT.items():
        path = ROOT / relative_path
        if not path.is_file():
            errors.append(f"missing documented surface: {relative_path}")
            continue
        text = read(path)
        for snippet in snippets:
            if snippet in text:
                errors.append(f"{relative_path}: stale workflow text remains: {snippet!r}")


def validate_assets(errors: list[str]) -> None:
    if not SOURCE_SVG.is_file():
        errors.append(f"missing source SVG: {SOURCE_SVG.relative_to(ROOT)}")
        return
    if not EXPORTED_SVG.is_file():
        errors.append(f"missing exported SVG: {EXPORTED_SVG.relative_to(ROOT)}")
        return
    if not EXPORTED_PNG.is_file():
        errors.append(f"missing exported PNG: {EXPORTED_PNG.relative_to(ROOT)}")
        return

    if not filecmp.cmp(SOURCE_SVG, EXPORTED_SVG, shallow=False):
        errors.append("docs/assets/gadd-sdlc-workflow.svg is not in sync with gadd-sdlc-workflow.source.svg")

    rsvg = shutil.which("rsvg-convert")
    if not rsvg:
        errors.append("rsvg-convert is required to validate docs/assets/gadd-sdlc-workflow.png freshness")
        return

    with tempfile.TemporaryDirectory(prefix="gadd-docs-") as temp_dir:
        temp_png = Path(temp_dir) / "gadd-sdlc-workflow.png"
        result = subprocess.run(
            [
                rsvg,
                "-w",
                "1800",
                "-h",
                "1220",
                str(SOURCE_SVG),
                "-o",
                str(temp_png),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            errors.append(f"rsvg-convert failed while validating PNG freshness: {result.stderr.strip()}")
            return
        if not filecmp.cmp(temp_png, EXPORTED_PNG, shallow=False):
            errors.append("docs/assets/gadd-sdlc-workflow.png is stale; regenerate it from gadd-sdlc-workflow.source.svg")


def main() -> int:
    errors: list[str] = []
    require_text(errors)
    reject_stale_text(errors)
    validate_assets(errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("GADD documentation freshness validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
