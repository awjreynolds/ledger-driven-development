from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import os
import sys

from tests.level2.harness.github_client import RepoRef


ROOT = Path(__file__).resolve().parents[3]
RUNS_DIR = ROOT / "tests" / "level2" / ".runs"


@dataclass(frozen=True)
class Config:
    skip_live: bool
    product_repo: RepoRef | None
    product_repo_path: Path | None
    render_repo: RepoRef | None
    render_repo_path: Path | None
    token: str | None
    cleanup: str
    run_id: str

    @property
    def product_repo_owner(self) -> str | None:
        return self.product_repo.owner if self.product_repo else None

    @property
    def product_repo_name(self) -> str | None:
        return self.product_repo.repo if self.product_repo else None


def load_config(env: dict[str, str] | None = None) -> Config:
    values = dict(os.environ if env is None else env)
    cleanup = values.get("GADD_L2_CLEANUP", "never")
    if cleanup not in {"never", "success", "always"}:
        raise ValueError("GADD_L2_CLEANUP must be one of: never, success, always")

    repo_value = values.get("GADD_L2_GITHUB_REPO")
    token = values.get("GADD_L2_GITHUB_TOKEN")
    run_id = values.get("GADD_L2_RUN_ID", "gadd-l2-local")
    if not repo_value or not token:
        return Config(
            skip_live=True,
            product_repo=None,
            product_repo_path=None,
            render_repo=None,
            render_repo_path=None,
            token=None,
            cleanup=cleanup,
            run_id=run_id,
        )

    render_repo = RepoRef.parse(values["GADD_L2_RENDER_REPO"]) if values.get("GADD_L2_RENDER_REPO") else None
    render_path = Path(values["GADD_L2_RENDER_REPO_PATH"]) if values.get("GADD_L2_RENDER_REPO_PATH") else None
    return Config(
        skip_live=False,
        product_repo=RepoRef.parse(repo_value),
        product_repo_path=Path(values["GADD_L2_PRODUCT_REPO_PATH"]) if values.get("GADD_L2_PRODUCT_REPO_PATH") else None,
        render_repo=render_repo,
        render_repo_path=render_path,
        token=token,
        cleanup=cleanup,
        run_id=run_id,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run live GitHub-backed GADD Level 2 quality checks.")
    parser.add_argument("--audit-existing", action="store_true", help="Inspect existing sandbox tickets without creating new artifacts.")
    parser.add_argument("--strict", action="store_true", help="Fail instead of skipping when live GitHub env is missing.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        config = load_config()
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    if config.skip_live:
        message = "Skipping Level 2 GitHub tests: set GADD_L2_GITHUB_REPO and GADD_L2_GITHUB_TOKEN to run live checks."
        print(message)
        return 1 if args.strict else 0
    print(f"Level 2 GitHub config loaded for {config.product_repo.full_name}; run_id={config.run_id}")
    return 0
