# Add refine facilitation contract and evidence checks

## Parent

GADD-0002 - Strengthen GADD PM command facilitation

## What to build

Update `/gadd:refine` so it guides PRD handoff quality, owns acceptance criteria and metrics refinement, resolves or owns open questions, and ends with the PRD approval/promotion gate. Record targeted evidence that all three PM commands include the new facilitation contract.

Expected touch point:

- `skills/gadd-refine/SKILL.md`
- Child ledgers for implementation evidence

## Acceptance criteria

- `/gadd:refine` includes Guided, Context dump, and Best guess modes.
- `/gadd:refine` includes a handoff-quality bar for testable criteria, measurable metrics, owned questions, dependencies, and solution-smuggling cleanup.
- `/gadd:refine` includes explicit systematic checks before approval.
- `/gadd:refine` ends with the PRD approval/promotion gate.
- Targeted checks confirm all three PM skills include the facilitation protocol and exit gate.
- `git diff --check` passes.

## Blocked by

GADD-0002-001, GADD-0002-002.

## User stories covered

2, 3, 4, 5

## GADD Traceability

- Parent PRD: `docs/tickets/GADD-0002-pm-command-facilitation/prd.md`
- Parent SDD: `docs/tickets/GADD-0002-pm-command-facilitation/sdd.md`
- Plan: `docs/tickets/GADD-0002-pm-command-facilitation/plan.md`
- Plan slice: `3. Refine facilitation and handoff contract`
- Ledger: `docs/tickets/GADD-0002-pm-command-facilitation/children/GADD-0002-003-refine-facilitation-contract/ledger.yml`
