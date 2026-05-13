# Update docs and end-to-end validation

## Parent

LDD-0003 - Make LDD ready for external trackers and guided next actions

## What to build

Update the user-facing workflow docs and validation so the new approve command, GitHub-first readiness boundary, guided next-action behavior, and PM guardrails are visible and enforced.

Expected touch points:

- `README.md`
- `GEMINI.md`
- `CONTEXT.md`
- `scripts/validate-ldd-mvp.sh`
- `docs/tickets/LDD-0003-tracker-readiness-guided-next/verification.md`

## Acceptance criteria

- Command lists include `/ldd:approve`.
- Documentation explains that GitHub is first, Linear/Jira are follow-on, and local ledgers remain canonical.
- Documentation explains that `/ldd:next` reports next actions but does not mutate durable state.
- Documentation explains why PM commands require bounded shared understanding.
- Validation covers the new command surface and workflow contracts.
- `bash scripts/validate-ldd-mvp.sh` and `git diff --check` pass.

## Blocked by

LDD-0003-001, LDD-0003-002, LDD-0003-003, LDD-0003-004.

## User stories covered

1, 2, 3, 4, 5, 6, 7

## LDD Traceability

- Parent PRD: `docs/tickets/LDD-0003-tracker-readiness-guided-next/prd.md`
- Parent SDD: `docs/tickets/LDD-0003-tracker-readiness-guided-next/sdd.md`
- Plan: `docs/tickets/LDD-0003-tracker-readiness-guided-next/plan.md`
- Plan slice: `Slice 5: End-to-end docs and package verification`
- Ledger: `docs/tickets/LDD-0003-tracker-readiness-guided-next/children/LDD-0003-005-docs-and-validation/ledger.yml`

