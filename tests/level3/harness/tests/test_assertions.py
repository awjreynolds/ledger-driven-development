from pathlib import Path
import tempfile
import unittest

from tests.level3.harness.assertions import evaluate_expectations
from tests.level3.harness.agent_adapter import AgentExecutionResult
from tests.level3.harness.local_tracker import LocalIssue, LocalTracker


class Level3AssertionTests(unittest.TestCase):
    def test_approval_gate_detected_from_transcript(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            transcript = root / "transcript.md"
            transcript.write_text("Approval required before design continues.\n", encoding="utf-8")
            result = AgentExecutionResult(0, transcript, None, None, [], 0.1)

            findings = evaluate_expectations(root, result, [{"approval_gate_requested": True}], LocalTracker(root))

            self.assertEqual([], findings)

    def test_missing_artifact_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            transcript = root / "transcript.md"
            transcript.write_text("Done.\n", encoding="utf-8")
            result = AgentExecutionResult(0, transcript, None, None, [], 0.1)

            findings = evaluate_expectations(root, result, [{"artifact_exists": "gadd/work-items/ITEM/prd.md"}], LocalTracker(root))

            self.assertEqual(["missing expected artifact: gadd/work-items/ITEM/prd.md"], [finding.message for finding in findings])

    def test_ticket_quality_reuses_level2_rubric(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tracker = LocalTracker(root)
            tracker.create_issue(
                LocalIssue(
                    role="Child",
                    title="Child: Normalize product layer names",
                    body=(
                        "## Boundary\nImplement product repo normalization only.\n\n"
                        "## Acceptance Criteria\nWhitespace is trimmed.\n\n"
                        "## Verification\nRun `npm test`.\n\n"
                        "## Next Action\nImplement with a failing test first.\n\n"
                        "## GADD Trace\nRun: scripted\nArtifact: gadd/work-items/CAD-0001/work-item.md\n"
                    ),
                    labels=["gadd-l2", "type:task"],
                )
            )
            transcript = root / "transcript.md"
            transcript.write_text("Created issue.\n", encoding="utf-8")
            result = AgentExecutionResult(0, transcript, None, None, [], 0.1)

            findings = evaluate_expectations(root, result, [{"tickets_pass_quality": True}], tracker)

            self.assertEqual([], findings)

    def test_transcript_contains_required_text(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            transcript = root / "transcript.md"
            transcript.write_text("Drift detected. Reconciliation required before update.\n", encoding="utf-8")
            result = AgentExecutionResult(0, transcript, None, None, [], 0.1)

            findings = evaluate_expectations(root, result, [{"transcript_contains": "Reconciliation required"}], LocalTracker(root))

            self.assertEqual([], findings)

    def test_artifact_quality_reuses_level2_rubric(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "gadd/work-items/BUG-0001/triage.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "# Triage\n\n"
                "## Source\nLocal tracker issue.\n\n"
                "## Reproduction\nRun npm test.\n\n"
                "## GitNexus Evidence\nOne affected symbol.\n\n"
                "## Route Decision\nready_for_implementation\n\n"
                "## Verification\nRun npm test.\n",
                encoding="utf-8",
            )
            transcript = root / "transcript.md"
            transcript.write_text("Created triage artifact.\n", encoding="utf-8")
            result = AgentExecutionResult(0, transcript, None, None, [], 0.1)

            findings = evaluate_expectations(
                root,
                result,
                [{"artifacts_pass_quality": [{"path": "gadd/work-items/BUG-0001/triage.md", "kind": "triage"}]}],
                LocalTracker(root),
            )

            self.assertEqual([], findings)

    def test_secret_like_transcript_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            transcript = root / "transcript.md"
            transcript.write_text("GH_TOKEN=ghp_abcdefghijklmnopqrstuvwxyz123456\n", encoding="utf-8")
            result = AgentExecutionResult(0, transcript, None, None, [], 0.1)

            findings = evaluate_expectations(root, result, [{"transcript_safe": True}], LocalTracker(root))

            self.assertEqual(["token-like value detected"], [finding.message for finding in findings])


if __name__ == "__main__":
    unittest.main()
