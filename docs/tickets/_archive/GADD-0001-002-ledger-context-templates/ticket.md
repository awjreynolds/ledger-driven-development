# Add ledger execution context and verification templates

## Parent

GADD-0001 - Add GADD execution context and verification gate

## What to build

Extend the GADD ledger and setup templates so new target repositories receive the execution context/header, child verification state, closure state, and a reusable verification report template. Mirror those template changes into this repository's copied `.gadd/templates`.

Expected touch points:

- `skills/gadd-setup/assets/templates/ledger.yml`
- `skills/gadd-setup/assets/templates/verification.md`
- `.gadd/templates/ledger.yml`
- `.gadd/templates/verification.md`
- `skills/gadd-setup/SKILL.md`
- `README.md`
- `CONTEXT.md`

## Acceptance criteria

- Ledger templates include `execution_context` with phase, current gate, next command or human action, reason, approved artifacts, and boundaries.
- Child ledger shape includes verification artifact state and closure state.
- `verification.md` template exists in source setup templates and copied `.gadd/templates`.
- Setup documentation includes the verification template as an installed handoff artifact.
- Glossary/docs define execution context, verification, and closure without introducing global ledger state or `progress.md`.
- `./scripts/validate-gadd-mvp.sh` and `git diff --check` pass.

## Blocked by

None.

## User stories covered

1, 3, 4

## GADD Traceability

- Parent PRD: `docs/tickets/_archive/GADD-0001-verify-context-header/prd.md`
- Parent SDD: `docs/tickets/_archive/GADD-0001-verify-context-header/sdd.md`
- Plan: `docs/tickets/_archive/GADD-0001-verify-context-header/plan.md`
- Plan slice: `2. Add ledger execution context and verification templates`
- Ledger: `docs/tickets/_archive/GADD-0001-002-ledger-context-templates/ledger.yml`
