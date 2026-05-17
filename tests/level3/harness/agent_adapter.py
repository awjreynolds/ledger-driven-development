from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class AgentExecutionRequest:
    run_id: str
    scenario_id: str
    step_name: str
    sandbox_path: Path
    prompt: str
    step: dict
    timeout_seconds: int
    transcript_dir: Path


@dataclass(frozen=True)
class AgentExecutionResult:
    exit_status: int
    transcript_path: Path
    stdout_path: Path | None
    stderr_path: Path | None
    files_changed: list[str]
    duration_seconds: float
    failure_reason: str | None = None


class AgentAdapter(Protocol):
    def run(self, request: AgentExecutionRequest) -> AgentExecutionResult:
        """Execute one scenario step in the sandbox and return normalized evidence."""


class AdapterRegistry:
    def __init__(self) -> None:
        self._factories: dict[str, type[AgentAdapter]] = {}

    def register(self, name: str, factory: type[AgentAdapter]) -> None:
        self._factories[name] = factory

    def create(self, name: str) -> AgentAdapter:
        try:
            factory = self._factories[name]
        except KeyError as error:
            known = ", ".join(sorted(self._factories)) or "none"
            raise ValueError(f"unknown Level 3 adapter {name!r}; known adapters: {known}") from error
        return factory()
