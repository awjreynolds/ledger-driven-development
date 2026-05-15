# Teach /gadd:next and /gadd:implement the verification gate

## Parent

GADD-0001 - Add GADD execution context and verification gate

## What to build

Update workflow navigation and implementation command rules so GADD routes implemented-but-unverified child work to `/gadd:verify`, and implementation completion never archives or externally closes child work directly.

Expected touch points:

- `skills/gadd-next/SKILL.md`
- `skills/gadd-implement/SKILL.md`
- Adapter files only if their thin-router text needs command list updates

## Acceptance criteria

- `/gadd:next` prioritizes child work with completed implementation evidence and unverified closure by reporting `/gadd:verify <child-ticket-id>`.
- `/gadd:next` can use `execution_context` when present and derive equivalent state when it is absent.
- `/gadd:implement` records implementation completion and verification-required closure state, but does not archive or externally close the child work item.
- Rules explicitly preserve the approved PRD, SDD, and plan boundaries.
- `./scripts/validate-gadd-mvp.sh` and `git diff --check` pass.

## Blocked by

- GADD-0001-001
- GADD-0001-002

## User stories covered

1, 2, 3, 5

## GADD Traceability

- Parent PRD: `docs/tickets/_archive/GADD-0001-verify-context-header/prd.md`
- Parent SDD: `docs/tickets/_archive/GADD-0001-verify-context-header/sdd.md`
- Plan: `docs/tickets/_archive/GADD-0001-verify-context-header/plan.md`
- Plan slice: `3. Teach /gadd:next and /gadd:implement the verification gate`
- Ledger: `docs/tickets/_archive/GADD-0001-003-next-implement-verify-gate/ledger.yml`
