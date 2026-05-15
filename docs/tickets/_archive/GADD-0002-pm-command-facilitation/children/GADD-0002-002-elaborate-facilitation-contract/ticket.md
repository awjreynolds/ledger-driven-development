# Add elaborate facilitation contract

## Parent

GADD-0002 - Strengthen GADD PM command facilitation

## What to build

Update `/gadd:elaborate` so it guides product detail inside existing scope. It must preserve scoped goals/non-goals, offer interaction modes, reject scope expansion, and keep draft acceptance criteria product-facing.

Expected touch point:

- `skills/gadd-elaborate/SKILL.md`

## Acceptance criteria

- `/gadd:elaborate` includes Guided, Context dump, and Best guess modes.
- `/gadd:elaborate` includes a product-detail quality bar that rejects scope expansion and implementation-specific criteria.
- `/gadd:elaborate` defines core product-detail questions for problem, users, stories, draft criteria, draft metrics, and open questions.
- `/gadd:elaborate` ends with an explicit exit gate that routes to `/gadd:refine` or back to `/gadd:scope`.
- `git diff --check` passes for the changed file.

## Blocked by

GADD-0002-001.

## User stories covered

2, 3, 4, 5

## GADD Traceability

- Parent PRD: `docs/tickets/GADD-0002-pm-command-facilitation/prd.md`
- Parent SDD: `docs/tickets/GADD-0002-pm-command-facilitation/sdd.md`
- Plan: `docs/tickets/GADD-0002-pm-command-facilitation/plan.md`
- Plan slice: `2. Elaborate facilitation and product-detail contract`
- Ledger: `docs/tickets/GADD-0002-pm-command-facilitation/children/GADD-0002-002-elaborate-facilitation-contract/ledger.yml`
