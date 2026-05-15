---
name: ldd-plan
description: Run /ldd:plan for an LDD ticket. Use when the user says /ldd:plan or wants an implementation plan and generated plan.html from an approved LDD SDD.
---

# /ldd:plan

Create or update `plan.md` and generated `plan.html` in the promoted ticket directory.

## Reads

- merged PRD
- SDD
- relevant ADRs
- GitNexus code-intelligence context when available and relevant

## Plan Must Include

- PRD summary
- SDD summary
- ADR summary and links
- implementation slices
- acceptance criteria traceability
- files / modules expected to change
- documentation impact by slice
- test strategy
- review checklist
- planned vertical slices for later `/ldd:decompose`

## Input Quality Gate

Required input standard before writing a plan:

- approved PRD and approved SDD in the ledger
- SDD decisions trace to PRD acceptance criteria
- no new architecture decision discovered during planning
- enough design detail to create traceable vertical slices

If inputs fail this standard, write nothing and name the blocking gap. The earliest LDD command that can repair missing or wrong design input is `/ldd:design`; missing product approval routes to `/ldd:approve <ticket-id>` or the owning Product Manager command.

## Rules

- Repo-local ledger is canonical. External trackers are optional sync/review surfaces.
- External mutations require human confirmation.
- Use the plan template's traceability and review checklist as mandatory completion criteria.
- GitNexus is strongly recommended for expected files/modules, slice boundaries, dependency order, and review-load estimates when code reality matters. If GitNexus is unavailable, stale, unindexed, or outside the configured related repositories, continue with normal inspection and record the limitation when it affects the plan.
- The plan may define vertical slices, but child tickets are created by `/ldd:decompose`.
- Do not introduce new architectural decisions. If planning discovers one, stop and return to `/ldd:design`.
- `plan.md` is the durable source; `plan.html` is generated from it.
- Commit locally after planning.
- Stop at explicit plan approval through `/ldd:approve <ticket-id>`.
- After writing the plan, set `execution_context.current_gate: plan_review`, `execution_context.next_command: /ldd:approve <ticket-id>`, and `execution_context.next_human_action: /ldd:approve <ticket-id>`.
- `/ldd:decompose` must not be the next command until `/ldd:approve <ticket-id>` has approved the plan.
- In GitHub tracker mode, use `.ldd/templates/pr-body-sdd-plan.md` as a managed PR projection for review; ask before creating or updating it and stop on external drift.
- SDD/Plan PR reviewer prompt: "Does this design and plan correctly implement the PRD? If yes, run `/ldd:approve <ticket-id>`."

## Stop Conditions

- missing SDD
- planning discovers a new architecture decision
- slices cannot trace to acceptance criteria
