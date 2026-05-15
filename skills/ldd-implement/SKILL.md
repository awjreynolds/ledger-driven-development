---
name: ldd-implement
description: Run /ldd:implement for an LDD child vertical-slice ticket. Use when the user says /ldd:implement or wants to execute an approved child ticket with code and tests.
---

# /ldd:implement

Execute one ready child vertical-slice ticket.

## Reads

- child ticket ledger
- parent Product Requirement ledger
- approved PRD
- approved SDD
- approved `plan.md`

## Input Quality Gate

Required input standard before implementation:

- a ready child ticket that is not blocked by unfinished dependencies
- readable child ticket body and child ledger
- approved parent PRD, SDD, and plan boundaries
- acceptance criteria and plan slice specific enough to implement and test
- documentation impact expectation from the child ticket or parent plan, or enough context to record `updated`, `not_needed`, or `blocked`

If inputs fail this standard, do not edit product code or package artifacts. The earliest LDD command that can repair missing child work is `/ldd:decompose`; missing or wrong plan/design/product boundaries route to `/ldd:plan`, `/ldd:design`, `/ldd:refine`, `/ldd:scope`, or `/ldd:research` depending on the gap.

## Rules

- Repo-local ledger is canonical. External trackers are optional sync/review surfaces.
- External mutations require human confirmation.
- Follow the approved child ticket and parent plan, and preserve approved PRD, SDD, and plan boundaries. Do not silently update `plan.md` from implementation.
- Do not auto-decompose. If no ready child tickets exist, report that there are no tickets to implement. If the plan is approved but no child tickets exist, report that `/ldd:decompose` is required.
- If the plan is wrong, stop and return to the earliest affected `/ldd:design` or `/ldd:plan` step.
- The implementation PR contains product code, tests, and documentation updates required by the child work. Do not write `progress.md`.
- Run configured checks before PR.
- Account for documentation impact before marking implementation complete. The only valid documentation statuses are `updated`, `not_needed`, and `blocked`.
- If documentation impact is `updated`, record the changed documentation paths in implementation evidence. If documentation impact is `not_needed`, record the direct rationale. If documentation impact is `blocked`, do not mark implementation completed; report the blocking documentation question and the earliest command or human decision that can repair it.
- Update relevant documentation when the child changes user-facing behavior, command behavior, public APIs, configuration, setup flow, templates, integration contracts, or operational workflow.
- Use the implementation PR body template to summarize plan adherence, tests/checks, and any approved deviations.
- In GitHub tracker mode, the implementation PR is a managed projection for review. Ask before creating or updating it, stop on external drift, and keep the child ledger canonical.
- Record implementation completion evidence in the child ledger, including changed-file summary, check evidence, documentation impact status and paths or rationale, and any implementation PR or local diff reference available.
- Mark the child as implemented but not closed by setting `artifacts.implementation.status: completed`, `ticket.status: verification_required`, `closure.status: verification_required`, and `execution_context.next_command: /ldd:verify <child-ticket-id>` when those fields are available.
- If the ledger lacks verification or closure fields, record equivalent implementation completion evidence and state that `/ldd:verify <child-ticket-id>` is the next gate so `/ldd:next` can derive the same state.
- Do not archive child tickets.
- Do not close external child work items.
- Do not mark child work done, archived, externally closed, or verified from this command; `/ldd:verify` decides closure readiness after implementation completion.
- Implementation PR reviewer prompt: "Does this implementation follow the approved plan?"

## Built-in TDD Loop

LDD is standalone. Run this loop directly from this skill; do not delegate it to another installed skill, command, or methodology package.

For each behavior in the child ticket:

1. Identify the next acceptance criterion or plan verification point.
2. Write the smallest focused test that proves the behavior is missing.
3. Run the focused test and confirm it fails for the expected reason.
4. Write the smallest implementation that makes the test pass.
5. Run the focused test and confirm it passes.
6. Update documentation for the behavior when required, or record why documentation is not needed.
7. Refactor only after the focused test is green.
8. Rerun the relevant broader test suite before moving to the next behavior.

If no test harness exists, create the smallest credible harness first. If a behavior cannot be tested automatically, state the reason and add the narrowest credible manual verification.

## Stop Conditions

- child ticket missing
- no ready child tickets exist
- plan is approved but `/ldd:decompose` has not created child tickets
- plan is wrong
- tests/checks fail
- documentation impact is blocked
- implementation requires a product-scope change
