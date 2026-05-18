from pathlib import Path
from unittest import mock
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

    def test_create_sandbox_can_seed_package_from_override_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package_root = root / "generated-package"
            (package_root / "skills" / "generated-skill").mkdir(parents=True)
            (package_root / "skills" / "generated-skill" / "SKILL.md").write_text(
                "generated\n", encoding="utf-8"
            )
            (package_root / "agent-skills.json").write_text(
                '{"commands":[]}\n', encoding="utf-8"
            )
            (package_root / "commands" / "generated" / "run.md").parent.mkdir(parents=True)
            (package_root / "commands" / "generated" / "run.md").write_text(
                "generated command\n", encoding="utf-8"
            )
            (package_root / ".claude-plugin").mkdir()
            (package_root / ".claude-plugin" / "plugin.json").write_text(
                '{"commands":["./commands/generated/run.md"]}\n', encoding="utf-8"
            )
            (package_root / "gemini-extension.json").write_text(
                '{"commands":["/generated:run"]}\n', encoding="utf-8"
            )

            sandbox = create_sandbox(
                run_root=root / "run",
                scenario_id="scenario",
                seed_files={},
                package_root=package_root,
            )

            self.assertTrue((sandbox.path / "skills" / "generated-skill" / "SKILL.md").is_file())
            self.assertEqual(
                "generated\n",
                (sandbox.path / "skills" / "generated-skill" / "SKILL.md").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertEqual(
                "generated command\n",
                (sandbox.path / "commands" / "generated" / "run.md").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertTrue((sandbox.path / ".claude-plugin" / "plugin.json").is_file())
            self.assertTrue((sandbox.path / "gemini-extension.json").is_file())

    def test_create_sandbox_requires_generated_package_surfaces(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package_root = root / "empty-package"
            package_root.mkdir()

            with self.assertRaisesRegex(ValueError, "generated package missing"):
                create_sandbox(
                    run_root=root / "run",
                    scenario_id="scenario",
                    seed_files={},
                    package_root=package_root,
                )

    def test_run_level3_fails_when_contract_command_skill_is_broken(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package_root = root / "generated"
            (package_root / "skills" / "gadd-approve").mkdir(parents=True)
            (package_root / "skills" / "gadd-approve" / "SKILL.md").write_text(
                "broken generated skill\n", encoding="utf-8"
            )
            (package_root / "commands" / "gadd").mkdir(parents=True)
            (package_root / "commands" / "gadd" / "approve.md").write_text(
                "Use the `gadd-approve` skill to run `/gadd:approve`.\n"
                "\nTreat `skills/gadd-approve/SKILL.md` as canonical.\n",
                encoding="utf-8",
            )
            (package_root / ".claude-plugin").mkdir()
            (package_root / ".claude-plugin" / "plugin.json").write_text(
                '{"commands":["./commands/gadd/approve.md"]}\n', encoding="utf-8"
            )
            (package_root / "gemini-extension.json").write_text(
                '{"commands":["/gadd:approve"]}\n', encoding="utf-8"
            )
            (package_root / "agent-skills.json").write_text(
                '{"commands":[{"command":"/gadd:approve","skill":"gadd-approve","path":"skills/gadd-approve"}]}\n',
                encoding="utf-8",
            )

            scenario = {
                "id": "broken-contract",
                "steps": [
                    {
                        "name": "approve",
                        "prompt": "Approved.",
                        "contract_commands": ["/gadd:approve"],
                        "scripted_response": "Approved.\n",
                        "expect": [],
                    }
                ],
            }

            with mock.patch.dict("os.environ", {"GADD_PACKAGE_ROOT": str(package_root)}):
                findings = __import__(
                    "tests.level3.harness.run_level3", fromlist=["run_scenario"]
                ).run_scenario(
                    config=load_config(env={}),
                    scenario=scenario,
                    runs_dir=root / "runs",
                    adapter_name="scripted",
                    tracker_mode="local",
                )

        self.assertTrue(any("generated package contract failed" in finding for finding in findings), findings)
        self.assertTrue(any("frontmatter" in finding for finding in findings), findings)
        self.assertTrue(any("skill heading" in finding for finding in findings), findings)

    def test_run_level3_continues_after_non_contract_findings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package_root = root / "generated"
            (package_root / "skills").mkdir(parents=True)
            (package_root / "commands").mkdir()
            (package_root / ".claude-plugin").mkdir()
            (package_root / "agent-skills.json").write_text('{"commands":[]}\n', encoding="utf-8")
            (package_root / ".claude-plugin" / "plugin.json").write_text(
                '{"commands":[]}\n', encoding="utf-8"
            )
            (package_root / "gemini-extension.json").write_text(
                '{"commands":[]}\n', encoding="utf-8"
            )
            scenario = {
                "id": "continue-after-finding",
                "steps": [
                    {
                        "name": "first",
                        "prompt": "First.",
                        "scripted_response": "First.\n",
                        "expect": [{"transcript_contains": "missing expected text"}],
                    },
                    {
                        "name": "second",
                        "prompt": "Second.",
                        "scripted_response": "Second ran.\n",
                        "expect": [{"transcript_contains": "Second ran"}],
                    },
                ],
            }
            config = load_config(env={})

            with mock.patch.dict("os.environ", {"GADD_PACKAGE_ROOT": str(package_root)}):
                findings = __import__(
                    "tests.level3.harness.run_level3", fromlist=["run_scenario"]
                ).run_scenario(
                    config=config,
                    scenario=scenario,
                    runs_dir=root / "runs",
                    adapter_name="scripted",
                    tracker_mode="local",
                )

            second_transcript = (
                root
                / "runs"
                / config.run_id
                / "continue-after-finding"
                / "transcripts"
                / "continue-after-finding-second.md"
            )

            self.assertTrue(any("missing expected text" in finding for finding in findings), findings)
            self.assertTrue(second_transcript.is_file())


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

    def test_github_tracker_without_env_skips_in_non_strict_mode(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with mock.patch.dict("os.environ", {}, clear=True):
                exit_code = main(
                    [
                        "--adapter",
                        "scripted",
                        "--tracker",
                        "github",
                        "--case",
                        "approval-gate-stop",
                        "--runs-dir",
                        temp_dir,
                    ]
                )

        self.assertEqual(0, exit_code)

    def test_github_tracker_without_env_fails_in_strict_mode(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with mock.patch.dict("os.environ", {}, clear=True):
                exit_code = main(
                    [
                        "--adapter",
                        "scripted",
                        "--tracker",
                        "github",
                        "--case",
                        "approval-gate-stop",
                        "--runs-dir",
                        temp_dir,
                        "--strict-tracker",
                    ]
                )

        self.assertEqual(1, exit_code)


if __name__ == "__main__":
    unittest.main()
