---
name: ldd-research
description: Run /ldd:research before LDD scoping when inputs are weak, sensitive, or need codebase investigation. Use when the user says /ldd:research or wants to gather PM-grade inputs before a PRD.
---

# /ldd:research

Gather PM-grade inputs before PRD scoping and write a sanitized `research.md` artifact.

This command is a standalone, agent-agnostic LDD command. Follow this file directly; do not require any other installed skill.

## Input

```text
/ldd:research [new|draft-id|ticket-id] [trigger or context]
```

If no trigger, draft, ticket, or context source is provided, ask one direct question for the source product trigger or context. Do not invent a product problem from repository structure alone.

## Reads

- repository files, docs, ADRs, and existing LDD artifacts with full read-only visibility
- human-supplied private/local PM context when explicitly provided
- `.ldd/config.yml` and ledger state when a draft or ticket is selected
- prior research, PRD, SDD, plan, or child artifacts when present

Research may inspect code and local context to discover codebase facts, constraints, comparable behavior, and open questions. It must not mutate code, GitHub, or non-research artifacts.

## Produces

- `research.md` in the draft or ticket directory
- optional `artifacts.research.path/status` ledger state when a ledger is available
- compact ledger event: `research_completed`, `research_blocked`, `research_split_recommended`, or `research_not_product_requirement`

## Input Quality Gate

Required input standard before writing research:

- a source trigger, user request, stakeholder note, support signal, operational problem, or comparable context source
- enough human-accessible context to investigate at least the target users or workflow, the problem evidence, or the desired outcome
- an explicit sensitivity classification when private, commercial, customer, or financially sensitive context is supplied

If the input does not meet this standard, write nothing and ask for the missing source/context. The earliest LDD command that can repair this gap is still `/ldd:research`; if the request is clearly not product work, stop and report `not_a_product_requirement`.

## Standard PM Inputs

Research prompts for these standard PM inputs before declaring scope readiness.

Prompt for, infer from supplied context, or mark missing:

1. Source trigger or request
2. Target users, personas, or stakeholders
3. Problem evidence
4. Current workflow
5. Desired outcome
6. Product importance
7. Known constraints
8. Prior context
9. Comparable behavior
10. Candidate non-goals
11. Open questions

## Research Output Contract

Write `research.md` using the installed template when present. The shareable research output must separate:

- Research Summary
- Expected PM Inputs
- Evidence
- Current Workflow
- Users / Stakeholders
- Desired Outcomes
- Constraints
- Codebase Facts
- Assumptions
- Risks
- Sensitivity Handling
- Open Questions
- Readiness Decision

Research is not product scope. Do not write PRD goals, non-goals, user stories, acceptance criteria, metrics, software design, implementation plans, decomposition, tests, verification decisions, or closure decisions.

## Readiness Decision

Choose exactly one readiness label:

- `ready_for_scope`: the sanitized findings are sufficient for `/ldd:scope`
- `blocked_on_more_input`: a missing PM input prevents responsible scoping
- `split_recommended`: the trigger contains multiple Product Requirements that should be scoped separately
- `not_a_product_requirement`: the request should not enter the LDD PRD workflow

Every readiness decision must include the recommended next command or stop reason. When commandable, print a copyable command block.

## Sensitivity Boundary

Private/local context may inform research, but committed and GitHub-visible artifacts must contain only sanitized conclusions.

- Public/shareable inputs may be summarized normally.
- Internal/private inputs may be summarized only as conclusions needed for product decisions.
- Financially sensitive, customer-identifying, secret, revenue, budget, or commercial material must not be quoted, copied, named, or written as raw values.
- Record redaction notes that describe the class of omitted material and the safe implication used.
- If sanitization removes too much evidence to justify scoping, set readiness to `blocked_on_more_input` and ask the human for a shareable summary or permission to proceed with explicit assumptions.

## Workflow

1. Resolve or create the draft/ticket directory when requested. If no directory context is available, prepare research content and ask where to store it.
2. Read the repo, docs, artifacts, and supplied private/local context read-only.
3. Classify input sensitivity before drafting any committed output.
4. Fill `research.md` with sanitized evidence, codebase facts, assumptions, risks, and open questions.
5. Choose one readiness decision.
6. Update optional ledger research fields and execution context when a ledger is available:
   - `artifacts.research.path`
   - `artifacts.research.status`
   - `execution_context.phase: research`
   - `execution_context.current_gate: research`
   - `execution_context.next_command` to `/ldd:scope <draft-id-or-ticket-id>` only for `ready_for_scope`
7. Report the readiness decision, artifact path, redaction notes, and next command or stop reason.

## Rules

- Repo-local ledger is canonical. External trackers are optional sync/review surfaces.
- External mutations require human confirmation.
- Research has full read-only repository, documentation, LDD artifact, and human-supplied private/local context visibility.
- Research may write only sanitized `research.md` and ledger research state.
- Do not mutate GitHub, create PRDs, approve artifacts, write design, write plans, decompose, implement, verify, close, or archive work.
- Do not store raw private, customer, revenue, budget, financial, or commercial detail in committed artifacts.
- Scope remains owned by `/ldd:scope`; research only says whether scoping is ready and why.

## Stop Conditions

- no product trigger or context source is available
- private input cannot be safely sanitized into a committed artifact
- the work is not a Product Requirement
- the trigger should be split before scoping
- requested output would require PRD scope, engineering design, planning, implementation, verification, closure, or external mutation
