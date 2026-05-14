# SDD #2 Slice 4: Scope adequacy gate and PM command gates (#6)

## Parent

PRD #1 Add LDD research and phase input gates; SDD #2.

## What to build

Make `/ldd:scope` reject weak inputs before writing scope, and add PM-phase input quality gates to scope, elaborate, and refine.

## Acceptance criteria

- [ ] `/ldd:scope` refuses to create/update goals and non-goals without a clear problem or desired outcome.
- [ ] Weak source inputs route to `/ldd:research` or one decisive missing-context question.
- [ ] PM commands state required input standards and earliest fixing commands.
- [ ] PM commands still avoid codebase reads as design input.

## Blocked by

#5.

## User stories covered

1, 4

## LDD Traceability

- Parent PRD: `docs/tickets/1-add-research-and-phase-gates/prd.md`
- Parent PRD issue: #1
- SDD issue: #2
- Tracker parent relationship: Native GitHub sub-issue of #2 verified during `/ldd:decompose`
- Plan: `docs/tickets/1-add-research-and-phase-gates/plan.md`
- Plan slice: 4. Scope adequacy gate and PM command gates
- Ledger: `docs/tickets/1-add-research-and-phase-gates/children/6-scope-adequacy-gate-and-pm-command-gates/ledger.yml`
- Canonical state: repo-local ledger
