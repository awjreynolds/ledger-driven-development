#!/usr/bin/env python3
"""Print or execute the GADD skill push and sandbox reinstall loop commands."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess


DEFAULT_SANDBOXES = (
    Path("/private/tmp/gadd-cad-live-test"),
    Path("/private/tmp/gadd-cad-render-test"),
)


def commands_for(sandboxes: tuple[Path, ...]) -> list[list[str]]:
    commands = [["git", "push"]]
    for sandbox in sandboxes:
        commands.append(["npx", "skills", "add", "awjreynolds/gadd", "--all", "-y", "--cwd", str(sandbox)])
    return commands


def format_commands(commands: list[list[str]]) -> str:
    return "\n".join(" ".join(command) for command in commands)


def run_commands(commands: list[list[str]]) -> int:
    for command in commands:
        result = subprocess.run(command, check=False)
        if result.returncode != 0:
            return result.returncode
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Run commands instead of printing them.")
    parser.add_argument(
        "--sandbox",
        action="append",
        type=Path,
        help="Sandbox repo path to reinstall into. May be provided more than once.",
    )
    args = parser.parse_args(argv)
    sandboxes = tuple(args.sandbox) if args.sandbox else DEFAULT_SANDBOXES
    commands = commands_for(sandboxes)
    if not args.execute:
        print(format_commands(commands))
        return 0
    return run_commands(commands)


if __name__ == "__main__":
    raise SystemExit(main())
