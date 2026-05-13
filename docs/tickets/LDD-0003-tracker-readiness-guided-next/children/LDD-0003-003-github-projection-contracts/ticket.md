# Define GitHub-first tracker projection contracts

## Parent

LDD-0003 - Make LDD ready for external trackers and guided next actions

## What to build

Make the GitHub-first external tracker boundary explicit in setup templates and command contracts. GitHub should be a managed projection surface, not canonical workflow state.

Expected touch points:

- `skills/ldd-setup/assets/templates/config.yml`
- `skills/ldd-setup/assets/templates/issue-body-prd.md`
- `skills/ldd-setup/assets/templates/issue-body-child.md`
- `skills/ldd-setup/assets/templates/pr-body-sdd-plan.md`
- `skills/ldd-setup/assets/templates/pr-body-implementation.md`
- Command skills that create, review, verify, or close work.
- `README.md`
- `CONTEXT.md`
- `scripts/validate-ldd-mvp.sh`

## Acceptance criteria

- GitHub is documented as the first external tracker dogfooding path.
- GitHub issues are the projection surface for PRD and child work.
- GitHub PRs are the projection surface for SDD/plan and implementation review.
- External tracker mutations require explicit human confirmation.
- External drift stops mutation before managed sections are updated.
- The repo-local ledger remains canonical.
- Linear and Jira are documented as follow-on optional collaboration surfaces.
- `bash scripts/validate-ldd-mvp.sh` and `git diff --check` pass.

## Blocked by

None.

## User stories covered

1, 2, 3, 4, 6

## LDD Traceability

- Parent PRD: `docs/tickets/LDD-0003-tracker-readiness-guided-next/prd.md`
- Parent SDD: `docs/tickets/LDD-0003-tracker-readiness-guided-next/sdd.md`
- Plan: `docs/tickets/LDD-0003-tracker-readiness-guided-next/plan.md`
- Plan slice: `Slice 3: GitHub-first tracker projection contracts`
- Ledger: `docs/tickets/LDD-0003-tracker-readiness-guided-next/children/LDD-0003-003-github-projection-contracts/ledger.yml`

