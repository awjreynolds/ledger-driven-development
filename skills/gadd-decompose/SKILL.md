---
name: gadd-decompose
description: Run /gadd:decompose after an approved GADD plan. Use when the user says /gadd:decompose or needs plan slices turned into child vertical-slice tickets for implementation.
---

# /gadd:decompose

Turn an approved `plan.md` into child vertical-slice tickets.

## Reads

- parent `ledger.yml`
- approved PRD
- approved SDD
- approved `plan.md`

## Produces

- child ticket entries in the parent ledger
- child ticket ledgers under the parent ticket directory
- external child work items only when a tracker is configured and the human approves

## Input Quality Gate

Required input standard before previewing or creating child tickets:

- approved PRD, approved SDD, and approved plan in the parent ledger
- plan slices are traceable to acceptance criteria and dependency-safe
- in GitHub tracker mode, the SDD issue is approved or bound and has a known issue number
- enough slice detail for independently grabbable child tickets
- each proposed slice has a review-load estimate that is reasonable for one human review

If inputs fail this standard, write nothing and name the blocking gap. The earliest GADD command that can repair missing slices is `/gadd:plan`; missing approval routes to `/gadd:approve <ticket-id>`; missing SDD issue linkage routes to `/gadd:approve <ticket-id>` for SDD approval or tracker reconciliation.

## Preview Before Creation

Before creating or updating any child ticket, present the proposed ticket set and stop for human approval. This approval is not handled by `/gadd:approve`; it is a decomposition review decision.

Use this review shape:

```text
Proposed child tickets:

1. SDD #<sdd-issue-number> Slice <slice-number>: <short outcome title>
   Type: Autonomous | Human-review
   Blocked by: None | <ticket title/id>
   User stories covered: <PRD story numbers>
   Documentation impact: Updated | Not needed: <reason> | Blocked: <question>
   Review load: Low | Medium | High, with expected file groups and risk
   Summary: <one or two sentences>

Ask:
- Does the granularity feel right?
- Are dependency relationships correct?
- Are Autonomous/Human-review classifications correct?
- Is the review load small enough for a focused PR?
- Is documentation impact explicit for every child ticket?
- Should any tickets be merged or split?
```

Only after approval may the command create child ledgers or external child work items. When stopping before approval, set `execution_context.next_human_action` to the decomposition review decision.

## Rules

- Repo-local ledger is canonical. External trackers are optional sync/review surfaces.
- External mutations require human confirmation.
- Decompose only from an approved plan. Do not invent scope or architecture.
- Child tickets are vertical slices derived from plan slices, not layer tasks.
- Decompose for human reviewability, not just execution convenience. A reviewer should be able to understand one child ticket and its likely PR without loading the entire project into working memory.
- Apply a cognitive-load budget before creating children. Estimate expected file groups, likely files touched, test surface, risk, and dependency coupling for each slice.
- Do not knowingly create a child ticket or aggregate implementation path that would produce a huge PR, especially anything expected to approach or exceed 200 changed files. Split by user-visible outcome, workflow path, command surface, or risk boundary before ticket creation.
- Prefer several coherent vertical slices over one overloaded slice when the same reviewer would otherwise need to review unrelated command surfaces, templates, docs, and tracker behavior in one PR.
- If a slice cannot be made reviewable without breaking atomic behavior, mark it `Human-review`, call out the overload risk in the preview, and require explicit human approval before creating the child ticket.
- In GitHub tracker mode, each child issue title must start with `SDD #<sdd_issue_number> Slice <slice-number>:` followed by a concise outcome title. This keeps issue lists readable and makes each implementation slice visibly traceable to its SDD parent without opening the issue body.
- In local-only tracker mode, use the equivalent approved SDD identifier in the child title, for example `SDD <ticket-id> Slice <slice-number>: <short outcome title>`.
- Each child ticket must be independently grabbable: an implementation agent can read the ticket, follow links as needed, and understand what end-to-end behavior to build, what acceptance criteria must pass, what it is blocked by, and which user stories or PRD criteria it covers.
- Each child ticket must reference the parent Product Requirement and approved plan slice.
- Each child ticket must include documentation impact: documentation to update, not needed with reason, or a blocked documentation question.
- In GitHub tracker mode, each child work item must be created as a native GitHub sub-issue of the approved SDD issue. Body traceability to the SDD issue is required, but body links alone are not enough when GitHub sub-issues are available.
- To create the GitHub relationship, create the child issue first, capture its numeric REST `id`, then call GitHub's sub-issues endpoint on the SDD issue: `POST /repos/{owner}/{repo}/issues/{sdd_issue_number}/sub_issues` with `sub_issue_id`. Verify the relationship with the parent/sub-issues REST endpoints before recording the child as externally synced.
- In GitHub tracker mode, native sub-issues make implementation child work items children of the SDD issue and grandchildren of the PRD issue.
- External child ticket bodies use GADD's standalone child issue shape: Parent, What to build, Acceptance criteria, Blocked by, User stories covered, plus minimal GADD Traceability.
- In GitHub tracker mode, child tickets may be projected as GitHub issues after explicit human confirmation. Each projected child issue must record its PRD issue reference, SDD issue reference, plan slice, native parent/sub-issue relationship status, and local ledger path. The child ledger remains canonical.
- If GitHub sub-issue attachment fails because the feature, permissions, repository settings, or API are unavailable, stop and report the failure. Do not silently fall back to body-only linked issues. A body-only linked issue fallback requires a separate explicit human confirmation after the failure is reported.
- Linear and Jira child-ticket projections are follow-on optional collaboration surfaces, but the portable GADD contract is the same: create tracker-native child/sub-items where the tracker supports them, and record body traceability as backup.
- Before updating an existing external child ticket, re-read it. If its body changed since the last recorded sync hash or timestamp, stop and ask the human to reconcile the external contribution.
- Keep the MVP lightweight: do not create a separate decomposition artifact unless the user explicitly asks.

## Stop Conditions

- parent ledger missing
- plan is missing or not approved
- plan slices are too vague to turn into independently grabbable vertical slices
- proposed slices are too large for focused human review and need to be split
- external tracker is configured but cannot be reached
- human rejects the proposed child ticket set
