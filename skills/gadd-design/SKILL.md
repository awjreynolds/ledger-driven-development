---
name: gadd-design
description: Run /gadd:design for a GADD ticket. Use when the user says /gadd:design or wants an SDD and ADR check from an approved GADD PRD.
---

# /gadd:design

Create or update `sdd.md` in the promoted ticket directory.

## Reads

- merged PRD
- relevant code
- existing ADRs under configured ADR directory
- GitNexus code-intelligence context when available and relevant

## Produces

- Software Design Document
- ADR creates/updates only when the strict ADR threshold is met
- required SDD `## Structure` header-file summary synchronized with the detailed design

## Input Quality Gate

Required input standard before writing design:

- approved PRD in the parent ledger
- readable code, docs, and ADR context needed to ground engineering design
- no contradiction between code reality and approved product scope
- no unresolved product question that would change goals, non-goals, or acceptance criteria

If inputs fail this standard, write nothing and name the blocking gap. The earliest GADD command that can repair a product gap is `/gadd:refine`, `/gadd:scope`, or `/gadd:research` depending on the missing input; code/design uncertainty remains in `/gadd:design` until it requires an ADR or PRD change.

## Exit Gate

After writing the SDD, stop at explicit SDD approval:

- Set `artifacts.sdd.status: draft`.
- Set `execution_context.current_gate: design_review`.
- Set `execution_context.next_command: /gadd:approve <ticket-id>`.
- Set `execution_context.next_human_action: /gadd:approve <ticket-id>`.
- Use this reviewer prompt: "Is this design ready for implementation planning? If yes, run `/gadd:approve <ticket-id>`."

## Rules

- Repo-local ledger is canonical. External trackers are optional sync/review surfaces.
- External mutations require human confirmation.
- SE-hat command: existing code and ADRs may shape implementation design.
- GitNexus is strongly recommended before deciding affected repos, systems, SDD boundaries, cross-repo sequencing, or contract risks. If GitNexus is unavailable, stale, unindexed, or outside the configured related repositories, continue with normal code inspection and record the limitation in the SDD.
- Use GitNexus findings as design evidence, not canonical workflow state. Record indexed repositories considered, freshness or staleness notes, affected repos/systems, and any limitations that materially affect design confidence.
- Use the SDD template's quality bar before committing design output.
- Always write or update `## Structure` as the first content section of the SDD. Treat it as the SDD's header-file summary: concise enough to skim, concrete enough to reveal the design shape.
- Always keep it synchronized with `Decision Summary`, `Proposed Design`, `Data Flow / Control Flow`, and `Interfaces / Contracts`. If the design changes components, boundaries, interfaces, flow, or explicit non-changes, update `## Structure` in the same edit.
- Do not use `## Structure` as a second PRD, implementation plan, or separate design authority. It summarizes the detailed SDD; it does not replace it.
- The PRD still owns product scope. If code reality contradicts the PRD, stop and return to the earliest affected Product Manager step.
- ADR threshold: hard to reverse, surprising without context, and the result of a real trade-off.
- Mandatory ADR support does not mean mandatory ADR creation.
- Commit locally after design. Do not push/update PRs unless explicitly approved.
- SDD approval must be recorded through `/gadd:approve <ticket-id>`, not conversational shorthand.
- In GitHub tracker mode, prepare SDD/plan review PR content only as a managed projection and ask for explicit human confirmation before any PR create or update.
- GitHub PRs are the first external review surface for SDD/plan review; Linear and Jira review surfaces are follow-on and optional.

## Stop Conditions

- PRD not approved
- code reality contradicts PRD
- ADR-worthy decision cannot be resolved
