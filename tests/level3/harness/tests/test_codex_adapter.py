from pathlib import Path
import tempfile
import unittest

from tests.level3.harness.agent_adapter import AgentExecutionRequest
from tests.level3.harness.codex_adapter import CodexAgentAdapter, codex_command_from_env


class CodexAdapterTests(unittest.TestCase):
    def test_codex_command_defaults_to_codex_exec(self):
        self.assertEqual(["codex", "exec"], codex_command_from_env({}))

    def test_codex_command_reads_env_string(self):
        self.assertEqual(
            ["codex", "exec", "--model", "gpt-5.2"],
            codex_command_from_env({"GADD_L3_CODEX_COMMAND": "codex exec --model gpt-5.2"}),
        )

    def test_missing_codex_binary_returns_failure_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            adapter = CodexAgentAdapter(command=["/definitely/missing/codex"])
            request = AgentExecutionRequest(
                run_id="run",
                scenario_id="scenario",
                step_name="step",
                sandbox_path=root,
                prompt="Run GADD.",
                step={},
                timeout_seconds=1,
                transcript_dir=root / "transcripts",
            )

            result = adapter.run(request)

            self.assertNotEqual(0, result.exit_status)
            self.assertEqual("adapter executable not found", result.failure_reason)


if __name__ == "__main__":
    unittest.main()
