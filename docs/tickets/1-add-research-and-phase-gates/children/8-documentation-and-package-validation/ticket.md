# SDD #2 Slice 6: Documentation and package validation (#8)

## Parent

PRD #1 Add GADD research and phase input gates; SDD #2.

## What to build

Update user-facing docs, glossary, design spec, and validation checks so research, gates, privacy, and tracker-native child work behavior are documented and enforced.

## Acceptance criteria

- [ ] README, GEMINI, CONTEXT, and package design docs describe `/gadd:research`, input gates, privacy boundaries, and tracker-native child work projection.
- [ ] `scripts/validate-gadd-mvp.sh` enforces the new command surface, templates, readiness labels, phase gates, and GitHub sub-issue hierarchy contract.
- [ ] `./scripts/validate-gadd-mvp.sh` and `git diff --check` pass.

## Blocked by

#3, #4, #5, #6, and #7.

## User stories covered

1, 2, 3, 4, 5

## GADD Traceability

- Parent PRD: `docs/tickets/1-add-research-and-phase-gates/prd.md`
- Parent PRD issue: #1
- SDD issue: #2
- Tracker parent relationship: Native GitHub sub-issue of #2 verified during `/gadd:decompose`
- Plan: `docs/tickets/1-add-research-and-phase-gates/plan.md`
- Plan slice: 6. Documentation and package validation
- Ledger: `docs/tickets/1-add-research-and-phase-gates/children/8-documentation-and-package-validation/ledger.yml`
- Canonical state: repo-local ledger
