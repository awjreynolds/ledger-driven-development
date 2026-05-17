from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[3]
PACKAGE_PATHS = [
    "skills",
    "agent-skills.json",
    "README.md",
    "docs/skills.md",
    "docs/workflow.md",
    "docs/package-model.md",
]


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


def _safe_relative_path(path: str) -> Path:
    relative = Path(path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"seed file path must stay inside sandbox: {path}")
    return relative


def create_sandbox(run_root: Path, scenario_id: str, seed_files: dict[str, str] | None = None) -> Sandbox:
    sandbox_path = run_root / "sandboxes" / scenario_id
    sandbox_path.mkdir(parents=True, exist_ok=True)
    for relative_path in PACKAGE_PATHS:
        source = ROOT / relative_path
        if source.exists():
            _copy_path(source, sandbox_path / relative_path)

    for raw_path, content in (seed_files or {}).items():
        relative = _safe_relative_path(raw_path)
        target = sandbox_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    return Sandbox(scenario_id=scenario_id, path=sandbox_path)
