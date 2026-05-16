# SDD #2 Slice 1: Research command surface (#3)

## Parent

PRD #1 Add GADD research and phase input gates; SDD #2.

## What to build

Add `/gadd:research` across the package surface so it is discoverable and installable in Codex, Claude, and Gemini. Include the canonical skill, OpenAI metadata, Claude/Gemini adapters, manifests, and command documentation.

## Acceptance criteria

- [ ] `/gadd:research` exists as a canonical skill and adapter-routed command.
- [ ] Codex/OpenAI, Claude, and Gemini package manifests expose `/gadd:research` consistently.
- [ ] `./scripts/validate-gadd-mvp.sh` checks the new command surface.

## Blocked by

None.

## User stories covered

1, 2

## GADD Traceability

- Parent PRD: `gadd/work-items/1-add-research-and-phase-gates/prd.md`
- Parent PRD issue: #1
- SDD issue: #2
- Tracker parent relationship: Native GitHub sub-issue of #2 verified during `/gadd:decompose`
- Plan: `gadd/work-items/1-add-research-and-phase-gates/plan.md`
- Plan slice: 1. Research command surface
- Ledger: `gadd/work-items/1-add-research-and-phase-gates/children/3-research-command-surface/ledger.yml`
- Canonical state: repo-local ledger
