---
name: ldd-core
description: Shared Ledger-Driven Development MVP rules for /ldd commands. Use whenever executing an /ldd:* command.
---

# Ledger-Driven Development Core Rules

GitHub is the ledger. LDD reads workflow state from GitHub Issues and Pull Requests, not from local progress logs, labels, generated audit files, or agent-session state.

## MVP Command Surface

- `/ldd:setup`
- `/ldd:next`
- `/ldd:scope`
- `/ldd:elaborate`
- `/ldd:refine`
- `/ldd:design`
- `/ldd:plan`
- `/ldd:implement`

## Human Control

LDD commands may make local repo changes when explicitly invoked:

- create or switch to the matching `ldd/...` branch for the active issue and phase
- edit artifacts
- generate `plan.html`
- create local commits

GitHub mutations require human confirmation:

- pushing a branch
- opening or updating a PR
- commenting on an issue or PR
- requesting reviewers
- closing an issue

## Requirements / Code Influence Boundary

PM-hat commands (`/ldd:scope`, `/ldd:elaborate`, `/ldd:refine`) must not read the codebase as a design input. If code knowledge appears during PM work, capture it only as a dependency, constraint, or open question.

SE-hat commands (`/ldd:design`, `/ldd:plan`) may use the existing codebase. `/ldd:design` reads the merged PRD, relevant code, and ADRs. `/ldd:plan` reads the PRD, SDD, and ADRs and must not introduce new architecture decisions.

## Paths

- PRD: `docs/tickets/{issue}/prd.md`
- SDD: `docs/tickets/{issue}/sdd.md`
- Plan: `docs/tickets/{issue}/plan.md`
- Plan HTML: `docs/tickets/{issue}/plan.html`

## Branches

- PRD: `ldd/prd/{issue}`
- SDD/Plan: `ldd/sdd-plan/{issue}`
- Implementation: `ldd/impl/{issue}`

## Pull Requests

- PRD title: `PRD: {title}`
- SDD/Plan title: `SDD + Plan: {title}`
- Implementation title: `{title}`
- PRD and SDD/Plan bodies use `references #{issue}`
- Implementation body uses `Closes #{issue}`

## Forbidden In MVP

- LDD-specific phase labels, gate labels, PR labels, or issue-state labels
- generated `progress.md`
- generated audit event files
- automatic GitHub Actions for workflow state transitions
- backend abstraction beyond GitHub
