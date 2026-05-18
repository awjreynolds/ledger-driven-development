from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[3]
PACKAGE_PATHS = [
    "skills",
    "commands",
    "agent-skills.json",
    ".claude-plugin",
    "gemini-extension.json",
    "README.md",
    "docs/skills.md",
    "docs/workflow.md",
    "docs/package-model.md",
]
REQUIRED_OVERRIDE_PACKAGE_PATHS = {
    "skills",
    "commands",
    "agent-skills.json",
    ".claude-plugin",
    "gemini-extension.json",
}


@dataclass(frozen=True)
class Sandbox:
    scenario_id: str
    path: Path


def _copy_path(source: Path, target: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _package_source(relative_path: str, package_root: Path | None) -> Path | None:
    if package_root is not None:
        generated_source = package_root / relative_path
        if generated_source.exists():
            return generated_source
        if relative_path in REQUIRED_OVERRIDE_PACKAGE_PATHS:
            raise ValueError(f"generated package missing required path: {generated_source}")
    repo_source = ROOT / relative_path
    return repo_source if repo_source.exists() else None


def _safe_relative_path(path: str) -> Path:
    relative = Path(path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"seed file path must stay inside sandbox: {path}")
    return relative


def create_sandbox(
    run_root: Path,
    scenario_id: str,
    seed_files: dict[str, str] | None = None,
    package_root: Path | None = None,
) -> Sandbox:
    sandbox_path = run_root / "sandboxes" / scenario_id
    sandbox_path.mkdir(parents=True, exist_ok=True)
    if package_root is None and os.environ.get("GADD_PACKAGE_ROOT"):
        package_root = Path(os.environ["GADD_PACKAGE_ROOT"])
    for relative_path in PACKAGE_PATHS:
        source = _package_source(relative_path, package_root)
        if source is not None:
            _copy_path(source, sandbox_path / relative_path)

    for raw_path, content in (seed_files or {}).items():
        relative = _safe_relative_path(raw_path)
        target = sandbox_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    return Sandbox(scenario_id=scenario_id, path=sandbox_path)
