from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.gadd_generated_contracts import validate_command_contract


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_package(root: Path, skill_content: str | None = None) -> Path:
    package_root = root / "package"
    write(
        package_root / "agent-skills.json",
        """{
  "commands": [
    {
      "command": "/gadd:next",
      "skill": "gadd-next",
      "path": "skills/gadd-next"
    }
  ]
}
""",
    )
    write(
        package_root / "commands" / "gadd" / "next.md",
        "Use the `gadd-next` skill to run `/gadd:next`.\n"
        "\nTreat `skills/gadd-next/SKILL.md` as canonical.\n",
    )
    write(
        package_root / "skills" / "gadd-next" / "SKILL.md",
        skill_content
        or """---
name: gadd-next
---

# /gadd:next

## Inputs

Mapped commands:

- `/gadd:next`

## Required Implementation Map Phrases

- /gadd:research
""",
    )
    return package_root


class GeneratedCommandContractTests(unittest.TestCase):
    def test_validates_command_manifest_adapter_and_skill_surface(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = create_package(Path(temp_dir))

            self.assertEqual([], validate_command_contract(package_root, "/gadd:next"))

    def test_fails_when_generated_skill_is_broken(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = create_package(Path(temp_dir), skill_content="broken generated skill\n")

            errors = validate_command_contract(package_root, "/gadd:next")

        self.assertTrue(any("frontmatter" in error for error in errors), errors)
        self.assertTrue(any("skill heading" in error for error in errors), errors)
        self.assertTrue(any("mapped command" in error for error in errors), errors)

    def test_frontmatter_name_must_be_declared_in_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = create_package(
                Path(temp_dir),
                skill_content="""This is not frontmatter.

name: gadd-next

# /gadd:next

Mapped commands:

- `/gadd:next`
""",
            )

            errors = validate_command_contract(package_root, "/gadd:next")

        self.assertTrue(any("frontmatter missing" in error for error in errors), errors)

    def test_required_phrases_must_be_in_declared_section(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = create_package(
                Path(temp_dir),
                skill_content="""---
name: gadd-next
---

# /gadd:next

## Inputs

Mapped commands:

- `/gadd:next`

## Notes

- /gadd:research
""",
            )

            errors = validate_command_contract(
                package_root,
                "/gadd:next",
                required_section_phrases={"Required Implementation Map Phrases": ["/gadd:research"]},
            )

        self.assertTrue(any("Required Implementation Map Phrases" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
