# Add scope facilitation contract

## Parent

GADD-0002 - Strengthen GADD PM command facilitation

## What to build

Update `/gadd:scope` so it is a guided Product Manager scoping workflow, not just an ownership checklist. It must explain new-draft behavior, duplicate-draft handling, interaction modes, scope quality bar, and exit gate.

Expected touch point:

- `skills/gadd-scope/SKILL.md`

## Acceptance criteria

- `/gadd:scope` states that promoted Product Requirement Work Items do not block new scoping work.
- `/gadd:scope` explains that a new draft is created when no active draft exists.
- `/gadd:scope` stops when an active draft already exists and asks the user to resolve it before creating another.
- `/gadd:scope` includes Guided, Context dump, and Best guess modes.
- `/gadd:scope` includes a scope-specific product quality bar and exit gate.
- `git diff --check` passes for the changed file.

## Blocked by

None.

## User stories covered

1, 2, 3, 5, 6

## GADD Traceability

- Parent PRD: `gadd/work-items/GADD-0002-pm-command-facilitation/prd.md`
- Parent SDD: `gadd/work-items/GADD-0002-pm-command-facilitation/sdd.md`
- Plan: `gadd/work-items/GADD-0002-pm-command-facilitation/plan.md`
- Plan slice: `1. Scope facilitation and draft-start contract`
- Ledger: `gadd/work-items/GADD-0002-pm-command-facilitation/children/GADD-0002-001-scope-facilitation-contract/ledger.yml`
