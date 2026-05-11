#!/usr/bin/env sh
set -eu

required_files='
.claude/commands/ldd/setup.md
.claude/commands/ldd/next.md
.claude/skills/ldd-core/SKILL.md
.claude/skills/ldd-core/templates/config.yml
.claude/skills/ldd-core/templates/prd.md
.claude/skills/ldd-core/templates/sdd.md
.claude/skills/ldd-core/templates/plan.md
.claude/skills/ldd-core/templates/plan.html
.claude/skills/ldd-core/templates/pr-body-prd.md
.claude/skills/ldd-core/templates/pr-body-sdd-plan.md
.claude/skills/ldd-core/templates/pr-body-implementation.md
'

for file in $required_files; do
  if [ ! -f "$file" ]; then
    echo "missing required file: $file" >&2
    exit 1
  fi
done

grep -q 'GitHub is the ledger' .claude/skills/ldd-core/SKILL.md
grep -q 'GitHub mutations require human confirmation' .claude/skills/ldd-core/SKILL.md
grep -q 'must not read the codebase as a design input' .claude/skills/ldd-core/SKILL.md

grep -q 'verify the repo has a GitHub remote' .claude/commands/ldd/setup.md
grep -q 'create `.ldd/config.yml`' .claude/commands/ldd/setup.md
grep -q 'It should not create labels or GitHub Actions' .claude/commands/ldd/setup.md

grep -q 'Read-only diagnostic command' .claude/commands/ldd/next.md
grep -q 'It never mutates GitHub' .claude/commands/ldd/next.md
grep -q 'If issue is closed' .claude/commands/ldd/next.md

grep -q 'docs/tickets' .claude/skills/ldd-core/templates/config.yml
grep -q '# PRD:' .claude/skills/ldd-core/templates/prd.md
grep -q '# Software Design Document:' .claude/skills/ldd-core/templates/sdd.md
grep -q '# Implementation Plan:' .claude/skills/ldd-core/templates/plan.md
grep -q 'Does this implementation follow the approved plan?' .claude/skills/ldd-core/templates/pr-body-implementation.md

echo "LDD MVP command surface validated"
