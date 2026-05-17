from __future__ import annotations

from pathlib import Path
import time

from tests.level3.harness.agent_adapter import AgentExecutionRequest, AgentExecutionResult


def _safe_relative_path(path: str) -> Path:
    relative = Path(path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"scripted file path must stay inside sandbox: {path}")
    return relative


class ScriptedAgentAdapter:
    def run(self, request: AgentExecutionRequest) -> AgentExecutionResult:
        started = time.monotonic()
        transcript_dir = request.transcript_dir
        transcript_dir.mkdir(parents=True, exist_ok=True)
        transcript_path = transcript_dir / f"{request.scenario_id}-{request.step_name}.md"
        response = str(request.step.get("scripted_response", ""))
        changed: list[str] = []

        for raw_path, content in request.step.get("scripted_files", {}).items():
            relative = _safe_relative_path(str(raw_path))
            target = request.sandbox_path / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(str(content), encoding="utf-8")
            changed.append(str(relative))

        transcript_path.write_text(
            f"# Transcript\n\n## Prompt\n{request.prompt}\n\n## Response\n{response}",
            encoding="utf-8",
        )
        return AgentExecutionResult(
            exit_status=0,
            transcript_path=transcript_path,
            stdout_path=None,
            stderr_path=None,
            files_changed=sorted(changed),
            duration_seconds=round(time.monotonic() - started, 3),
        )
