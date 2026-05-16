# Define GitHub-first tracker projection contracts

## Parent

GADD-0003 - Make GADD ready for external trackers and guided next actions

## What to build

Make the GitHub-first external tracker boundary explicit in setup templates and command contracts. GitHub should be a managed projection surface, not canonical workflow state.

Expected touch points:

- `skills/gadd-setup/assets/templates/config.yml`
- `skills/gadd-setup/assets/templates/issue-body-prd.md`
- `skills/gadd-setup/assets/templates/issue-body-child.md`
- `skills/gadd-setup/assets/templates/pr-body-sdd-plan.md`
- `skills/gadd-setup/assets/templates/pr-body-implementation.md`
- Command skills that create, review, verify, or close work.
- `README.md`
- `CONTEXT.md`
- `scripts/validate-gadd-mvp.sh`

## Acceptance criteria

- GitHub is documented as the first external tracker dogfooding path.
- GitHub issues are the projection surface for PRD and child work.
- GitHub PRs are the projection surface for SDD/plan and implementation review.
- External tracker mutations require explicit human confirmation.
- External drift stops mutation before managed sections are updated.
- The repo-local ledger remains canonical.
- Linear and Jira are documented as follow-on optional collaboration surfaces.
- `bash scripts/validate-gadd-mvp.sh` and `git diff --check` pass.

## Blocked by

None.

## User stories covered

1, 2, 3, 4, 6

## GADD Traceability

- Parent PRD: `gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/prd.md`
- Parent SDD: `gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/sdd.md`
- Plan: `gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/plan.md`
- Plan slice: `Slice 3: GitHub-first tracker projection contracts`
- Ledger: `gadd/work-items/_archive/GADD-0003-003-github-projection-contracts/ledger.yml`

