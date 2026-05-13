# Add scope facilitation contract

## Parent

LDD-0002 - Strengthen LDD PM command facilitation

## What to build

Update `/ldd:scope` so it is a guided Product Manager scoping workflow, not just an ownership checklist. It must explain new-draft behavior, duplicate-draft handling, interaction modes, scope quality bar, and exit gate.

Expected touch point:

- `skills/ldd-scope/SKILL.md`

## Acceptance criteria

- `/ldd:scope` states that promoted Product Requirement tickets do not block new scoping work.
- `/ldd:scope` explains that a new draft is created when no active draft exists.
- `/ldd:scope` stops when an active draft already exists and asks the user to resolve it before creating another.
- `/ldd:scope` includes Guided, Context dump, and Best guess modes.
- `/ldd:scope` includes a scope-specific product quality bar and exit gate.
- `git diff --check` passes for the changed file.

## Blocked by

None.

## User stories covered

1, 2, 3, 5, 6

## LDD Traceability

- Parent PRD: `docs/tickets/LDD-0002-pm-command-facilitation/prd.md`
- Parent SDD: `docs/tickets/LDD-0002-pm-command-facilitation/sdd.md`
- Plan: `docs/tickets/LDD-0002-pm-command-facilitation/plan.md`
- Plan slice: `1. Scope facilitation and draft-start contract`
- Ledger: `docs/tickets/LDD-0002-pm-command-facilitation/children/LDD-0002-001-scope-facilitation-contract/ledger.yml`
