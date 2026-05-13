# Preserve shared-understanding guardrails

## Parent

LDD-0003 - Make LDD ready for external trackers and guided next actions

## What to build

Preserve the bounded shared-understanding behavior in PM skills and add validation coverage so it does not regress. The guardrail should keep the useful part of grill-style questioning while preventing unbounded product creep.

Expected touch points:

- `skills/ldd-scope/SKILL.md`
- `skills/ldd-elaborate/SKILL.md`
- `skills/ldd-refine/SKILL.md`
- `scripts/validate-ldd-mvp.sh`
- `README.md`
- `CONTEXT.md`

## Acceptance criteria

- PM commands require bounded shared understanding before marking a PRD ready.
- The guardrail explicitly distinguishes shared understanding from open-ended scope expansion.
- Validation checks for the PM gate language in scope, elaborate, and refine skills.
- Documentation explains why this behavior exists.
- `bash scripts/validate-ldd-mvp.sh` and `git diff --check` pass.

## Blocked by

None.

## User stories covered

1, 5, 6

## LDD Traceability

- Parent PRD: `docs/tickets/LDD-0003-tracker-readiness-guided-next/prd.md`
- Parent SDD: `docs/tickets/LDD-0003-tracker-readiness-guided-next/sdd.md`
- Plan: `docs/tickets/LDD-0003-tracker-readiness-guided-next/plan.md`
- Plan slice: `Slice 4: Shared-understanding guardrails and validation`
- Ledger: `docs/tickets/LDD-0003-tracker-readiness-guided-next/children/LDD-0003-004-shared-understanding-guardrails/ledger.yml`

