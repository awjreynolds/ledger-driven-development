# SDD #2 Slice 5: Downstream phase gates and GitHub hierarchy safeguards (#7)

## Parent

PRD #1 Add LDD research and phase input gates; SDD #2.

## What to build

Add input gates to downstream LDD commands and enforce the GitHub hierarchy: PRD issue #1 -> SDD issue #2 -> native implementation sub-issues.

## Acceptance criteria

- [ ] Design, plan, decompose, implement, verify, close, approve, next, and setup state their input standards and reject behavior.
- [ ] Plan approval routes through `/ldd:approve` before decomposition.
- [ ] GitHub decomposition creates native sub-issues under the approved SDD issue when supported, with body traceability as backup.
- [ ] Validation catches missing gate language and hierarchy safeguards.

## Blocked by

#6.

## User stories covered

4, 5

## LDD Traceability

- Parent PRD: `docs/tickets/1-add-research-and-phase-gates/prd.md`
- Parent PRD issue: #1
- SDD issue: #2
- Tracker parent relationship: Native GitHub sub-issue of #2 verified during `/ldd:decompose`
- Plan: `docs/tickets/1-add-research-and-phase-gates/plan.md`
- Plan slice: 5. Downstream phase gates and GitHub hierarchy safeguards
- Ledger: `docs/tickets/1-add-research-and-phase-gates/children/7-downstream-phase-gates-and-github-hierarchy-safeguards/ledger.yml`
- Canonical state: repo-local ledger
