# Guide /gadd:next and approval-routing gates

## Parent

GADD-0003 - Make GADD ready for external trackers and guided next actions

## What to build

Update the workflow command contracts so `/gadd:next` reports the next command and next human action, and PRD/SDD review gates route to `/gadd:approve <work-item-id>`.

Expected touch points:

- `skills/gadd-next/SKILL.md`
- `skills/gadd-refine/SKILL.md`
- `skills/gadd-design/SKILL.md`
- `skills/gadd-plan/SKILL.md`
- `skills/gadd-decompose/SKILL.md`
- `skills/gadd-implement/SKILL.md`
- `skills/gadd-verify/SKILL.md`
- `skills/gadd-close/SKILL.md`
- `scripts/validate-gadd-mvp.sh`

## Acceptance criteria

- `/gadd:next` reports both `next_command` and `next_human_action` when available.
- `/gadd:next` names `/gadd:approve <work-item-id>` for PRD and SDD approval gates.
- `/gadd:next` remains read-only and does not perform durable local or external mutations.
- Blocked states report the blocking decision or drift resolution required.
- Upstream commands set `next_human_action` when they stop at PRD or SDD approval gates.
- `bash scripts/validate-gadd-mvp.sh` and `git diff --check` pass.

## Blocked by

GADD-0003-001.

## User stories covered

5, 6, 7

## GADD Traceability

- Parent PRD: `gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/prd.md`
- Parent SDD: `gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/sdd.md`
- Plan: `gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/plan.md`
- Plan slice: `Slice 2: Guided /gadd:next and approval-routing gates`
- Ledger: `gadd/work-items/_archive/GADD-0003-002-next-and-approval-routing/ledger.yml`

