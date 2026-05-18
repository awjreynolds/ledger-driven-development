from __future__ import annotations

import importlib.util
from pathlib import Path
from unittest import mock
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "run-gadd-level2.py"


def load_runner_module():
    spec = importlib.util.spec_from_file_location("run_gadd_level2", SCRIPT)
    if not spec or not spec.loader:
        raise AssertionError(f"unable to load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Level2PackageRootTests(unittest.TestCase):
    def test_package_source_prefers_generated_package_when_path_exists(self) -> None:
        runner = load_runner_module()
        with tempfile.TemporaryDirectory(prefix="gadd-level2-package-root-") as temp_dir:
            package_root = Path(temp_dir) / "generated"
            generated_skills = package_root / "skills"
            generated_skills.mkdir(parents=True)

            self.assertEqual(generated_skills, runner.package_source("skills", package_root))
            self.assertEqual(ROOT / "README.md", runner.package_source("README.md", package_root))

    def test_package_source_requires_generated_package_surfaces(self) -> None:
        runner = load_runner_module()
        with tempfile.TemporaryDirectory(prefix="gadd-level2-package-root-") as temp_dir:
            package_root = Path(temp_dir) / "generated"
            package_root.mkdir()

            with self.assertRaisesRegex(runner.Level2Error, "generated package missing"):
                runner.package_source("skills", package_root)

    def test_level2_fails_when_generated_command_skill_is_broken(self) -> None:
        runner = load_runner_module()
        with tempfile.TemporaryDirectory(prefix="gadd-level2-package-root-") as temp_dir:
            root = Path(temp_dir)
            package_root = root / "generated"
            (package_root / "skills" / "gadd-next").mkdir(parents=True)
            (package_root / "skills" / "gadd-next" / "SKILL.md").write_text(
                "broken generated skill\n", encoding="utf-8"
            )
            (package_root / "commands" / "gadd").mkdir(parents=True)
            (package_root / "commands" / "gadd" / "next.md").write_text(
                "Use the `gadd-next` skill to run `/gadd:next`.\n"
                "\nTreat `skills/gadd-next/SKILL.md` as canonical.\n",
                encoding="utf-8",
            )
            (package_root / "agent-skills.json").write_text(
                '{"commands":[{"command":"/gadd:next","skill":"gadd-next","path":"skills/gadd-next"}]}\n',
                encoding="utf-8",
            )

            scenario = {"id": "package-contract", "steps": []}
            step = {
                "name": "next",
                "source_scenario": "full-prd-workflow",
                "fixture": "01-needs-prd",
                "work_item": "GADD-L1-PRD",
                "runner_command": "/gadd:next GADD-L1-PRD",
                "expect_output_contains": [],
                "expect_changed_files": [],
            }

            with mock.patch.dict("os.environ", {"GADD_PACKAGE_ROOT": str(package_root)}):
                errors = runner.run_step("fixture-next", scenario, step, 1, root / "artifacts")

        self.assertTrue(any("generated package contract failed" in error for error in errors), errors)
        self.assertTrue(any("frontmatter" in error for error in errors), errors)
        self.assertTrue(any("skill heading" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
