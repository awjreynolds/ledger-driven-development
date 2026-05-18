from __future__ import annotations

import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "scripts" / "generate-gaps-skill-package.py"
FIXTURE = ROOT / "tests" / "gaps" / "fixtures" / "tiny-process" / "ga-process.yml"


class GenerateGapsSkillPackageTests(unittest.TestCase):
    def run_generator(
        self, *args: str | Path, fixture: Path = FIXTURE
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(GENERATOR), str(fixture), *(str(arg) for arg in args)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_dry_run_generates_preview_files(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            output_root = Path(temp_dir)
            result = self.run_generator("--output-root", output_root)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            generated = output_root / "gaps" / "generated" / "tiny-process"
            self.assertTrue(
                (generated / "skills" / "tiny-process-intake" / "SKILL.md").is_file()
            )
            self.assertTrue((generated / "commands" / "tiny" / "intake.md").is_file())
            self.assertTrue((generated / "implementation.yml").is_file())
            self.assertTrue((generated / "validation-checklist.md").is_file())

    def test_default_mode_does_not_modify_package_roots(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            output_root = Path(temp_dir)
            result = self.run_generator("--output-root", output_root)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertFalse((output_root / "skills").exists())
            self.assertFalse((output_root / "commands").exists())

    def test_write_requires_explicit_flag(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            result = self.run_generator("--adopt-output", "--output-root", Path(temp_dir))
            self.assertEqual(result.returncode, 2)
            self.assertIn("--write", result.stderr)

    def test_write_without_adopt_output_is_rejected(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            result = self.run_generator("--write", "--output-root", Path(temp_dir))
            self.assertEqual(result.returncode, 2)
            self.assertIn("--adopt-output", result.stderr)

    def test_rejects_path_traversal_process_id_before_writing(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            output_root = Path(temp_dir) / "out"
            fixture = Path(temp_dir) / "ga-process.yml"
            fixture.write_text(
                FIXTURE.read_text(encoding="utf-8").replace(
                    "id: tiny_process", "id: ../escape"
                ),
                encoding="utf-8",
            )

            result = self.run_generator("--output-root", output_root, fixture=fixture)

            self.assertEqual(result.returncode, 1)
            self.assertIn("process.id", result.stderr)
            self.assertFalse((Path(temp_dir) / "escape").exists())
            self.assertFalse((output_root / "gaps").exists())

    def test_adopt_output_keeps_review_artifacts_under_generated_directory(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            output_root = Path(temp_dir)
            result = self.run_generator("--write", "--adopt-output", "--output-root", output_root)

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertTrue((output_root / "skills" / "tiny-process-intake" / "SKILL.md").is_file())
            self.assertTrue((output_root / "commands" / "tiny" / "intake.md").is_file())
            self.assertFalse((output_root / "README.generated.md").exists())
            self.assertFalse((output_root / "implementation.yml").exists())
            self.assertTrue(
                (
                    output_root
                    / "gaps"
                    / "generated"
                    / "tiny-process"
                    / "README.generated.md"
                ).is_file()
            )
            self.assertTrue(
                (
                    output_root
                    / "gaps"
                    / "generated"
                    / "tiny-process"
                    / "implementation.yml"
                ).is_file()
            )

    def test_adopt_output_refuses_existing_files_without_overwrite(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            output_root = Path(temp_dir)
            existing = output_root / "skills" / "tiny-process-intake" / "SKILL.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("keep me\n", encoding="utf-8")

            result = self.run_generator("--write", "--adopt-output", "--output-root", output_root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("--overwrite", result.stderr)
            self.assertEqual(existing.read_text(encoding="utf-8"), "keep me\n")

    def test_adopt_output_preflights_all_collisions_before_writing(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            output_root = Path(temp_dir)
            preview = self.run_generator("--output-root", output_root)
            self.assertEqual(preview.returncode, 0, preview.stderr + preview.stdout)

            result = self.run_generator("--write", "--adopt-output", "--output-root", output_root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("--overwrite", result.stderr)
            self.assertFalse((output_root / "skills").exists())
            self.assertFalse((output_root / "commands").exists())

    def test_adopt_output_preflights_parent_path_collisions_before_writing(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            output_root = Path(temp_dir)
            (output_root / "commands").write_text("blocks command directory\n", encoding="utf-8")

            result = self.run_generator("--write", "--adopt-output", "--output-root", output_root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("not a directory", result.stderr)
            self.assertFalse((output_root / "skills").exists())
            self.assertEqual(
                (output_root / "commands").read_text(encoding="utf-8"),
                "blocks command directory\n",
            )

    def test_adopt_output_overwrites_existing_files_when_requested(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            output_root = Path(temp_dir)
            existing = output_root / "skills" / "tiny-process-intake" / "SKILL.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("replace me\n", encoding="utf-8")

            result = self.run_generator(
                "--write", "--adopt-output", "--overwrite", "--output-root", output_root
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertNotEqual(existing.read_text(encoding="utf-8"), "replace me\n")

    def test_adopt_output_overwrite_preflights_directory_targets_before_writing(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            output_root = Path(temp_dir)
            existing_skill = output_root / "skills" / "tiny-process-intake" / "SKILL.md"
            existing_skill.parent.mkdir(parents=True)
            existing_skill.write_text("keep me\n", encoding="utf-8")
            blocked_target = output_root / "commands" / "tiny" / "intake.md"
            blocked_target.mkdir(parents=True)

            result = self.run_generator(
                "--write", "--adopt-output", "--overwrite", "--output-root", output_root
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("is a directory", result.stderr)
            self.assertEqual(existing_skill.read_text(encoding="utf-8"), "keep me\n")
            self.assertTrue(blocked_target.is_dir())

    def test_generated_implementation_uses_input_process_path(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            output_root = Path(temp_dir)
            result = self.run_generator("--output-root", output_root)

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            implementation = (
                output_root / "gaps" / "generated" / "tiny-process" / "implementation.yml"
            ).read_text(encoding="utf-8")
            self.assertIn("processSpec: tests/gaps/fixtures/tiny-process/ga-process.yml", implementation)

    def test_generated_artifacts_preserve_non_claims(self) -> None:
        with TemporaryDirectory(prefix="gaps-generator-") as temp_dir:
            output_root = Path(temp_dir)
            result = self.run_generator("--output-root", output_root)

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            generated = output_root / "gaps" / "generated" / "tiny-process"
            readme = (generated / "README.generated.md").read_text(encoding="utf-8")
            skill = (
                generated / "skills" / "tiny-process-intake" / "SKILL.md"
            ).read_text(encoding="utf-8")
            self.assertIn("no regulatory compliance", readme)
            self.assertIn("no certification", readme)
            self.assertIn("no legal sufficiency", readme)
            self.assertIn("Do not claim regulatory compliance", skill)


if __name__ == "__main__":
    unittest.main()
