from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate-gaps.py"
REFERENCE = ROOT / "gaps" / "examples" / "gadd" / "ga-process.yml"


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


class ValidateGapsTests(unittest.TestCase):
    def run_validator(self, *paths: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(VALIDATOR), *(str(path) for path in paths)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_invalid_spec(self, mutate) -> Path:
        data = load_reference()
        mutate(data)
        temp_dir = tempfile.TemporaryDirectory(prefix="gaps-invalid-")
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "ga-process.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_valid_examples_pass(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_missing_known_gaps_fails(self) -> None:
        spec = self.write_invalid_spec(lambda data: data.pop("knownGaps"))
        result = self.run_validator(spec)
        self.assertEqual(result.returncode, 1)
        self.assertIn("knownGaps", result.stderr)

    def test_invalid_gate_type_fails(self) -> None:
        def mutate(data: dict) -> None:
            first_lane = next(iter(data["lanes"].values()))
            first_lane["gates"][0]["gateType"] = "rubber_stamp"

        spec = self.write_invalid_spec(mutate)
        result = self.run_validator(spec)
        self.assertEqual(result.returncode, 1)
        self.assertIn("gateType", result.stderr)

    def test_stale_standards_alignment_name_fails(self) -> None:
        def mutate(data: dict) -> None:
            data["standardsAlignment"] = data.pop("standards_alignment")

        spec = self.write_invalid_spec(mutate)
        result = self.run_validator(spec)
        self.assertEqual(result.returncode, 1)
        self.assertIn("standards_alignment", result.stderr)


if __name__ == "__main__":
    unittest.main()
