---
work item: GADD-0002
title: "Strengthen GADD PM command facilitation"
created: 2026-05-13
updated: 2026-05-13
status: approved
---

# PRD: Strengthen GADD PM command facilitation

<!--
Product Manager artifact. Describe the product need and acceptance boundary.
Do not use the codebase as design input. Do not include implementation choices,
architecture, file paths, APIs, schemas, libraries, test strategy, or code snippets.
Capture technical uncertainty only as a dependency, constraint, or open question.
-->

## Problem

The GADD Product Manager commands currently express the right ownership boundaries, but they do not yet give agents enough operating guidance to run a dependable PM conversation. A user can ask for scope, elaboration, or refinement, but the command may behave like a static checklist instead of guiding the user through ambiguity, preserving assumptions, and ending with a clear handoff decision.

This creates friction during dogfooding. Product work can stall when `/gadd:scope` cannot start a new Product Requirement from source context, or drift when an agent tries to fill missing product detail by smuggling in technical design. It also makes handoffs weaker because the next command, unresolved questions, and required human decision are not always explicit.

## Goals

- Make `/gadd:scope`, `/gadd:elaborate`, and `/gadd:refine` stronger guided Product Manager workflows, not just thin ownership checklists.
- Preserve GADD's Product Manager boundary: product-scope commands must not smuggle in technical design, implementation mechanics, or codebase-derived design decisions.
- Add a self-contained PM facilitation protocol to the three commands so they can guide users through ambiguity without depending on external skills.
- Support starting a new draft Product Requirement from source context when no active draft exists, even if other promoted Work Items are still in later workflow phases.
- Make each PM command end with an explicit handoff gate that states the updated artifact, unresolved questions, recommended next GADD command, and human decision needed.

## Non-goals

- Do not add a required dependency on external PM, facilitation, grill, or orchestration skills.
- Do not merge `/gadd:scope`, `/gadd:elaborate`, and `/gadd:refine` into a single monolithic PRD command.
- Do not change downstream engineering ownership for `/gadd:design`, `/gadd:plan`, `/gadd:decompose`, `/gadd:implement`, or `/gadd:verify`.
- Do not introduce duplicate workflow state such as `progress.md`, session logs, or global ledgers.
- Do not let an incomplete promoted Work Item block creation of a separate new draft Product Requirement.
- Do not make `/gadd:scope` mutate a promoted Work Item unless the user explicitly identifies that Work Item.

## Users / Personas

- Product author - needs the PM commands to turn rough context into a clean Product Requirement without forcing them to know the GADD workflow internals.
- Product reviewer - needs confidence that scope, elaboration, and refinement preserve product intent without adding hidden design or implementation decisions.
- Agent running a GADD PM command - needs enough self-contained guidance to ask focused questions, label assumptions, and stop at the correct handoff boundary.
- Maintainer dogfooding GADD - needs new Product Requirement drafts to start cleanly while other promoted Work Items continue through later workflow phases.

## User Stories

1. As a product author, I want `/gadd:scope` to start a new draft Product Requirement from source context when no active draft exists, so that new product work is not blocked by unrelated promoted Work Items.
2. As a product author, I want the PM commands to offer guided, context-dump, and best-guess modes, so that I can choose the right level of interaction for the situation.
3. As an agent running a GADD PM command, I want a self-contained facilitation protocol, so that I can ask focused questions, preserve assumptions, and avoid relying on external skills.
4. As a product reviewer, I want scope, elaboration, and refinement to reject solution-smuggling language, so that engineering design starts from product outcomes rather than hidden implementation choices.
5. As a maintainer, I want each PM command to end with an explicit handoff gate, so that the next GADD action and required human decision are visible from the artifact state.
6. As a maintainer dogfooding GADD, I want incomplete promoted Work Items to remain separate from new draft Product Requirements, so that parallel product discovery does not corrupt active workflow records.

## Acceptance Criteria

- [ ] A user can start new scoping work from source context when no active draft exists, even if an unrelated promoted Work Item is incomplete.
- [ ] New scoping work does not mutate a promoted Work Item unless the user explicitly identifies that Work Item.
- [ ] If a user tries to start new scoping work while an active draft already exists, GADD asks the user to continue, promote, rename, or discard the existing draft before creating another draft.
- [ ] The PM commands provide a self-contained guided interaction pattern that does not require external PM, facilitation, grill, or orchestration skills.
- [ ] The PM commands offer guided, context-dump, and best-guess modes, and make assumptions visible when best-guess mode is used.
- [ ] The PM commands preserve their ownership boundaries: `/gadd:scope` owns goals and non-goals, `/gadd:elaborate` owns product detail, and `/gadd:refine` owns handoff quality.
- [ ] Product-facing acceptance criteria avoid prescribing technical design, implementation sequence, internal schemas, or command mechanics unless those details are explicitly part of the product requirement.
- [ ] Each PM command ends by stating whether the artifact is ready for the next GADD command, whether a return to an earlier PM command is required, or whether a human decision blocks progress.
- [ ] GADD continues to use repo-local ledgers as canonical workflow state and does not introduce duplicate progress logs, session logs, or global workflow state.

```gherkin
Scenario: New scope starts while another promoted Work Item is incomplete
  Given an unrelated promoted Product Requirement is still active
  And no draft Product Requirement is active
  When a user starts new scoping work from source context
  Then GADD creates a new draft Product Requirement
  And the unrelated promoted Work Item remains unchanged
```

```gherkin
Scenario: Existing active draft blocks accidental duplicate scoping
  Given an active draft Product Requirement already exists
  When a user starts another new scope without identifying a different target
  Then GADD asks the user to resolve the existing draft first
  And no second active draft is created automatically
```

```gherkin
Scenario: Product Manager command reaches a handoff gate
  Given a Product Manager command updates its owned PRD sections
  When the command finishes
  Then it states the updated artifact, unresolved product questions, recommended next GADD command, and required human decision
```

## Success Metrics

- A maintainer can start a new PM-command Product Requirement while another promoted Work Item remains in verification, without modifying the promoted Work Item.
- A reviewer can identify the next recommended GADD command and required human decision from the draft ledger and PRD in under two minutes without relying on chat history.
- The refined Product Requirement contains zero acceptance criteria that require codebase inspection to understand.
- Dogfooding sessions for `/gadd:scope`, `/gadd:elaborate`, and `/gadd:refine` have no recurring confusion about whether incomplete promoted Work Items block new draft scoping.
- Product reviewers can answer "Is this ready for engineering design?" from the PRD without asking which PM command owns each remaining question.

## Dependencies

- GADD skills must remain standalone and agent-agnostic.
- Repo-local ledger state remains canonical; external trackers stay optional review and sync surfaces.
- The existing scope/elaborate/refine research update is the source context for this Product Requirement.
- Scope must preserve the GADD distinction between Product Requirement drafts and promoted Work Item workflow records.
- The active `GADD-0001` Work Item is still in verification and should not be modified by this new Product Requirement.

## Open Questions

- Resolved: The minimum facilitation protocol should include command boundary, guided/context-dump/best-guess entry modes, one-question-at-a-time ambiguity handling, visible assumptions, phase-appropriate anti-pattern checks, and an explicit exit gate.
- Resolved: `Guided`, `Context dump`, and `Best guess` should be exposed consistently across all three PM commands, while each command keeps phase-specific questions and quality checks.
- Resolved: `/gadd:scope` should create a human-readable draft slug from the source context and block duplicate active drafts by asking the user to resolve the existing draft first.
- Resolved: PM commands should share the same exit-gate shape, but the wording should name the phase-specific next command or return path.
- Resolved: A blocking product ambiguity is one that changes goals, non-goals, users, acceptance boundary, rollout confidence, or whether the work belongs in the current PM command. Other missing detail may be labeled as an assumption or passed to the next GADD phase with an owner.

## PRD Handoff Checklist

<!-- Complete before opening the PRD PR. -->

- [x] Problem is expressed from the user's perspective.
- [x] Goals and non-goals make the scope boundary clear.
- [x] User stories cover the main workflow and meaningful user-visible edge cases.
- [x] Acceptance criteria are observable without reading code.
- [x] Metrics define how product success will be judged.
- [x] Dependencies and open questions are explicit.
- [x] No implementation decisions, architecture, file paths, APIs, schemas, libraries, test strategy, or code snippets are present.
