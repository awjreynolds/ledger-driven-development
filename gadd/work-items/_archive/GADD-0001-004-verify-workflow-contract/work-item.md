# Define /gadd:verify workflow and report contract

## Parent

GADD-0001 - Add GADD execution context and verification gate

## What to build

Define the standalone `/gadd:verify` command workflow and verification report contract. The command must check evidence, check drift, write `verification.md`, update child ledger verification state, and block closure when evidence is insufficient.

Expected touch points:

- `skills/gadd-verify/SKILL.md`
- `skills/gadd-setup/assets/templates/verification.md`
- `gadd/templates/verification.md`
- `scripts/validate-gadd-mvp.sh`

## Acceptance criteria

- `/gadd:verify` is explicitly scoped to child-ticket closure, not repository health.
- The command reads child ledger, parent ledger, approved PRD, approved SDD, approved plan, child Work Item, implementation evidence, check evidence, and external drift metadata.
- The command writes a human-readable `verification.md` report.
- The command updates child ledger verification status to `passed`, `failed`, or `override_required`.
- The command blocks closure when evidence is missing, checks fail, scope/design/plan drift is detected, or external ticket drift is unresolved.
- The command never mutates external trackers without human confirmation.
- `./scripts/validate-gadd-mvp.sh` and `git diff --check` pass.

## Blocked by

- GADD-0001-001
- GADD-0001-002

## User stories covered

2, 4, 5

## GADD Traceability

- Parent PRD: `gadd/work-items/_archive/GADD-0001-verify-context-header/prd.md`
- Parent SDD: `gadd/work-items/_archive/GADD-0001-verify-context-header/sdd.md`
- Plan: `gadd/work-items/_archive/GADD-0001-verify-context-header/plan.md`
- Plan slice: `4. Define /gadd:verify workflow and report contract`
- Ledger: `gadd/work-items/_archive/GADD-0001-004-verify-workflow-contract/ledger.yml`
