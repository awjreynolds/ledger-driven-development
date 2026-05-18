from __future__ import annotations

import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "scripts" / "generate-gaps-skill-package.py"
FIXTURE = ROOT / "tests" / "gaps" / "fixtures" / "tiny-process" / "ga-process.yml"


class GenerateGapsSkillPackageTests(unittest.TestCase):
    def run_generator(self, *args: str | Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(GENERATOR), str(FIXTURE), *(str(arg) for arg in args)],
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
            generated = output_root / "gaps" / "generated" / "tiny_process"
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


if __name__ == "__main__":
    unittest.main()
