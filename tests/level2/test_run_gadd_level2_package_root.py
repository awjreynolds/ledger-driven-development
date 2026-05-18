from __future__ import annotations

import importlib.util
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
