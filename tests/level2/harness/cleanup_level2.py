#!/usr/bin/env python3
"""Clean up run-marked GADD Level 2 GitHub artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tests.level2.harness.github_client import GitHubClient, RepoRef
from tests.level2.harness.run_level2 import load_config, manifest_path, utc_now, write_manifest


def cleanup_run(run_id: str) -> int:
    config = load_config()
    if config.skip_live:
        print("Cannot clean up without GADD_L2_GITHUB_REPO.", file=sys.stderr)
        return 2
    path = manifest_path(run_id)
    if not path.is_file():
        print(f"Missing manifest: {path}", file=sys.stderr)
        return 2

    manifest = json.loads(path.read_text(encoding="utf-8"))
    client = GitHubClient(config.token)
    closed = []
    for issue in manifest.get("issues", []):
        repo = RepoRef.parse(issue["repo"])
        number = int(issue["number"])
        live = client.get_issue(repo, number)
        labels = [label["name"] for label in live.get("labels", [])]
        if "gadd-l2" not in labels or f"gadd-l2:{run_id}" not in labels:
            print(f"Refusing to clean unmarked issue {repo.full_name}#{number}", file=sys.stderr)
            return 1
        if live.get("state") != "closed":
            client.close_issue(repo, number)
        closed.append({"repo": repo.full_name, "number": number})

    manifest["cleanup"] = {"status": "closed_issues", "at": utc_now(), "closed": closed}
    write_manifest(run_id, manifest)
    print(f"Cleaned GADD Level 2 run {run_id}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args(argv)
    return cleanup_run(args.run_id)


if __name__ == "__main__":
    raise SystemExit(main())
