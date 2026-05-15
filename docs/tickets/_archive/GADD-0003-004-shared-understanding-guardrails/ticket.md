# Preserve shared-understanding guardrails

## Parent

GADD-0003 - Make GADD ready for external trackers and guided next actions

## What to build

Preserve the bounded shared-understanding behavior in PM skills and add validation coverage so it does not regress. The guardrail should keep the useful part of grill-style questioning while preventing unbounded product creep.

Expected touch points:

- `skills/gadd-scope/SKILL.md`
- `skills/gadd-elaborate/SKILL.md`
- `skills/gadd-refine/SKILL.md`
- `scripts/validate-gadd-mvp.sh`
- `README.md`
- `CONTEXT.md`

## Acceptance criteria

- PM commands require bounded shared understanding before marking a PRD ready.
- The guardrail explicitly distinguishes shared understanding from open-ended scope expansion.
- Validation checks for the PM gate language in scope, elaborate, and refine skills.
- Documentation explains why this behavior exists.
- `bash scripts/validate-gadd-mvp.sh` and `git diff --check` pass.

## Blocked by

None.

## User stories covered

1, 5, 6

## GADD Traceability

- Parent PRD: `docs/tickets/_archive/GADD-0003-tracker-readiness-guided-next/prd.md`
- Parent SDD: `docs/tickets/_archive/GADD-0003-tracker-readiness-guided-next/sdd.md`
- Plan: `docs/tickets/_archive/GADD-0003-tracker-readiness-guided-next/plan.md`
- Plan slice: `Slice 4: Shared-understanding guardrails and validation`
- Ledger: `docs/tickets/_archive/GADD-0003-004-shared-understanding-guardrails/ledger.yml`

