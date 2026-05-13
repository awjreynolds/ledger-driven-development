---
ticket: 2026-05-13-pm-command-facilitation
title: "Strengthen LDD PM command facilitation"
created: 2026-05-13
updated: 2026-05-13
status: draft
---

# PRD: Strengthen LDD PM command facilitation

<!--
Product Manager artifact. Describe the product need and acceptance boundary.
Do not use the codebase as design input. Do not include implementation choices,
architecture, file paths, APIs, schemas, libraries, test strategy, or code snippets.
Capture technical uncertainty only as a dependency, constraint, or open question.
-->

## Problem

Not yet addressed. Owned by `/ldd:elaborate`.

## Goals

- Make `/ldd:scope`, `/ldd:elaborate`, and `/ldd:refine` stronger guided Product Manager workflows, not just thin ownership checklists.
- Preserve LDD's Product Manager boundary: product-scope commands must not smuggle in technical design, implementation mechanics, or codebase-derived design decisions.
- Add a self-contained PM facilitation protocol to the three commands so they can guide users through ambiguity without depending on external skills.
- Support starting a new draft Product Requirement from source context when no active draft exists, even if other promoted tickets are still in later workflow phases.
- Make each PM command end with an explicit handoff gate that states the updated artifact, unresolved questions, recommended next LDD command, and human decision needed.

## Non-goals

- Do not add a required dependency on external PM, facilitation, grill, or orchestration skills.
- Do not merge `/ldd:scope`, `/ldd:elaborate`, and `/ldd:refine` into a single monolithic PRD command.
- Do not change downstream engineering ownership for `/ldd:design`, `/ldd:plan`, `/ldd:decompose`, `/ldd:implement`, or `/ldd:verify`.
- Do not introduce duplicate workflow state such as `progress.md`, session logs, or global ledgers.
- Do not let an incomplete promoted ticket block creation of a separate new draft Product Requirement.
- Do not make `/ldd:scope` mutate a promoted ticket unless the user explicitly identifies that ticket.

## Users / Personas

Not yet addressed. Owned by `/ldd:elaborate`.

## User Stories

Not yet addressed. Owned by `/ldd:elaborate`.

## Acceptance Criteria

Not yet addressed. Draft criteria are owned by `/ldd:elaborate`; testable criteria are owned by `/ldd:refine`.

## Success Metrics

Not yet addressed. Draft metrics are owned by `/ldd:elaborate`; measurable metrics are owned by `/ldd:refine`.

## Dependencies

- LDD skills must remain standalone and agent-agnostic.
- Repo-local ledger state remains canonical; external trackers stay optional review and sync surfaces.
- The existing scope/elaborate/refine research update is the source context for this Product Requirement.
- Scope must preserve the LDD distinction between Product Requirement drafts and promoted ticket workflow records.
- The active `LDD-0001` ticket is still in verification and should not be modified by this new Product Requirement.

## Open Questions

- What minimum facilitation protocol belongs in every PM command without making the skills too verbose? Owner: elaboration.
- Should `Guided`, `Context dump`, and `Best guess` modes be exposed identically across all three PM commands? Owner: elaboration.
- How should `/ldd:scope` name and de-duplicate new drafts created from source documents? Owner: refinement.

## PRD Handoff Checklist

<!-- Complete before opening the PRD PR. -->

- [ ] Problem is expressed from the user's perspective.
- [x] Goals and non-goals make the scope boundary clear.
- [ ] User stories cover the main workflow and meaningful user-visible edge cases.
- [ ] Acceptance criteria are observable without reading code.
- [ ] Metrics define how product success will be judged.
- [x] Dependencies and open questions are explicit.
- [x] No implementation decisions, architecture, file paths, APIs, schemas, libraries, test strategy, or code snippets are present.
