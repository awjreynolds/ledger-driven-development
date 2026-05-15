# Work Item Triage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved Work Item triage model so GADD can route unclassified intake to implementation, SDD-only design, PRD discovery, or terminal states.

**Architecture:** This is a clean package model shift from Ticket-centric PRD flow to Work Item-centric governed work. The repo-local ledger remains canonical for workflow control state, while external issues/comments become the human-facing projection for triage narratives in external-tracker mode. `/gadd:triage` is added as an intake command; downstream commands branch on Work Item type and approved boundary source.

**Tech Stack:** Markdown Agent Skills, JSON package manifests, Gemini TOML command routers, YAML OpenAI skill metadata, shell validation, SVG/PNG documentation assets.

---

## File Structure

Create:

- `skills/gadd-triage/SKILL.md`: canonical triage command contract.
- `skills/gadd-triage/agents/openai.yaml`: OpenAI skill metadata.
- `commands/gadd/triage.md`: Claude Code command adapter.
- `commands/gadd/triage.toml`: Gemini command adapter.
- `skills/gadd-setup/assets/templates/work-item-ledger.yml`: setup template for `ledger.yml` in each Work Item directory.
- `skills/gadd-setup/assets/templates/triage.md`: local-only triage narrative template and external projection comment template.
- `skills/gadd-setup/assets/templates/issue-body-work-item.md`: external issue body projection for generic Work Items.
- `docs/assets/gadd-sdlc-workflow.source.svg`: editable diagram source copied from the final SVG before PNG rendering.

Modify:

- `agent-skills.json`: add `/gadd:triage`, update ledger state source from `docs/tickets/**/ledger.yml` to `docs/work-items/**/ledger.yml`, and revise command purposes to Work Item language.
- `.claude-plugin/plugin.json`: add `./commands/gadd/triage.md`.
- `gemini-extension.json`: add `/gadd:triage`.
- `GEMINI.md`: update package guidance to Work Item language and triage routing.
- `README.md`: add triage entry path and update Available Skills.
- `CONTEXT.md`: replace Ticket as canonical term with Work Item and add triage vocabulary.
- `docs/skills.md`: add `/gadd:triage`, rename ticket concepts, and document Product Requirement lane boundaries.
- `docs/workflow.md`: add triage section and update workflow mechanics.
- `docs/package-model.md`: change setup output from `docs/tickets/` to `docs/work-items/`.
- `docs/assets/gadd-sdlc-workflow.svg`: show triage intake and Work Item routes.
- `docs/assets/gadd-sdlc-workflow.png`: rendered PNG matching the SVG.
- `scripts/validate-gadd-mvp.sh`: enforce new command, templates, Work Item language, diagram assets, and GitNexus expectations.
- `skills/gadd-setup/SKILL.md`: create `docs/work-items/`, GitNexus setup guidance, label mappings, and Work Item templates.
- `skills/gadd-next/SKILL.md`: navigate Work Item type/state/route.
- `skills/gadd-approve/SKILL.md`: approve SDD gates for `engineering_change` without PRD, while preserving PRD approval for `product_requirement`.
- `skills/gadd-design/SKILL.md`: accept approved PRD or approved triage outcome.
- `skills/gadd-plan/SKILL.md`: support SDD-only engineering changes when planning is needed.
- `skills/gadd-decompose/SKILL.md`: decompose planned Work Item slices that are not necessarily PRD children.
- `skills/gadd-implement/SKILL.md`: implement from triage outcome for `bug_fix` and `task`.
- `skills/gadd-verify/SKILL.md`: verify based on Work Item type.
- `skills/gadd-close/SKILL.md`: close verified Work Items.
- `skills/gadd-archive/SKILL.md`: archive closed Work Item packages.
- `skills/gadd-research/SKILL.md`, `skills/gadd-scope/SKILL.md`, `skills/gadd-elaborate/SKILL.md`, `skills/gadd-refine/SKILL.md`: make these explicitly Product Requirement lane commands.
- `skills/gadd-setup/assets/templates/config.yml`: use Work Item directories, GitNexus-required triage policy, and label mapping config.
- `skills/gadd-setup/assets/templates/ledger.yml`: delete after `work-item-ledger.yml` is added, then update validation so `ledger.yml` is no longer required as a setup template.
- `skills/gadd-setup/assets/templates/prd.md`, `sdd.md`, `plan.md`, `verification.md`, PR/issue templates: update Work Item paths and language.

Test:

- `./scripts/validate-gadd-mvp.sh`
- `python3 -m json.tool agent-skills.json`
- `python3 -m json.tool .claude-plugin/plugin.json`
- `python3 -m json.tool .claude-plugin/marketplace.json`
- `python3 -m json.tool gemini-extension.json`
- `rg -n "GADD ticket|child ticket|docs/tickets|<ticket>|ticket-id" README.md CONTEXT.md docs skills commands agent-skills.json gemini-extension.json`

---

### Task 1: Make Validation Expect the Work Item Triage Package

**Files:**
- Modify: `scripts/validate-gadd-mvp.sh`

- [ ] **Step 1: Add triage to the command set and Work Item required files**

Change the command list near the top to include `triage` after `next`:

```sh
commands='setup next triage research scope elaborate refine approve design plan decompose implement verify close archive'
```

In `required_files`, replace the old template block:

```sh
skills/gadd-setup/assets/templates/ledger.yml
skills/gadd-setup/assets/templates/research.md
skills/gadd-setup/assets/templates/prd.md
skills/gadd-setup/assets/templates/sdd.md
skills/gadd-setup/assets/templates/plan.md
skills/gadd-setup/assets/templates/plan.html
skills/gadd-setup/assets/templates/issue-body-child.md
```

with:

```sh
skills/gadd-setup/assets/templates/work-item-ledger.yml
skills/gadd-setup/assets/templates/triage.md
skills/gadd-setup/assets/templates/research.md
skills/gadd-setup/assets/templates/prd.md
skills/gadd-setup/assets/templates/sdd.md
skills/gadd-setup/assets/templates/plan.md
skills/gadd-setup/assets/templates/plan.html
skills/gadd-setup/assets/templates/verification.md
skills/gadd-setup/assets/templates/issue-body-work-item.md
skills/gadd-setup/assets/templates/issue-body-prd.md
skills/gadd-setup/assets/templates/issue-body-sdd.md
skills/gadd-setup/assets/templates/pr-body-prd.md
skills/gadd-setup/assets/templates/pr-body-sdd-plan.md
skills/gadd-setup/assets/templates/pr-body-implementation.md
docs/assets/gadd-sdlc-workflow.svg
docs/assets/gadd-sdlc-workflow.png
```

- [ ] **Step 2: Add package-level grep checks**

Replace existing checks that require `/gadd:research` after setup with this expanded set:

```sh
grep -q '"stateSource": "docs/work-items/**/ledger.yml"' agent-skills.json
grep -q '"command": "/gadd:triage"' agent-skills.json
grep -q 'npx skills add awjreynolds/gadd' README.md
grep -q 'docs/workflow.md' README.md
grep -q 'docs/skills.md' README.md
grep -q 'docs/package-model.md' README.md
grep -q '/gadd:triage' README.md
grep -q 'Work Item' README.md
grep -q 'unclassified intake' README.md
grep -q 'Work Item' CONTEXT.md
grep -q 'Triage Quality Loop' CONTEXT.md
grep -q 'External Issue' CONTEXT.md
grep -q 'docs/work-items/' docs/package-model.md
grep -q '/gadd:triage' docs/skills.md
grep -q 'Product Requirement lane' docs/skills.md
grep -q 'Unclassified intake' docs/workflow.md
grep -q 'triage outcome' docs/workflow.md
grep -q 'ready_for_implementation' docs/workflow.md
grep -q 'needs_sdd' docs/workflow.md
grep -q 'needs_prd' docs/workflow.md
```

- [ ] **Step 3: Add manifest and adapter checks for triage**

Add these checks near the existing adapter checks:

```sh
grep -q './commands/gadd/triage.md' .claude-plugin/plugin.json
grep -q '"/gadd:triage"' gemini-extension.json
grep -q '"/gadd:triage"' agent-skills.json
```

- [ ] **Step 4: Add Work Item template checks**

Replace setup template checks that require `docs/tickets` and `ledger.yml` with:

```sh
grep -q 'draft_directory: docs/work-items/_drafts' skills/gadd-setup/assets/templates/config.yml
grep -q 'archive_directory: docs/work-items/_archive' skills/gadd-setup/assets/templates/config.yml
grep -q 'code_intelligence:' skills/gadd-setup/assets/templates/config.yml
grep -q 'preferred_tool: gitnexus' skills/gadd-setup/assets/templates/config.yml
grep -q 'required_for_triage: true' skills/gadd-setup/assets/templates/config.yml
grep -q 'labels:' skills/gadd-setup/assets/templates/config.yml
grep -q 'gadd:needs-info' skills/gadd-setup/assets/templates/config.yml
grep -q 'schema_version: 1' skills/gadd-setup/assets/templates/work-item-ledger.yml
grep -q 'work_item:' skills/gadd-setup/assets/templates/work-item-ledger.yml
grep -q 'type: external_issue_intake' skills/gadd-setup/assets/templates/work-item-ledger.yml
grep -q 'state: needs_info' skills/gadd-setup/assets/templates/work-item-ledger.yml
grep -q 'external:' skills/gadd-setup/assets/templates/work-item-ledger.yml
grep -q 'triage:' skills/gadd-setup/assets/templates/work-item-ledger.yml
grep -q '# Triage Narrative' skills/gadd-setup/assets/templates/triage.md
grep -q 'What we have established' skills/gadd-setup/assets/templates/triage.md
grep -q 'What we still need' skills/gadd-setup/assets/templates/triage.md
grep -q '# Work Item:' skills/gadd-setup/assets/templates/issue-body-work-item.md
```

- [ ] **Step 5: Add downstream contract checks**

Add these checks after the per-command loop:

```sh
grep -q 'approved triage outcome' skills/gadd-design/SKILL.md
grep -q 'Raw external issues must route through /gadd:triage' skills/gadd-design/SKILL.md
grep -q 'engineering_change' skills/gadd-approve/SKILL.md
grep -q 'without requiring an approved PRD' skills/gadd-approve/SKILL.md
grep -q 'ready_for_implementation' skills/gadd-next/SKILL.md
grep -q 'needs_sdd' skills/gadd-next/SKILL.md
grep -q 'needs_prd' skills/gadd-next/SKILL.md
grep -q 'bug_fix' skills/gadd-implement/SKILL.md
grep -q 'task' skills/gadd-implement/SKILL.md
grep -q 'approved triage outcome' skills/gadd-implement/SKILL.md
grep -q 'verify Work Items, not only child tickets' skills/gadd-verify/SKILL.md
grep -q 'Work Item archive directory' skills/gadd-archive/SKILL.md
```

- [ ] **Step 6: Add negative checks for old canonical storage language**

Add this block near the end:

```sh
if rg -n 'GADD ticket|docs/tickets|child ticket|parent ticket|ticket directory|ticket-id|<ticket>' README.md CONTEXT.md docs skills commands agent-skills.json gemini-extension.json >/tmp/gadd-ticket-language.txt; then
  echo "legacy ticket language remains outside external tracker context:" >&2
  cat /tmp/gadd-ticket-language.txt >&2
  exit 1
fi
```

During implementation, narrow this negative check if it catches intentional phrases such as "external tracker tickets/issues". Do not weaken it before the docs and command contracts have been updated.

- [ ] **Step 7: Run validation and confirm it fails for missing triage files**

Run:

```bash
./scripts/validate-gadd-mvp.sh
```

Expected: FAIL. The first failure should be a missing triage or Work Item file such as:

```text
missing required file: skills/gadd-setup/assets/templates/work-item-ledger.yml
```

- [ ] **Step 8: Commit validation red state**

```bash
git add scripts/validate-gadd-mvp.sh
git commit -m "test: require work item triage package surface"
```

---

### Task 2: Add the `/gadd:triage` Command Surface

**Files:**
- Create: `skills/gadd-triage/SKILL.md`
- Create: `skills/gadd-triage/agents/openai.yaml`
- Create: `commands/gadd/triage.md`
- Create: `commands/gadd/triage.toml`
- Modify: `agent-skills.json`
- Modify: `.claude-plugin/plugin.json`
- Modify: `gemini-extension.json`

- [ ] **Step 1: Create `skills/gadd-triage/SKILL.md`**

Use this initial contract:

```markdown
---
name: gadd-triage
description: Run /gadd:triage for unclassified GADD intake. Use when the user says /gadd:triage, provides an external issue, reports a bug, asks what to do with an issue, or wants to route a task, bug, engineering change, or ambiguous request into GADD.
---

# /gadd:triage

Normalize unclassified intake into a GADD Work Item and route it to implementation, SDD-only design, PRD discovery, or a terminal state.

This command is a standalone, agent-agnostic GADD command. Follow this file directly; do not require brainstorming, grill-me, issue-generation, or external triage skills.

## Inputs

```text
/gadd:triage [new|work-item-id|external-ref] [context]
```

Use `/gadd:triage` for unclassified incoming work: external issues, bug reports, engineer tasks, support reports, ambiguous requests, and "what should we do with this?" items. Do not require triage before deliberate PM-led Product Requirement discovery; `/gadd:research` and `/gadd:scope` remain valid direct entry points.

## Reads

- `.gadd/config.yml` when present
- active Work Item ledgers under the configured Work Item root
- external issue body, comments, labels, timestamps, and reporter metadata when an external reference is supplied and the tracker is configured
- repository files, docs, tests, ADRs, and existing GADD artifacts
- GitNexus code-intelligence context when code reality matters

## Writes

- a Work Item `ledger.yml`
- local-only `triage.md` only when no external tracker is configured for the Work Item
- compact ledger events for triage route decisions and external projection metadata
- external issue body/comment/labels/close only after human-in-the-loop approval and drift checks

## Work Item Types

- `bug_fix`: broken behavior against a clear expectation.
- `task`: bounded work where the desired outcome is clear and blast radius is low enough for implementation from the approved triage outcome.
- `engineering_change`: product intent is settled, but SDD is needed because architecture, contracts, data model, security/privacy behavior, cross-repo impact, or blast radius is meaningful.
- `product_requirement`: PRD path is required because product outcome, users, acceptance criteria, non-goals, or scope needs product agreement.
- `external_issue_intake`: temporary type while poor-quality external input is being normalized.
- `not_gadd_work`: duplicate, out of scope, unsupported, or not actionable through GADD.

## Triage States

Set exactly one state:

- `needs_info`
- `ready_for_implementation`
- `needs_sdd`
- `needs_prd`
- `blocked_on_human_decision`
- `duplicate`
- `out_of_scope`
- `not_gadd_work`

## Input Quality Gate

Required input standard before routing:

- source intake exists: user request, external issue, bug report, task description, support signal, or comparable context
- enough context exists to identify the affected behavior, desired outcome, or missing information
- external issue state has been freshly read when an external reference is supplied
- external drift has been checked before any external mutation
- GitNexus evidence is available and fresh enough before routing `bug_fix`, `task`, or `engineering_change` to `ready_for_implementation` or `needs_sdd`, unless the human explicitly approves manual fallback
- manual fallback records lower confidence and must not silently claim low blast radius

If the input quality gate fails, write only safe local state when useful and set `state: needs_info` or `blocked_on_human_decision`. Ask one focused question or recommend the earliest repairing action.

## Triage Quality Loop

Run a bounded quality loop:

1. Read the incoming request, external issue, comments, labels, and existing GADD state.
2. Create or bind a local Work Item early.
3. For bugs, attempt reproduction or identify the exact missing repro evidence.
4. Use GitNexus where code reality matters.
5. Draft or update the triage narrative and route decision.
6. Identify only gaps that block routing or implementation quality.
7. Ask focused questions one at a time, or propose a cleaned-up external issue rewrite.
8. Stop when the Work Item can route to implementation, SDD, PRD discovery, or a terminal state.

Do not visibly switch the user into brainstorming, grill-me, or another skill. The quality loop belongs to `/gadd:triage`.

## Routing Rules

- `ready_for_implementation` routes to `/gadd:implement <work-item-id>`.
- `needs_sdd` routes to `/gadd:design <work-item-id>`.
- `needs_prd` routes to `/gadd:research <work-item-id>` or `/gadd:scope <work-item-id>`.
- `needs_info` remains in `/gadd:triage <work-item-id>`.
- terminal states may lead to external update, label, comment, or close only after human approval and drift checks.

## Approved Triage Outcome

In external-tracker mode, the approved triage outcome is the projected external issue body/comment plus the local ledger route decision.

In local-only mode, the approved triage outcome is `triage.md` plus the local ledger route decision.

The durable GADD workflow state is the Work Item ledger. The human-facing triage narrative should live where the humans work: the external issue body or comments when an external tracker is configured.

## External Projection

Before posting a comment, rewriting a body, applying labels, or closing an issue:

1. Re-read the external issue.
2. Compare `external_updated_at` and `body_hash` with the ledger.
3. Present the exact proposed body/comment/label/close action.
4. Ask for human approval.
5. Record the projected URL, timestamp, hash, and managed labels in the ledger after success.

External comments should be normal engineering triage:

```markdown
## Triage Summary

What we have established:

- The command fails when the reporter passes an empty title.

What we still need:

- Please provide the exact command invocation and the expected title value.

Current GADD route:

- State: needs_info
- Likely route after clarification: needs_sdd | ready_for_implementation | needs_prd

---

GADD Traceability:
- Work Item: <work-item-id>
- Route: <route>
- Last synchronized: <timestamp>
```

Do not include raw private context, sensitive repo analysis, non-shareable GitNexus detail, or internal reasoning in external comments.

## Exit Gate

End with:

- Work Item ID
- type and state
- route and next command
- GitNexus evidence status or approved fallback status
- external projection status
- one copyable next command

## Stop Conditions

- no source intake exists
- external issue cannot be read when needed
- unresolved external drift would be overwritten
- GitNexus is missing, stale, or unindexed and the human has not approved fallback
- missing information prevents responsible route selection
- requested mutation lacks human approval
```

- [ ] **Step 2: Create `skills/gadd-triage/agents/openai.yaml`**

```yaml
interface:
  display_name: "GADD Triage"
  short_description: "Normalize intake and route Work Items"
  default_prompt: "Use $gadd-triage to triage an external issue, bug, task, or ambiguous request."

policy:
  allow_implicit_invocation: true
```

- [ ] **Step 3: Create Claude and Gemini command adapters**

`commands/gadd/triage.md`:

```markdown
Use the `gadd-triage` skill to run `/gadd:triage`.

Treat `skills/gadd-triage/SKILL.md` as canonical. This file is only a Claude Code slash-command adapter.
```

`commands/gadd/triage.toml`:

```toml
description = "Normalize unclassified GADD intake and route the Work Item."
prompt = """
Run `/gadd:triage` using the `gadd-triage` Agent Skill.

If the `gadd-triage` skill is available, activate it and follow its `SKILL.md` exactly. Treat the skill as canonical; this TOML file is only a command router.

User arguments:
{{args}}
"""
```

- [ ] **Step 4: Update `agent-skills.json`**

Change:

```json
"stateSource": "docs/tickets/**/ledger.yml"
```

to:

```json
"stateSource": "docs/work-items/**/ledger.yml"
```

Insert this command object after `/gadd:next`:

```json
{
  "command": "/gadd:triage",
  "skill": "gadd-triage",
  "path": "skills/gadd-triage",
  "purpose": "Normalize unclassified intake and route a Work Item to implementation, SDD, PRD discovery, or a terminal state."
}
```

- [ ] **Step 5: Update adapter manifests**

Add `"./commands/gadd/triage.md"` to `.claude-plugin/plugin.json` immediately after `next.md`.

Add `"/gadd:triage"` to `gemini-extension.json` immediately after `"/gadd:next"`.

- [ ] **Step 6: Verify command surface**

Run:

```bash
python3 -m json.tool agent-skills.json >/dev/null
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
python3 -m json.tool gemini-extension.json >/dev/null
./scripts/validate-gadd-mvp.sh
```

Expected: JSON checks pass. Validation still fails on Work Item docs/templates that later tasks have not updated.

- [ ] **Step 7: Commit command surface**

```bash
git add agent-skills.json .claude-plugin/plugin.json gemini-extension.json skills/gadd-triage commands/gadd/triage.md commands/gadd/triage.toml
git commit -m "feat: add gadd triage command surface"
```

---

### Task 3: Convert Setup Templates to Work Items

**Files:**
- Create: `skills/gadd-setup/assets/templates/work-item-ledger.yml`
- Create: `skills/gadd-setup/assets/templates/triage.md`
- Create: `skills/gadd-setup/assets/templates/issue-body-work-item.md`
- Modify: `skills/gadd-setup/assets/templates/config.yml`
- Modify: `skills/gadd-setup/SKILL.md`
- Modify: `skills/gadd-setup/assets/templates/prd.md`
- Modify: `skills/gadd-setup/assets/templates/sdd.md`
- Modify: `skills/gadd-setup/assets/templates/plan.md`
- Modify: `skills/gadd-setup/assets/templates/verification.md`
- Modify: `skills/gadd-setup/assets/templates/pr-body-implementation.md`

- [ ] **Step 1: Create `work-item-ledger.yml`**

```yaml
schema_version: 1
work_item:
  id: "{work_item_id}"
  title: "{title}"
  type: external_issue_intake
  state: needs_info
  route: /gadd:triage {work_item_id}
  created_at: "{created_at}"
  updated_at: "{updated_at}"
external:
  provider: null
  kind: null
  id: null
  url: null
  title: null
  last_read_at: null
  external_updated_at: null
  body_hash: null
  labels:
    observed: []
    managed: []
triage:
  projection:
    mode: null
    url: null
    projected_at: null
    projected_by: null
    body_hash: null
  code_intelligence:
    provider: gitnexus
    freshness: unknown
    indexed_repositories: []
    summary: null
    fallback_approved: false
artifacts:
  research:
    path: null
    status: null
  prd:
    path: null
    status: null
  sdd:
    path: null
    status: null
  plan:
    path: null
    status: null
  implementation:
    status: null
    evidence: {}
  verification:
    path: null
    status: null
closure:
  status: open
  verified_at: null
  closed_at: null
  external_closed_at: null
children: []
sync:
  external_body_hash: null
  external_updated_at: null
  managed_body_version: null
execution_context:
  phase: triage
  current_gate: triage
  next_command: /gadd:triage {work_item_id}
  next_human_action: null
  next_reason: Work Item is in triage and needs enough evidence to route.
  approved_artifacts: {}
  boundaries: {}
events:
  - type: work_item_created
    at: "{created_at}"
    by: gadd
    summary: Work Item created for triage.
```

- [ ] **Step 2: Create `triage.md`**

```markdown
# Triage Narrative: {title}

> Local-only artifact. In external-tracker mode, project this narrative to the external issue body or comment after human approval and record the projection in `ledger.yml`.

## Triage Summary

### What we have established

- {established_fact}

### What we still need

- {question}

## Source

- Work Item: `{work_item_id}`
- External issue: {external_url}
- Reporter or source: {source}

## Behavior / Request

### Expected behavior or desired outcome

{expected}

### Actual behavior or current state

{actual}

## Evidence

- Repro status: {repro_status}
- Evidence reviewed: {evidence}

## GitNexus / Code Intelligence

- Provider: GitNexus
- Freshness: {freshness}
- Indexed repositories: {indexed_repositories}
- Affected areas: {affected_areas}
- Blast-radius summary: {blast_radius}
- Manual fallback approved: {fallback_approved}

## Route Decision

- Type: `{work_item_type}`
- State: `{work_item_state}`
- Route: `{route}`
- Rationale: {route_rationale}

## GADD Traceability

- Work Item: `{work_item_id}`
- Last synchronized: {last_synchronized}
```

- [ ] **Step 3: Create `issue-body-work-item.md`**

```markdown
# Work Item: {title}

## Summary

{summary}

## Expected / Desired

{expected}

## Actual / Current

{actual}

## Evidence

{evidence}

## Acceptance / Done Criteria

- {criterion}

## GADD Traceability

- Work Item: `{work_item_id}`
- Type: `{work_item_type}`
- State: `{work_item_state}`
- Route: `{route}`
- Local ledger: `{ledger_path}`
```

- [ ] **Step 4: Update `config.yml`**

Set Work Item paths and required GitNexus triage policy:

```yaml
workflow:
  root: docs/work-items
  draft_directory: docs/work-items/_drafts
  archive_directory: docs/work-items/_archive

code_intelligence:
  preferred_tool: gitnexus
  required_for_triage: true
  required_for_routes:
    - ready_for_implementation
    - needs_sdd
  fallback_requires_human_approval: true
  freshness_policy:
    warn_when_stale: true
    block_when_stale_for_triage: true

labels:
  triage:
    needs_info: gadd:needs-info
    ready_for_implementation: gadd:ready-for-implementation
    needs_sdd: gadd:needs-sdd
    needs_prd: gadd:needs-prd
    blocked_on_human_decision: gadd:blocked-human
  types:
    bug_fix: type:bug
    task: type:task
    engineering_change: type:engineering-change
    product_requirement: type:product-requirement
```

Preserve existing tracker, branch, PR, plan renderer, and ADR sections unless they conflict with Work Item paths.

- [ ] **Step 5: Update `skills/gadd-setup/SKILL.md`**

Change its create list to:

```markdown
- `docs/work-items/`
- `docs/work-items/_drafts/`
- `docs/work-items/_archive/`
- `.gadd/config.yml`
- `.gadd/templates/work-item-ledger.yml`
- `.gadd/templates/triage.md`
- `.gadd/templates/research.md`
- `.gadd/templates/prd.md`
- `.gadd/templates/sdd.md`
- `.gadd/templates/plan.md`
- `.gadd/templates/plan.html`
- `.gadd/templates/verification.md`
- `.gadd/templates/issue-body-work-item.md`
- `.gadd/templates/issue-body-prd.md`
- `.gadd/templates/issue-body-sdd.md`
- `.gadd/templates/pr-body-prd.md`
- `.gadd/templates/pr-body-sdd-plan.md`
- `.gadd/templates/pr-body-implementation.md`
```

Replace "GitNexus remains advisory and must not block setup" with:

```markdown
GitNexus is expected for normal GADD operation and required for impact-aware triage routing. Setup must not silently install GitNexus or index repositories, but it must record the required triage policy, detect availability when practical, and print the exact setup or refresh action the human needs before `/gadd:triage` can route code-impacting Work Items.
```

- [ ] **Step 6: Update artifact templates to Work Item paths**

In `prd.md`, `sdd.md`, `plan.md`, `verification.md`, and PR body templates, replace:

```text
ticket: {ticket}
docs/tickets/{ticket}
Child ticket
Parent Product Requirement: {parent_ticket_id}
```

with:

```text
work_item: {work_item_id}
docs/work-items/{work_item_id}
Child Work Item
Parent Product Requirement Work Item: {parent_work_item_id}
```

Use exact visible headings:

```markdown
## GADD Traceability

- Work Item: `{work_item_id}`
- Work Item type: `{work_item_type}`
- Local ledger: `docs/work-items/{work_item_id}/ledger.yml`
```

- [ ] **Step 7: Run validation**

Run:

```bash
./scripts/validate-gadd-mvp.sh
```

Expected: template-related checks pass. Remaining failures should point at docs and downstream command contracts.

- [ ] **Step 8: Commit setup templates**

```bash
git add skills/gadd-setup/SKILL.md skills/gadd-setup/assets/templates
git commit -m "feat: add work item setup templates"
```

---

### Task 4: Update Canonical Docs and Workflow Diagram

**Files:**
- Modify: `README.md`
- Modify: `CONTEXT.md`
- Modify: `docs/skills.md`
- Modify: `docs/workflow.md`
- Modify: `docs/package-model.md`
- Modify: `docs/assets/gadd-sdlc-workflow.svg`
- Modify: `docs/assets/gadd-sdlc-workflow.png`
- Optional create: `docs/assets/gadd-sdlc-workflow.source.svg`

- [ ] **Step 1: Update `README.md` skill list**

Add `/gadd:triage` after `/gadd:next`:

```markdown
- `/gadd:triage` - Normalize unclassified intake into a Work Item and route it to implementation, SDD, PRD discovery, or a terminal state.
```

Change the opening description to include:

```markdown
GADD manages Work Items across triage, product scope, engineering design, planning, implementation, verification, and closure. External issues are collaboration surfaces; repo-local ledgers remain canonical workflow state.
```

Add a short "Entry Paths" section:

```markdown
## Entry Paths

- Known product discovery starts with `/gadd:research` or `/gadd:scope`.
- Unclassified intake starts with `/gadd:triage`.
- Existing Work Items continue with `/gadd:next`.
```

- [ ] **Step 2: Update `CONTEXT.md` canonical terms**

Add or replace terms so the canonical set includes:

```markdown
**Work Item**:
The canonical repo-local unit of GADD-governed work.
_Avoid_: ticket, issue, story

**External Issue**:
A tracker-native GitHub, Linear, Jira, or similar record that can source or project a Work Item.
_Avoid_: canonical ledger state

**Triage Outcome**:
The approved route decision for an unclassified Work Item, made from triage evidence, GitNexus impact evidence, and human approval where required.
_Avoid_: permanent local triage brief

**Triage Quality Loop**:
The bounded clarification loop inside `/gadd:triage` that improves poor-quality intake only until the Work Item can route responsibly.
_Avoid_: switching into a separate brainstorming or grill-me workflow
```

Update relationship bullets:

```markdown
- A Work Item has exactly one repo-local Ledger.
- A Work Item may bind to an External Issue, but the External Issue is not canonical workflow state.
- A Work Item may be a `bug_fix`, `task`, `engineering_change`, `product_requirement`, `external_issue_intake`, or `not_gadd_work`.
- Product Requirement work is one Work Item type, not the only GADD entry path.
- In external-tracker mode, the triage narrative is projected to the External Issue after human approval; the Ledger records route and sync metadata.
```

- [ ] **Step 3: Update `docs/skills.md`**

Add `/gadd:triage` to the catalog before `/gadd:research`:

```markdown
| `/gadd:triage` | Intake | Normalize unclassified intake and route a Work Item. | External issue, bug report, task, support signal, ambiguous request, optional GitNexus context | Work Item ledger, approved triage outcome, optional external comment/body/labels after approval | `/gadd:implement`, `/gadd:design`, `/gadd:research`, `/gadd:scope`, or terminal state |
```

Rename the Product + Repo Context lane to "Product Requirement Lane" where it describes `/gadd:research`, `/gadd:scope`, `/gadd:elaborate`, and `/gadd:refine`. State that those commands reject non-product Work Item types.

- [ ] **Step 4: Update `docs/workflow.md`**

Add this section before "MVP Workflow":

```markdown
## Intake And Triage

GADD has two entry paths:

- Known product discovery starts with `/gadd:research` or `/gadd:scope`.
- Unclassified intake starts with `/gadd:triage`.

`/gadd:triage` creates or binds a Work Item, normalizes poor-quality external issues, uses GitNexus for blast-radius evidence when code reality matters, and records the route decision in the Work Item ledger.

Triage routes:

- `ready_for_implementation` -> `/gadd:implement <work-item-id>`
- `needs_sdd` -> `/gadd:design <work-item-id>`
- `needs_prd` -> `/gadd:research <work-item-id>` or `/gadd:scope <work-item-id>`
- `needs_info`, `duplicate`, `out_of_scope`, `not_gadd_work`, or `blocked_on_human_decision` -> remain in triage or terminal handling

In external-tracker mode, the human-facing triage narrative is projected to the external issue body or comments after human approval. The repo-local ledger stores workflow state, external binding, sync hashes, GitNexus evidence summary, and projection links.
```

- [ ] **Step 5: Update `docs/package-model.md` setup output**

Replace:

```text
docs/tickets/_drafts/
docs/tickets/_archive/
```

with:

```text
docs/work-items/_drafts/
docs/work-items/_archive/
```

Add `gadd-triage` to the skill layout examples only if the doc lists specific commands.

- [ ] **Step 6: Update workflow SVG**

Edit `docs/assets/gadd-sdlc-workflow.svg` so the diagram shows:

```text
Unclassified intake -> /gadd:triage -> triage outcome
triage outcome -> /gadd:implement
triage outcome -> /gadd:design
triage outcome -> /gadd:research or /gadd:scope
Known product discovery -> /gadd:research or /gadd:scope -> PRD lane
```

Use "Work Items" and "External issues" terminology in the diagram. Remove "ready child ticket", "child vertical-slice tickets", and `/gadd:implement <ticket>` text.

- [ ] **Step 7: Render PNG**

Run:

```bash
sips -s format png docs/assets/gadd-sdlc-workflow.svg --out docs/assets/gadd-sdlc-workflow.png
file docs/assets/gadd-sdlc-workflow.png
```

Expected:

```text
docs/assets/gadd-sdlc-workflow.png: PNG image data
```

If `sips` cannot render the SVG correctly, use the browser screenshot path available in the environment and record the command in `scripts/validate-gadd-mvp.sh` comments.

- [ ] **Step 8: Run docs checks**

Run:

```bash
rg -n "GADD ticket|child ticket|docs/tickets|<ticket>|ticket-id" README.md CONTEXT.md docs
./scripts/validate-gadd-mvp.sh
```

Expected: `rg` should return only intentional external-ticket references or no output. Validation may still fail on downstream skill contracts until later tasks.

- [ ] **Step 9: Commit docs and diagram**

```bash
git add README.md CONTEXT.md docs/skills.md docs/workflow.md docs/package-model.md docs/assets/gadd-sdlc-workflow.svg docs/assets/gadd-sdlc-workflow.png
git commit -m "docs: document work item triage workflow"
```

---

### Task 5: Update Downstream Skill Contracts for Work Item Routing

**Files:**
- Modify: `skills/gadd-next/SKILL.md`
- Modify: `skills/gadd-approve/SKILL.md`
- Modify: `skills/gadd-design/SKILL.md`
- Modify: `skills/gadd-plan/SKILL.md`
- Modify: `skills/gadd-decompose/SKILL.md`
- Modify: `skills/gadd-implement/SKILL.md`
- Modify: `skills/gadd-verify/SKILL.md`
- Modify: `skills/gadd-close/SKILL.md`
- Modify: `skills/gadd-archive/SKILL.md`
- Modify: `skills/gadd-research/SKILL.md`
- Modify: `skills/gadd-scope/SKILL.md`
- Modify: `skills/gadd-elaborate/SKILL.md`
- Modify: `skills/gadd-refine/SKILL.md`

- [ ] **Step 1: Update `/gadd:next` routing**

Add this decision order before existing PRD-led routing:

```markdown
## Work Item Routing

If `work_item.state: needs_info`, report:

```text
next_command: /gadd:triage <work-item-id>
```

If `work_item.state: ready_for_implementation`, report:

```text
next_command: /gadd:implement <work-item-id>
```

If `work_item.state: needs_sdd`, report:

```text
next_command: /gadd:design <work-item-id>
```

If `work_item.state: needs_prd`, route to `/gadd:research <work-item-id>` when research is absent or blocked; otherwise route to `/gadd:scope <work-item-id>`.

If `work_item.state` is `duplicate`, `out_of_scope`, or `not_gadd_work`, report no implementation command and show the recorded terminal reason.
```

- [ ] **Step 2: Update `/gadd:approve`**

Add SDD gate rules:

```markdown
SDD approval is allowed when either:

- the Work Item type is `product_requirement` and the PRD is approved, or
- the Work Item type is `engineering_change` and the approved triage outcome is recorded in the ledger.

Do not require an approved PRD for `engineering_change` SDD approval. Do require the SDD `## Structure` quality gate in both paths.
```

- [ ] **Step 3: Update `/gadd:design`**

Replace the approved PRD-only input gate with:

```markdown
Required boundary before writing design:

- `product_requirement`: approved PRD in the Work Item ledger.
- `engineering_change`: approved triage outcome in the Work Item ledger.

Raw external issues are never design inputs. If the user passes an external reference and it is not already bound to a `needs_sdd` Work Item, stop and route to `/gadd:triage <external-ref>`.
```

- [ ] **Step 4: Update `/gadd:implement`**

Add required input matrix:

```markdown
Required inputs by Work Item type:

- `bug_fix`: approved triage outcome, GitNexus or approved fallback evidence, done criteria, documentation impact.
- `task`: approved triage outcome, GitNexus or approved fallback evidence, done criteria, documentation impact.
- `engineering_change`: approved triage outcome, approved SDD, optional approved plan when the SDD requires one.
- `product_requirement`: approved PRD, approved SDD, approved plan, and ready decomposed Work Item slice when decomposition exists.
```

Replace `/gadd:implement <ticket>` examples with `/gadd:implement <work-item-id>`.

- [ ] **Step 5: Update `/gadd:verify`**

Replace parent PRD/SDD/plan mandatory gate with:

```markdown
Required approved inputs by Work Item type:

- `bug_fix` and `task`: approved triage outcome, implementation evidence, check evidence, documentation impact, external drift review.
- `engineering_change`: approved triage outcome, approved SDD, optional plan/decomposition artifacts if used, implementation evidence, check evidence, documentation impact, external drift review.
- `product_requirement`: approved PRD, approved SDD, approved plan, decomposition artifacts when used, implementation evidence, check evidence, documentation impact, external drift review.
```

Keep verification as mandatory before closure.

- [ ] **Step 6: Update `/gadd:close` and `/gadd:archive`**

Replace child/parent-ticket-only wording with Work Item wording:

```markdown
Close one verified Work Item, or close a parent Work Item only when every child Work Item is verified and closeable.
```

Archive under configured `docs/work-items/_archive` by default.

- [ ] **Step 7: Update Product Requirement lane commands**

In `gadd-research`, `gadd-scope`, `gadd-elaborate`, and `gadd-refine`, add:

```markdown
This is a Product Requirement lane command. It accepts direct PM-led product discovery or Work Items routed from triage with `state: needs_prd`. Reject `bug_fix`, `task`, and `engineering_change` Work Items with a clear route back to `/gadd:next <work-item-id>` or `/gadd:triage <work-item-id>`.
```

- [ ] **Step 8: Update `/gadd:plan` and `/gadd:decompose`**

Add:

```markdown
For `engineering_change`, `/gadd:plan` may run after SDD approval when the SDD says multiple reviewable slices or review-load management are needed. A PRD is not required for this path.

For `engineering_change`, `/gadd:decompose` creates child Work Items under the SDD/design Work Item projection rather than under a PRD issue.
```

- [ ] **Step 9: Run validation**

Run:

```bash
./scripts/validate-gadd-mvp.sh
```

Expected: downstream contract checks pass. Remaining failures should point to manifests/adapters/docs if any were missed.

- [ ] **Step 10: Commit skill contract updates**

```bash
git add skills/gadd-*/SKILL.md
git commit -m "feat: route skills by work item type"
```

---

### Task 6: Update Command Adapters and Metadata Text

**Files:**
- Modify: `commands/gadd/*.md`
- Modify: `commands/gadd/*.toml`
- Modify: `skills/gadd-*/agents/openai.yaml`
- Modify: `GEMINI.md`

- [ ] **Step 1: Update adapter descriptions**

For each command adapter that mentions "ticket", use Work Item language. Examples:

`commands/gadd/implement.toml` should say:

```toml
description = "Implement a ready GADD Work Item with code, tests, docs impact, and evidence."
```

`commands/gadd/verify.toml` should say:

```toml
description = "Verify an implemented GADD Work Item for closure readiness."
```

`commands/gadd/design.toml` should say:

```toml
description = "Create or update an SDD from an approved PRD or approved triage outcome."
```

- [ ] **Step 2: Update OpenAI metadata**

Use short descriptions like:

```yaml
interface:
  display_name: "GADD Implement"
  short_description: "Implement a ready Work Item"
  default_prompt: "Use $gadd-implement to implement Work Item GADD-123."
```

Apply these exact short descriptions:

```yaml
# skills/gadd-next/agents/openai.yaml
short_description: "Report the next action for a Work Item"
default_prompt: "Use $gadd-next to inspect Work Item GADD-123."

# skills/gadd-approve/agents/openai.yaml
short_description: "Approve a PRD, SDD, or plan gate"
default_prompt: "Use $gadd-approve to approve the active gate for Work Item GADD-123."

# skills/gadd-design/agents/openai.yaml
short_description: "Design from a PRD or triage outcome"
default_prompt: "Use $gadd-design to create an SDD for Work Item GADD-123."

# skills/gadd-plan/agents/openai.yaml
short_description: "Plan implementation for an approved design"
default_prompt: "Use $gadd-plan to plan Work Item GADD-123."

# skills/gadd-decompose/agents/openai.yaml
short_description: "Create reviewable Work Item slices"
default_prompt: "Use $gadd-decompose to decompose Work Item GADD-123."

# skills/gadd-verify/agents/openai.yaml
short_description: "Verify Work Item closure readiness"
default_prompt: "Use $gadd-verify to verify Work Item GADD-123."

# skills/gadd-close/agents/openai.yaml
short_description: "Close a verified Work Item"
default_prompt: "Use $gadd-close to close Work Item GADD-123."

# skills/gadd-archive/agents/openai.yaml
short_description: "Archive closed Work Item files"
default_prompt: "Use $gadd-archive to archive Work Item GADD-123."
```

- [ ] **Step 3: Update `GEMINI.md`**

Add:

```markdown
GADD's canonical work unit is a Work Item. External issues and tickets are tracker-native collaboration surfaces. Use `/gadd:triage` for unclassified intake and `/gadd:research` or `/gadd:scope` for known PM-led Product Requirement discovery.
```

- [ ] **Step 4: Run adapter checks**

Run:

```bash
rg -n "ticket|child ticket|parent ticket|<ticket>|ticket-id" commands skills/gadd-*/agents GEMINI.md
./scripts/validate-gadd-mvp.sh
```

Expected: `rg` returns only intentional external-ticket references, or no output. Validation passes adapter and metadata checks.

- [ ] **Step 5: Commit adapters**

```bash
git add commands/gadd skills/gadd-*/agents/openai.yaml GEMINI.md
git commit -m "chore: update adapters for work item language"
```

---

### Task 7: Final Validation and Cleanup

**Files:**
- Modify: `scripts/validate-gadd-mvp.sh`
- Modify: `agent-skills.json`
- Modify: `.claude-plugin/plugin.json`
- Modify: `gemini-extension.json`
- Modify: `README.md`
- Modify: `CONTEXT.md`
- Modify: `docs/skills.md`
- Modify: `docs/workflow.md`
- Modify: `docs/package-model.md`
- Modify: `skills/gadd-*/SKILL.md`
- Modify: `commands/gadd/*.md`
- Modify: `commands/gadd/*.toml`
- Modify: `skills/gadd-*/agents/openai.yaml`

- [ ] **Step 1: Run full validation**

Run:

```bash
./scripts/validate-gadd-mvp.sh
```

Expected:

```text
GADD MVP validation passed.
```

If the script currently has no success message, add this final line:

```sh
echo "GADD MVP validation passed."
```

- [ ] **Step 2: Run JSON checks**

```bash
python3 -m json.tool agent-skills.json >/dev/null
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool gemini-extension.json >/dev/null
```

Expected: no output and exit code 0.

- [ ] **Step 3: Run legacy language scan**

```bash
rg -n "GADD ticket|child ticket|parent ticket|docs/tickets|<ticket>|ticket-id" README.md CONTEXT.md docs skills commands agent-skills.json gemini-extension.json
```

Expected: no output except intentional references to external tracker tickets/issues. If there are intentional references, rewrite them as "external tracker tickets/issues" so the scan can be strict.

- [ ] **Step 4: Inspect final diff**

```bash
git diff --stat
git diff --check
```

Expected: no whitespace errors. Diff should include triage command files, Work Item templates, docs, diagram assets, validation, and downstream skill contracts.

- [ ] **Step 5: Commit validation cleanup**

```bash
git add .
git commit -m "test: validate work item triage workflow"
```

---

## Self-Review Notes

Spec coverage:

- Work Item canonical model: Tasks 3, 4, 5, 6, 7.
- `/gadd:triage` front door: Task 2.
- External-first triage narrative: Tasks 2, 3, 4, 5.
- GitNexus expected and triage-required: Tasks 1, 2, 3, 4.
- Downstream command ambiguity: Task 5.
- Workflow PNG/SVG and triage section: Task 4.
- Validation enforcement: Tasks 1 and 7.
- Clean-break storage from `docs/tickets` to `docs/work-items`: Tasks 1, 3, 4, 7.

Type consistency:

- Work Item ID template token: `{work_item_id}`.
- Work Item type field: `work_item.type`.
- Work Item state field: `work_item.state`.
- Route field: `work_item.route`.
- External binding field: `external`.
- Triage projection field: `triage.projection`.
- GitNexus evidence field: `triage.code_intelligence`.

No intentional compatibility layer is included. This plan implements the clean model shift requested in the approved design.
