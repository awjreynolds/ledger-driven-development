---
ticket: 2026-05-14-add-research-and-phase-gates
title: "Add LDD research and phase input gates"
created: 2026-05-14
updated: 2026-05-14
---

# PRD: Add LDD research and phase input gates

<!--
Product Manager artifact. Describe the product need and acceptance boundary.
Do not use the codebase as design input. Do not include implementation choices,
architecture, file paths, APIs, schemas, libraries, test strategy, or code snippets.
Capture technical uncertainty only as a dependency, constraint, or open question.
-->

## Problem

Not yet elaborated. `/ldd:scope` only defines the product boundary for this draft.

## Goals

- Add a first-class LDD research phase that gathers PM-grade inputs before PRD scoping when the source context is weak, sensitive, or needs codebase investigation.
- Ensure the research phase can use full read-only visibility into the repository and relevant local context while recording findings as evidence, constraints, risks, assumptions, or open questions rather than product scope or design decisions.
- Add input-quality gates across LDD phases so each command validates that its approved or source inputs meet that phase's standard before producing or mutating its artifact.
- Strengthen `/ldd:scope` so it checks whether supplied inputs are good enough to define a useful product boundary, and routes to research or asks for missing source context when they are not.
- Preserve sensitive private PM inputs, including financially sensitive context, by allowing research to consume private/local context while committing only sanitized, shareable conclusions to repo and GitHub-visible artifacts.
- Use this Product Requirement to validate the configured GitHub projection path while preserving the repo-local ledger as canonical state.

## Non-goals

- Do not make GitHub the canonical source of LDD workflow state.
- Do not mutate GitHub from `/ldd:scope`; external tracker mutation remains gated by explicit human confirmation and the owning LDD command.
- Do not add Linear or Jira projection behavior as part of this Product Requirement.
- Do not store raw financially sensitive inputs, customer names, revenue figures, budgets, or private commercial notes in committed artifacts or GitHub-visible projections.
- Do not let research outputs prescribe architecture, command algorithms, file placement, schemas, implementation sequencing, or tests.
- Do not collapse research, scoping, elaboration, refinement, design, planning, implementation, and verification into a single monolithic command.

## Users / Personas

Not yet elaborated.

## User Stories

Not yet elaborated.

## Acceptance Criteria

Not yet refined.

## Success Metrics

Not yet refined.

## Dependencies

- The repository is configured for GitHub projection in `.ldd/config.yml`, with repo-local ledgers remaining canonical.
- External GitHub mutations require explicit human confirmation and drift checks.
- `/ldd:research` needs a clear sensitivity boundary between private intake material and shareable repo/GitHub artifacts.
- Existing LDD command boundaries must be preserved: PM commands own product inputs and scope, design owns engineering translation, plan owns executable slices, implementation owns child work, verification and close own closure readiness and closure.
- Phase gates should reject poor inputs and route to the earliest phase that can fix them rather than silently inventing missing context.

## Open Questions

- Non-blocking for scope: What exact readiness labels should `/ldd:research` use for input quality and next routing?
- Non-blocking for scope: Should private research intake live only in project context/pasted notes, or should LDD also define a gitignored local private folder convention?
- Non-blocking for scope: Which downstream phase gates need full behavior changes in the first implementation slice versus a shared contract update?
- Non-blocking for scope: What GitHub projection action should validate the integration after PRD approval: creating the Product Requirement issue, opening a PRD PR, or both?

## PRD Handoff Checklist

<!-- Complete before opening the PRD PR. -->

- [ ] Problem is expressed from the user's perspective.
- [x] Goals and non-goals make the scope boundary clear.
- [ ] User stories cover the main workflow and meaningful user-visible edge cases.
- [ ] Acceptance criteria are observable without reading code.
- [ ] Metrics define how product success will be judged.
- [x] Dependencies and open questions are explicit.
- [x] No implementation decisions, architecture, file paths, APIs, schemas, libraries, test strategy, or code snippets are present.
