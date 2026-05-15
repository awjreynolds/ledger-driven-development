# Update docs and validation for end-to-end workflow

## Parent

GADD-0001 - Add GADD execution context and verification gate

## What to build

Update public docs, glossary, MVP design notes, validation checks, and the active GADD ledger state so the full scope/design/plan/decompose/implement/verify path is documented and enforceable.

Expected touch points:

- `README.md`
- `CONTEXT.md`
- `docs/superpowers/specs/2026-05-12-local-ledger-mvp-design.md`
- `docs/tickets/_archive/GADD-0001-verify-context-header/ledger.yml`
- `scripts/validate-gadd-mvp.sh`

## Acceptance criteria

- Public docs show `/gadd:verify` as part of the MVP workflow after implementation and before closure/archive.
- Glossary terms and relationships cover execution context, verification, closure, and verified child work.
- MVP design notes reflect the new verification gate without introducing a global ledger, `progress.md`, or external sync engine.
- Validation enforces the new command package surface and key child-ticket closure language.
- Active GADD ledger state remains consistent with completed child work and the next required gate.
- `./scripts/validate-gadd-mvp.sh`, `git diff --check`, and a `/gadd:next` sanity check pass.

## Blocked by

- GADD-0001-001
- GADD-0001-002
- GADD-0001-003
- GADD-0001-004

## User stories covered

1, 2, 3, 4, 5

## GADD Traceability

- Parent PRD: `docs/tickets/_archive/GADD-0001-verify-context-header/prd.md`
- Parent SDD: `docs/tickets/_archive/GADD-0001-verify-context-header/sdd.md`
- Plan: `docs/tickets/_archive/GADD-0001-verify-context-header/plan.md`
- Plan slice: `5. Update docs and validation for the new end-to-end workflow`
- Ledger: `docs/tickets/_archive/GADD-0001-005-docs-validation-workflow/ledger.yml`
