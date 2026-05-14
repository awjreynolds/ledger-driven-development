# SDD #2 Slice 3: Research workflow and privacy contract (#5)

## Parent

PRD #1 Add LDD research and phase input gates; SDD #2.

## What to build

Define the `/ldd:research` workflow: standard PM input prompts, full read-only code/docs/local context visibility, sanitized research output, and readiness labels.

## Acceptance criteria

- [ ] Research prompts for the standard PM inputs listed in the PRD.
- [ ] Research rules allow full read-only repository, documentation, artifact, and human-supplied private/local context visibility.
- [ ] Research output separates evidence, codebase facts, constraints, assumptions, risks, sensitivity handling, open questions, and one readiness label.
- [ ] Sensitive/private inputs are summarized only as sanitized implications with redaction notes.

## Blocked by

#3 and #4.

## User stories covered

1, 2, 3

## LDD Traceability

- Parent PRD: `docs/tickets/1-add-research-and-phase-gates/prd.md`
- Parent PRD issue: #1
- SDD issue: #2
- Tracker parent relationship: Native GitHub sub-issue of #2 verified during `/ldd:decompose`
- Plan: `docs/tickets/1-add-research-and-phase-gates/plan.md`
- Plan slice: 3. Research workflow and privacy contract
- Ledger: `docs/tickets/1-add-research-and-phase-gates/children/5-research-workflow-and-privacy-contract/ledger.yml`
- Canonical state: repo-local ledger
