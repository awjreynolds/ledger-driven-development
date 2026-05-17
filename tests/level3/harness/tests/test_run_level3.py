from pathlib import Path
import tempfile
import unittest

from tests.level3.harness.sandbox import create_sandbox
from tests.level3.harness.run_level3 import load_config, main, summarize_findings


class SandboxTests(unittest.TestCase):
    def test_create_sandbox_seeds_package_and_target_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            run_root = Path(temp_dir)
            sandbox = create_sandbox(
                run_root=run_root,
                scenario_id="scenario",
                seed_files={"cad.js": "export function normalizeLayerName(name) { return name; }\n"},
            )

            self.assertTrue((sandbox.path / "skills").is_dir())
            self.assertTrue((sandbox.path / "cad.js").is_file())
            self.assertEqual("scenario", sandbox.scenario_id)


class RunLevel3ConfigTests(unittest.TestCase):
    def test_default_config_uses_scripted_local(self):
        config = load_config(env={})

        self.assertEqual("scripted", config.adapter)
        self.assertEqual("local", config.tracker)

    def test_invalid_tracker_rejected(self):
        with self.assertRaises(ValueError):
            load_config(env={"GADD_L3_TRACKER": "jira"})

    def test_summary_reports_findings(self):
        self.assertEqual("2 Level 3 findings", summarize_findings(["a", "b"]))


class RunLevel3MainTests(unittest.TestCase):
    def test_scripted_runner_executes_single_case(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            exit_code = main(
                [
                    "--adapter",
                    "scripted",
                    "--tracker",
                    "local",
                    "--case",
                    "approval-gate-stop",
                    "--runs-dir",
                    temp_dir,
                ]
            )

            self.assertEqual(0, exit_code)


if __name__ == "__main__":
    unittest.main()
