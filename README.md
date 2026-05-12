# Ledger-Driven Development Skills

Installable Codex skills for the Ledger-Driven Development MVP.

LDD uses GitHub Issues and Pull Requests as the workflow ledger. It separates product scope, engineering design, implementation planning, and implementation so AI-assisted work has explicit reviewable handoffs.

## Install

Install all MVP skills into Codex:

```sh
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo awjreynolds/ledger-driven-development \
  --path skills/ldd-setup \
  --path skills/ldd-next \
  --path skills/ldd-scope \
  --path skills/ldd-elaborate \
  --path skills/ldd-refine \
  --path skills/ldd-design \
  --path skills/ldd-plan \
  --path skills/ldd-implement
```

Restart Codex after installing.

There is no `ldd-core` skill to install. The shared LDD rules are intentionally embedded in each command-shaped skill so users install and invoke the same surface:

```text
/ldd:setup
/ldd:next
/ldd:scope
/ldd:elaborate
/ldd:refine
/ldd:design
/ldd:plan
/ldd:implement
```

## MVP Workflow

```text
GitHub issue
  -> PRD PR
  -> SDD/Plan PR
  -> Implementation PR
  -> issue closed
```

GitHub is the ledger. LDD reads native issue and PR state rather than creating phase labels, local progress logs, audit files, or workflow Actions.

## Handoff Artifacts

`/ldd:setup` installs templates into a target repository:

```text
.ldd/config.yml
.ldd/templates/prd.md
.ldd/templates/sdd.md
.ldd/templates/plan.md
.ldd/templates/plan.html
.ldd/templates/pr-body-prd.md
.ldd/templates/pr-body-sdd-plan.md
.ldd/templates/pr-body-implementation.md
docs/tickets/
```

The templates are quality contracts, not blank forms:

- PRDs keep product scope separate from technical design.
- SDDs translate approved PRDs into designs grounded in code and ADRs.
- Plans trace acceptance criteria to implementation slices and verification.
- PR bodies focus reviewers on the correct handoff question.

## Command Summary

| Skill | Purpose |
| --- | --- |
| `ldd-setup` | Bootstrap LDD files in a target GitHub repo. |
| `ldd-next` | Read GitHub state for one issue and report the next LDD command. |
| `ldd-scope` | Write PRD goals, non-goals, and initial constraints. |
| `ldd-elaborate` | Fill product detail inside the approved scope. |
| `ldd-refine` | Make the PRD testable and ready for engineering design review. |
| `ldd-design` | Write the SDD and apply the ADR threshold. |
| `ldd-plan` | Write the implementation plan and generated HTML review copy. |
| `ldd-implement` | Execute the approved plan with code and tests. |

## Validate This Repo

```sh
./scripts/validate-ldd-mvp.sh
```
