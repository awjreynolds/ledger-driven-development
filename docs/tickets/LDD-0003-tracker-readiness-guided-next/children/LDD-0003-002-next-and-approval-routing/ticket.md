# Guide /ldd:next and approval-routing gates

## Parent

LDD-0003 - Make LDD ready for external trackers and guided next actions

## What to build

Update the workflow command contracts so `/ldd:next` reports the next command and next human action, and PRD/SDD review gates route to `/ldd:approve <ticket-id>`.

Expected touch points:

- `skills/ldd-next/SKILL.md`
- `skills/ldd-refine/SKILL.md`
- `skills/ldd-design/SKILL.md`
- `skills/ldd-plan/SKILL.md`
- `skills/ldd-decompose/SKILL.md`
- `skills/ldd-implement/SKILL.md`
- `skills/ldd-verify/SKILL.md`
- `skills/ldd-close/SKILL.md`
- `scripts/validate-ldd-mvp.sh`

## Acceptance criteria

- `/ldd:next` reports both `next_command` and `next_human_action` when available.
- `/ldd:next` names `/ldd:approve <ticket-id>` for PRD and SDD approval gates.
- `/ldd:next` remains read-only and does not perform durable local or external mutations.
- Blocked states report the blocking decision or drift resolution required.
- Upstream commands set `next_human_action` when they stop at PRD or SDD approval gates.
- `bash scripts/validate-ldd-mvp.sh` and `git diff --check` pass.

## Blocked by

LDD-0003-001.

## User stories covered

5, 6, 7

## LDD Traceability

- Parent PRD: `docs/tickets/LDD-0003-tracker-readiness-guided-next/prd.md`
- Parent SDD: `docs/tickets/LDD-0003-tracker-readiness-guided-next/sdd.md`
- Plan: `docs/tickets/LDD-0003-tracker-readiness-guided-next/plan.md`
- Plan slice: `Slice 2: Guided /ldd:next and approval-routing gates`
- Ledger: `docs/tickets/LDD-0003-tracker-readiness-guided-next/children/LDD-0003-002-next-and-approval-routing/ledger.yml`

