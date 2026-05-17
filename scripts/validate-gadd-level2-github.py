#!/usr/bin/env python3
"""Run opt-in live GitHub-backed GADD Level 2 quality scenarios."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.level2.harness.run_level2 import main


if __name__ == "__main__":
    raise SystemExit(main())
