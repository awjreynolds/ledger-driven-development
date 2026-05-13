---
ticket: null
draft_id: "2026-05-13-tracker-readiness-guided-next"
title: "Make LDD ready for external trackers and guided next actions"
created: 2026-05-13
updated: 2026-05-13
---

# PRD: Make LDD ready for external trackers and guided next actions

<!--
Product Manager artifact. Describe the product need and acceptance boundary.
Do not use the codebase as design input. Do not include implementation choices,
architecture, file paths, APIs, schemas, libraries, test strategy, or code snippets.
Capture technical uncertainty only as a dependency, constraint, or open question.
-->

## Problem

Not yet addressed by `/ldd:scope`.

## Goals

- Identify the functional gaps that prevent a maintainer from using LDD as the normal workflow for real project work.
- Make LDD usable with external planning and review surfaces, especially GitHub, Linear, and Jira, while preserving the repo-local ledger as the canonical workflow record.
- Let a maintainer understand which tracker capabilities are required for basic LDD use, which are optional, and which should remain out of scope for the near term.
- Improve `/ldd:next` so it not only reports the next LDD command, but also offers to perform the next action when that action is appropriate for the current workflow state.
- Preserve human confirmation before any external tracker mutation or workflow transition that changes durable state.

## Non-goals

- Do not replace the repo-local ledger with GitHub, Linear, Jira, or any other external tracker.
- Do not require all three tracker integrations to be equally complete before LDD can become useful.
- Do not build a general project-management platform, bidirectional sync engine, or generic issue migration tool.
- Do not make `/ldd:next` perform external mutations or local artifact changes without an explicit human go-ahead.
- Do not collapse the existing LDD phases into a single automatic command that bypasses product, design, planning, implementation, verification, or closure gates.
- Do not make tracker-specific authentication, permissions, or hosting choices part of product scope unless they directly change the user-facing workflow boundary.

## Users / Personas

Not yet addressed by `/ldd:scope`.

## User Stories

Not yet addressed by `/ldd:scope`.

## Acceptance Criteria

Not yet addressed by `/ldd:scope`.

## Success Metrics

Not yet addressed by `/ldd:scope`.

## Dependencies

- LDD must remain local-ledger-first; external trackers are review, collaboration, and notification surfaces unless a later approved requirement explicitly changes that boundary.
- GitHub, Linear, and Jira have different workflow concepts, permission models, and API limits, so scope must allow a common LDD product model without assuming identical tracker behavior.
- External tracker changes require human confirmation.
- `/ldd:next` must continue to diagnose workflow state accurately before it offers to continue with the next action.
- The functional-gap assessment should distinguish required MVP gaps from useful enhancements so the resulting work can be decomposed safely.

## Open Questions

- Should the first external-tracker path prioritize GitHub because it is closest to code review, or should the first path prioritize the tracker a target team already uses for planning?
- What is the minimum tracker behavior required for LDD to be considered "usable" rather than merely "sync-capable"?
- Should `/ldd:next` offer to run only the next LDD command, or should it also offer specific human-review actions such as approving an artifact, resolving drift, or choosing between blocked options?

## PRD Handoff Checklist

<!-- Complete before opening the PRD PR. -->

- [ ] Problem is expressed from the user's perspective.
- [x] Goals and non-goals make the scope boundary clear.
- [ ] User stories cover the main workflow and meaningful user-visible edge cases.
- [ ] Acceptance criteria are observable without reading code.
- [ ] Metrics define how product success will be judged.
- [x] Dependencies and open questions are explicit.
- [x] No implementation decisions, architecture, file paths, APIs, schemas, libraries, test strategy, or code snippets are present.
