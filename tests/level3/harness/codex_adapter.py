from __future__ import annotations

import os
import shlex
import subprocess
import time
from pathlib import Path

from tests.level3.harness.agent_adapter import AgentExecutionRequest, AgentExecutionResult


def codex_command_from_env(env: dict[str, str] | None = None) -> list[str]:
    values = dict(os.environ if env is None else env)
    return shlex.split(values.get("GADD_L3_CODEX_COMMAND", "codex exec"))


def _snapshot_files(root: Path) -> dict[str, float]:
    return {str(path.relative_to(root)): path.stat().st_mtime for path in root.rglob("*") if path.is_file()}


class CodexAgentAdapter:
    def __init__(self, command: list[str] | None = None) -> None:
        self.command = command or codex_command_from_env()

    def run(self, request: AgentExecutionRequest) -> AgentExecutionResult:
        started = time.monotonic()
        request.transcript_dir.mkdir(parents=True, exist_ok=True)
        stdout_path = request.transcript_dir / f"{request.scenario_id}-{request.step_name}.stdout.txt"
        stderr_path = request.transcript_dir / f"{request.scenario_id}-{request.step_name}.stderr.txt"
        transcript_path = request.transcript_dir / f"{request.scenario_id}-{request.step_name}.md"
        before = _snapshot_files(request.sandbox_path)

        try:
            completed = subprocess.run(
                [*self.command, request.prompt],
                cwd=request.sandbox_path,
                text=True,
                capture_output=True,
                timeout=request.timeout_seconds,
                check=False,
            )
            stdout_path.write_text(completed.stdout, encoding="utf-8")
            stderr_path.write_text(completed.stderr, encoding="utf-8")
            transcript_path.write_text(
                f"# Transcript\n\n## Prompt\n{request.prompt}\n\n## Stdout\n{completed.stdout}\n\n## Stderr\n{completed.stderr}\n",
                encoding="utf-8",
            )
            after = _snapshot_files(request.sandbox_path)
            changed = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
            return AgentExecutionResult(
                exit_status=completed.returncode,
                transcript_path=transcript_path,
                stdout_path=stdout_path,
                stderr_path=stderr_path,
                files_changed=changed,
                duration_seconds=round(time.monotonic() - started, 3),
                failure_reason=None if completed.returncode == 0 else "adapter command failed",
            )
        except FileNotFoundError:
            transcript_path.write_text(f"# Transcript\n\nAdapter executable not found: {self.command[0]}\n", encoding="utf-8")
            return AgentExecutionResult(
                exit_status=127,
                transcript_path=transcript_path,
                stdout_path=None,
                stderr_path=None,
                files_changed=[],
                duration_seconds=round(time.monotonic() - started, 3),
                failure_reason="adapter executable not found",
            )
        except subprocess.TimeoutExpired:
            transcript_path.write_text("# Transcript\n\nAdapter timed out.\n", encoding="utf-8")
            return AgentExecutionResult(
                exit_status=124,
                transcript_path=transcript_path,
                stdout_path=None,
                stderr_path=None,
                files_changed=[],
                duration_seconds=round(time.monotonic() - started, 3),
                failure_reason="adapter timed out",
            )
