from pathlib import Path
import tempfile
import unittest

from tests.level3.harness.sandbox import create_sandbox


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


if __name__ == "__main__":
    unittest.main()
