from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate-gaps-implementation.py"
REFERENCE = ROOT / "gaps" / "examples" / "gadd" / "implementation.yml"


def load_reference() -> dict:
    result = subprocess.run(
        [
            "ruby",
            "-ryaml",
            "-rjson",
            "-e",
            "puts JSON.generate(YAML.load_file(ARGV[0]))",
            str(REFERENCE),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


class ValidateGapsImplementationTests(unittest.TestCase):
    def run_validator(self, *paths: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(VALIDATOR), *(str(path) for path in paths)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_invalid_map(self, mutate) -> Path:
        data = load_reference()
        mutate(data)
        temp_dir = tempfile.TemporaryDirectory(prefix="gaps-implementation-invalid-")
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "implementation.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_gadd_implementation_map_passes(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_missing_skill_fails(self) -> None:
        def mutate(data: dict) -> None:
            data["laneImplementations"]["intake"]["skills"].append("missing-skill")

        spec = self.write_invalid_map(mutate)
        result = self.run_validator(spec)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing-skill", result.stderr)

    def test_unmapped_process_lane_fails(self) -> None:
        def mutate(data: dict) -> None:
            data["laneImplementations"].pop("implementation")

        spec = self.write_invalid_map(mutate)
        result = self.run_validator(spec)
        self.assertEqual(result.returncode, 1)
        self.assertIn("implementation", result.stderr)


if __name__ == "__main__":
    unittest.main()
