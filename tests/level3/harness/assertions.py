from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tests.level2.harness.artifact_quality import ArtifactReference, evaluate_artifacts
from tests.level2.harness.ticket_quality import Ticket, evaluate_ticket
from tests.level3.harness.agent_adapter import AgentExecutionResult
from tests.level3.harness.local_tracker import LocalTracker
from tests.level3.harness.transcript import find_secret_like_values


@dataclass(frozen=True)
class Level3Finding:
    message: str


def evaluate_expectations(
    sandbox_path: Path,
    result: AgentExecutionResult,
    expectations: list[dict],
    tracker: LocalTracker,
) -> list[Level3Finding]:
    findings: list[Level3Finding] = []
    transcript_text = result.transcript_path.read_text(encoding="utf-8") if result.transcript_path.is_file() else ""
    for expectation in expectations:
        if "approval_gate_requested" in expectation:
            if expectation["approval_gate_requested"] and "approval required" not in transcript_text.lower():
                findings.append(Level3Finding("approval gate was not requested"))
        elif "no_continuation_past_approval" in expectation:
            if expectation["no_continuation_past_approval"] and "continuing without approval" in transcript_text.lower():
                findings.append(Level3Finding("agent continued past approval gate"))
        elif "artifact_exists" in expectation:
            relative = str(expectation["artifact_exists"])
            if not (sandbox_path / relative).is_file():
                findings.append(Level3Finding(f"missing expected artifact: {relative}"))
        elif "tickets_pass_quality" in expectation:
            if expectation["tickets_pass_quality"]:
                findings.extend(_evaluate_local_ticket_quality(tracker))
        elif "artifacts_pass_quality" in expectation:
            findings.extend(_evaluate_artifact_quality(sandbox_path, expectation["artifacts_pass_quality"]))
        elif "verification_recorded" in expectation:
            if expectation["verification_recorded"] and not _has_verification_artifact(sandbox_path):
                findings.append(Level3Finding("verification artifact was not recorded"))
        elif "implementation_changed_files" in expectation:
            expected = sorted(str(path) for path in expectation["implementation_changed_files"])
            actual = sorted(path for path in result.files_changed if not path.startswith("gadd/"))
            if actual != expected:
                findings.append(Level3Finding(f"implementation changed files mismatch: expected {expected}, got {actual}"))
        elif "transcript_contains" in expectation:
            expected_text = str(expectation["transcript_contains"])
            if expected_text not in transcript_text:
                findings.append(Level3Finding(f"transcript missing expected text: {expected_text}"))
        elif "transcript_safe" in expectation:
            if expectation["transcript_safe"]:
                findings.extend(Level3Finding(finding.message) for finding in find_secret_like_values(transcript_text))
        else:
            findings.append(Level3Finding(f"unsupported expectation: {expectation}"))
    return findings


def _evaluate_local_ticket_quality(tracker: LocalTracker) -> list[Level3Finding]:
    findings: list[Level3Finding] = []
    for issue in tracker.list_issues():
        ticket = Ticket(
            role=issue.role,
            title=issue.title,
            body=issue.body,
            state=issue.state,
            labels=issue.labels,
            comments=[],
        )
        for finding in evaluate_ticket(ticket):
            findings.append(Level3Finding(f"issue {issue.number}: {finding.message}"))
    return findings


def _has_verification_artifact(sandbox_path: Path) -> bool:
    return any(path.name == "verification.md" for path in sandbox_path.glob("gadd/work-items/**/verification.md"))


def _evaluate_artifact_quality(sandbox_path: Path, references: list[dict]) -> list[Level3Finding]:
    artifact_references = [
        ArtifactReference(path=str(reference["path"]), kind=str(reference["kind"]))
        for reference in references
    ]
    return [
        Level3Finding(f"{finding.path}: {finding.message}")
        for finding in evaluate_artifacts(sandbox_path, artifact_references)
    ]
