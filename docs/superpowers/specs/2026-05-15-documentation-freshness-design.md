# Documentation Freshness Design

**Date:** 2026-05-15
**Status:** proposed design
**Context:** making documentation freshness explicit in LDD implementation and verification

## Thesis

LDD should treat documentation freshness as part of implementation evidence, not as optional cleanup and not as a hidden reviewer responsibility.

When a child work item changes user-facing behavior, command behavior, public APIs, configuration, setup flow, templates, integration contracts, or operational workflow, the implementation must either update the relevant documentation or record a direct rationale that no documentation update is needed.

## Current Gap

The current README accurately reflects the existing workflow, but the workflow does not yet make documentation freshness explicit.

Current behavior:

- `plan.md` asks for files/modules and tests/checks, but not documentation impact.
- Child tickets ask for what to build, acceptance criteria, review load, and traceability, but not documentation impact.
- `/ldd:implement` records changed-file summary and check evidence, but does not require docs changed or docs-not-needed rationale.
- `/ldd:verify` checks implementation evidence, check evidence, and scope/design/plan drift, but only catches missing docs when docs were already part of the approved plan or child ticket.

This leaves agents room to treat code changes as complete even when user-facing docs, setup docs, templates, or external issue/PR body guidance are stale.

## Design Rule

Every implementation slice must account for documentation impact.

The valid outcomes are exactly:

- `updated`: documentation was changed and the implementation evidence names the changed docs.
- `not_needed`: documentation was reviewed and no update is needed; the implementation evidence states why.
- `blocked`: documentation impact is unclear or cannot be updated safely; the child cannot pass verification until resolved.

An agent must not silently choose `not_needed`. The rationale must be written in the implementation evidence and visible to verification.

## Planning Contract

The plan template should add a documentation impact column or section.

For each slice, the plan should identify likely documentation touch points:

- user-facing README or usage docs
- command skill docs
- setup templates
- external issue or PR body templates
- ADR or architecture docs
- no documentation expected, with reason

The plan remains a planning aid, not a final permission boundary. If implementation discovers different documentation impact, it must explain the variance in implementation evidence.

## Child Ticket Contract

Child ticket bodies should include a `Documentation impact` section.

The section should tell an implementation agent what documentation needs to be updated, or state that documentation is not expected and why. This keeps child work independently grabbable without forcing the agent to infer documentation obligations from the parent plan.

## Implementation Contract

`/ldd:implement` should require documentation evidence before marking a child as implemented.

Implementation completion evidence must include:

- changed-file summary
- check evidence
- implementation PR or local diff reference when available
- documentation impact status: `updated`, `not_needed`, or `blocked`
- documentation files changed, or docs-not-needed rationale

If documentation impact is `blocked`, `/ldd:implement` must not mark the child as implementation-completed. It should report the blocking documentation question and the earliest command or human decision that can repair it.

Implementation must not silently update approved PRD, SDD, or plan artifacts to make documentation match code. If implementation reveals that approved artifacts are wrong or incomplete, it must stop and route to the earliest affected `/ldd:scope`, `/ldd:design`, or `/ldd:plan` command.

## Verification Contract

`/ldd:verify` should treat missing documentation evidence as a verification issue.

Verification should:

- read documentation impact evidence from the child ledger, implementation evidence, PR body, or local diff summary
- fail verification when documentation impact is missing for a slice that changes user-facing behavior, command behavior, public APIs, configuration, setup flow, templates, integration contracts, or operational workflow
- fail verification when documentation impact is `blocked`
- pass documentation review when docs were updated and trace to the implemented behavior
- pass documentation review when `not_needed` has a direct rationale that matches the actual change

Verification remains a child-ticket closure-readiness gate, not a broad documentation audit. It checks the documentation impact of the implemented child work only.

## README Contract

The README should state the rule plainly:

- implementation evidence must include documentation impact
- documentation is updated when behavior or usage changes
- documentation-not-needed requires a written rationale
- verification checks documentation impact before closure readiness

This keeps the public package description aligned with the command contracts.

## Ledger Evidence

The child ledger may record compact documentation evidence under implementation evidence, for example:

```yaml
artifacts:
  implementation:
    status: completed
    evidence:
      docs:
        status: updated
        paths:
          - README.md
        rationale: README workflow section updated for the changed command contract.
```

For no documentation changes:

```yaml
artifacts:
  implementation:
    evidence:
      docs:
        status: not_needed
        rationale: Internal-only refactor with no user-facing behavior, command contract, setup, template, API, or workflow change.
```

## Non-Goals

- Do not require documentation edits for every code change.
- Do not turn `/ldd:verify` into a repository-wide documentation audit.
- Do not let implementation silently rewrite approved PRD, SDD, or plan artifacts.
- Do not add a duplicate progress log for documentation work.
- Do not make documentation freshness depend on external tracker state unless the child ticket or plan explicitly requires it.

## Follow-On Work

- Update `README.md`.
- Update `skills/ldd-setup/assets/templates/plan.md`.
- Update `skills/ldd-setup/assets/templates/issue-body-child.md`.
- Update `skills/ldd-implement/SKILL.md`.
- Update `skills/ldd-verify/SKILL.md`.
- Update validation if package checks should enforce the new contract text.
