---
work item: GADD-0003
prd: gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/prd.md
created: 2026-05-13
updated: 2026-05-13
status: approved
adrs: []
---

# Software Design Document: Make GADD ready for external trackers and guided next actions

## Context

This design implements the approved PRD for `GADD-0003`. GADD already has command-shaped skills, thin command adapters, package manifests, repo-local ledgers, rich issue/PR templates, verification, closure, and a validation script that enforces the installable package surface. The remaining gaps are about making the workflow usable as a normal day-to-day loop: external visibility, explicit approval commands, safer continuation from `/gadd:next`, and preventing PM artifacts from passing gates without shared understanding.

- PRD: `gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/prd.md`
- Existing entry points:
  - `skills/gadd-*/SKILL.md`
  - `commands/gadd/*.md`
  - `commands/gadd/*.toml`
  - `agent-skills.json`
  - `.claude-plugin/plugin.json`
  - `gemini-extension.json`
  - `skills/gadd-setup/assets/templates/*`
  - `scripts/validate-gadd-mvp.sh`
- Relevant ADRs: none. No ADR directory exists yet.
- Terms from the codebase/domain glossary: Ledger, Product Requirement, Software Design Document, Execution Context, Work Item Promotion, External Tracker, External Drift, Standalone Skill Contract, Human-approved Closure.

## Constraints

- Product constraints from the PRD:
  - Repo-local ledgers remain canonical.
  - GitHub is the first external-tracker dogfooding path.
  - Linear and Jira remain follow-on collaboration surfaces.
  - External tracker mutations require explicit human confirmation.
  - `/gadd:next` must diagnose state before offering continuation.
  - PRD and SDD approval must use explicit `/gadd:approve <work-item-id>` rather than conversation-only shorthand.
  - `/gadd:approve` does not approve plans, decomposition, closure, or external mutations in this PRD.
- Technical constraints from existing code:
  - Commands are standalone skills; there is no shared installed runtime library.
  - Every command needs a skill folder, adapter files, agent metadata, manifest entries, and validation coverage.
  - The validation script hard-codes command lists and package requirements.
  - Current tracker configuration supports `provider: local`; GitHub behavior must be additive and optional.
  - Existing PRD/SDD/plan/verification templates are copied into target repos by `/gadd:setup`.
- Operational constraints:
  - Agents may run in environments without GitHub credentials or network access.
  - External tracker body drift must stop mutation until a human reconciles it.
  - `/gadd:next` must remain safe to run repeatedly.
- Compatibility constraints:
  - Existing local-only ledgers remain valid.
  - Existing approved PRDs and SDDs continue to work without `/gadd:approve` history.
  - Existing `approve PRD` prompt wording can be supported as legacy guidance, but the forward path should name `/gadd:approve`.
- Explicit non-goals:
  - No full bidirectional sync engine.
  - No equal Linear/Jira implementation now.
  - No replacement of the repo-local ledger with GitHub Issues or PRs.
  - No plan, decomposition, closure, or external mutation approval in `/gadd:approve`.
  - No hidden automation of durable state changes from `/gadd:next`.

## Existing System

- Current flow:
  - `/gadd:scope`, `/gadd:elaborate`, and `/gadd:refine` create and approve PRDs.
  - `/gadd:design` creates SDDs.
  - `/gadd:plan` creates implementation plans and plan review artifacts.
  - `/gadd:decompose`, `/gadd:implement`, `/gadd:verify`, and `/gadd:close` advance child work.
  - `/gadd:next` reads ledgers and reports the next command.
- Current data/contracts:
  - `ledger.yml` stores artifact statuses, paths, sync metadata, execution context, and events.
  - `issue-body-prd.md`, `issue-body-child.md`, `pr-body-sdd-plan.md`, and `pr-body-implementation.md` already describe external projections.
  - `sync.external_body_hash` and `sync.managed_body_version` exist but no GitHub-first command behavior currently exercises them.
- Extension points:
  - Additive command-shaped skills can be introduced by following the existing `gadd-verify` and `gadd-close` pattern.
  - Existing templates can be extended without breaking current local ledgers.
  - `gadd/config.yml` already has `tracker.provider`, `repo`, `project`, and branch/PR title config fields.
- Fragile or risky areas:
  - Command/package surface is duplicated across manifests, adapters, README/GEMINI/docs, and validation.
  - Approval is currently expressed in prompts and chat, not as a first-class command.
  - `/gadd:next` is read-only and safe, but it does not yet clearly distinguish "next command" from "next human action".
  - External tracker synchronization can easily become a broad sync engine if not constrained.
- Prior art to follow:
  - `/gadd:verify` was added as a standalone command for a distinct gate.
  - PM skills now include bounded shared-understanding gates without depending on external skills.
  - External mutations already require human confirmation throughout the command contracts.

## Decision Summary

| Decision | Rationale | Source |
| --- | --- | --- |
| Add `/gadd:approve` as a standalone command-shaped skill. | Approval needs to be durable and understandable outside the current conversation. A command matches existing package architecture. | PRD, existing command-skill pattern |
| Limit `/gadd:approve` to PRD and SDD approval for this PRD. | The PRD explicitly excludes plan, decomposition, closure, and external mutation approval. | PRD |
| Infer PRD vs SDD approval from ledger state when exactly one approval gate is active. | The user approved inference, and it keeps the common command short while avoiding ambiguous shorthand. | PRD |
| Update `/gadd:next` to report both `next_command` and `next_human_action`, and offer safe continuation text without mutating state itself. | The PRD wants continuation from diagnosis, while preserving safety and explicit human confirmation. | PRD, existing `/gadd:next` read-only rule |
| Treat GitHub-first visibility as managed projections of existing GADD artifacts, not as canonical state. | The repo-local ledger remains canonical and the PRD rejects a full sync engine. | PRD, existing templates |
| Use existing GitHub surfaces: issues for PRD/child work, PRs for SDD+plan and implementation review. | Current templates already map to these review surfaces and GitHub is closest to code review. | PRD, templates |
| Keep bounded shared-understanding gates in PM skills and validation as part of this design. | The PRD names PM shared understanding as required-for-use. The skill updates are existing product reality that design must preserve. | PRD, current skills |
| No ADR is required. | The design extends the existing command-skill and ledger-first architecture. It does not introduce a hard-to-reverse ownership boundary or new runtime architecture. | ADR threshold |

## Alternatives Considered

| Alternative | Why not | Tradeoff accepted |
| --- | --- | --- |
| Keep using conversational `approve`. | It is ambiguous outside the current chat and does not satisfy the PRD. | Add one new command to the package surface. |
| Require `/gadd:approve prd GADD-0003` and `/gadd:approve sdd GADD-0003`. | It is explicit but noisier than needed when ledger state is unambiguous. | Inference is default; explicit artifact targets can be follow-on if ambiguity appears. |
| Make `/gadd:next` execute the next command automatically. | It would make a read-only diagnostic command mutate durable state. | `/gadd:next` offers the next action but waits for a separate command or explicit user instruction. |
| Build generic Linear/Jira/GitHub adapters now. | That expands beyond GitHub-first dogfooding and risks a broad sync engine. | GitHub path proves the common model first. |
| Store external tracker state as canonical. | The PRD says repo-local ledger remains canonical. | External tracker state is a projection with drift checks. |
| Add a shared runtime module for tracker operations. | The package currently has standalone markdown skills rather than executable runtime code. | Some instructions are duplicated, but installability remains simple. |

## Proposed Design

### New or changed responsibilities

- `/gadd:approve`
  - New standalone command-shaped skill under `skills/gadd-approve/`.
  - Reads a target Work Item ledger and determines the active approval gate.
  - Approves PRD when `current_gate: prd_approval` or `artifacts.prd.status: draft` and no SDD approval gate is active.
  - Approves SDD when `current_gate: design_review` or `artifacts.sdd.status: draft` and the PRD is already approved.
  - Updates frontmatter/status, ledger artifact status, `approved_artifacts`, `execution_context`, and events.
  - Stops if both PRD and SDD approvals are plausible, neither is plausible, or the artifact is missing.
  - Does not approve plan, decomposition, closure, or external mutation gates.

- `/gadd:next`
  - Continues to read ledger state without mutating files or external trackers.
  - Reports `next_human_action` when present.
  - For PRD/SDD approval gates, reports `/gadd:approve <work-item-id>`.
  - Offers safe continuation phrasing, for example: `Next action: /gadd:approve GADD-0003. Run that when ready.`
  - Does not itself perform approval, external mutation, archival, or artifact writes.

- GitHub-first tracker visibility
  - Extends command contracts for PM/design/plan/decompose/implement/verify/close to use GitHub only when `gadd/config.yml` has `tracker.provider: github` and required repo configuration.
  - Uses existing issue and PR body templates as managed projections.
  - Records external IDs/URLs and body hash/timestamp in `ledger.yml`.
  - Requires human confirmation before every create/edit/close operation.
  - Stops on external body drift before updating managed sections.

- PM shared-understanding gates
  - Keep the recently added bounded gates in `/gadd:scope`, `/gadd:elaborate`, and `/gadd:refine`.
  - Extend validation to require key phrases so regressions are caught.

- Package surface
  - Add `approve` to `scripts/validate-gadd-mvp.sh` command list.
  - Add skill, adapters, agent metadata, and manifest entries.
  - Update README/GEMINI/CONTEXT/docs where command lists and workflow diagrams are maintained.

### State/data changes

No new top-level ledger section is required. `/gadd:approve` uses existing fields:

```yaml
artifacts:
  prd:
    path: gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/prd.md
    status: approved
  sdd:
    path: gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/sdd.md
    status: draft

execution_context:
  phase: design
  current_gate: design_review
  next_command: /gadd:approve GADD-0003
  next_human_action: /gadd:approve GADD-0003
  next_reason: SDD is drafted and needs human approval before planning.
  approved_artifacts:
    prd: gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/prd.md
    sdd: null
    plan: null
```

Approval events use existing event style:

```yaml
events:
  - at: 2026-05-13T17:03:21Z
    type: prd_approved
    actor: human
  - at: 2026-05-13T17:30:00Z
    type: sdd_approved
    actor: human
```

GitHub projection state uses existing tracker/sync fields:

```yaml
tracker:
  mode: github
  external_id: "123"
  external_url: "https://github.com/org/repo/issues/123"

sync:
  status: synced | local_only | drift_detected
  last_checked_at: 2026-05-13T17:30:00Z
  external_updated_at: 2026-05-13T17:29:00Z
  external_body_hash: "sha256:..."
  managed_body_version: 1
```

If implementation needs per-artifact external URLs later, design should add them narrowly during planning only if one URL per Work Item is insufficient for PRD issue plus SDD/plan PR references.

### Boundary changes

- `/gadd:approve` becomes the only GADD command for PRD and SDD approval.
- `/gadd:refine` and `/gadd:design` may still ask the human whether the artifact is ready, but their next durable approval action should name `/gadd:approve <work-item-id>`.
- GitHub is a review/collaboration surface. It never owns phase state.
- Linear/Jira behavior is documented as follow-on and should not be implemented in the first plan unless needed for shared abstractions that GitHub already uses.

### Error handling

- Ambiguous approval gate: `/gadd:approve` stops and reports the candidate gates plus the explicit next command needed to disambiguate.
- Missing artifact: `/gadd:approve` stops and routes to the command that should create it.
- Artifact not ready: `/gadd:approve` stops and routes to `/gadd:refine` for PRD or `/gadd:design` for SDD.
- External tracker not configured: GitHub projection steps are skipped and local ledger approval proceeds.
- Missing GitHub credentials or CLI: command reports local completion and states external sync is pending human/environment setup.
- External drift: command stops before mutation and asks for reconciliation.

### Backwards compatibility

- Existing Work Items with `prd_approved` or `sdd_approved` events remain approved.
- Existing commands that mention "approve PRD" remain understandable, but new prompt text should prefer `/gadd:approve <work-item-id>`.
- Local-only mode continues to work without GitHub.
- Ledgers without `next_human_action` can still be interpreted by `/gadd:next` using artifact statuses.

## Data Flow / Control Flow

1. PRD approval path:
   1. `/gadd:refine <work-item>` finishes the PRD and sets `current_gate: prd_approval`.
   2. `/gadd:next <work-item>` reports `/gadd:approve <work-item>` as the next human action.
   3. `/gadd:approve <work-item>` sees exactly one PRD approval gate.
   4. It marks PRD frontmatter and ledger artifact status as approved.
   5. It sets `approved_artifacts.prd`, records `prd_approved`, and routes to `/gadd:design <work-item>`.

2. SDD approval path:
   1. `/gadd:design <work-item>` writes `sdd.md` and sets `artifacts.sdd.status: draft`.
   2. It sets `current_gate: design_review` and `next_human_action: /gadd:approve <work-item>`.
   3. `/gadd:approve <work-item>` sees exactly one SDD approval gate.
   4. It marks SDD frontmatter and ledger artifact status as approved.
   5. It sets `approved_artifacts.sdd`, records `sdd_approved`, and routes to `/gadd:plan <work-item>`.

3. `/gadd:next` continuation path:
   1. Reads target ledger and derives current gate.
   2. Reports `next_command`, `next_human_action`, and reason.
   3. If the next action is safe and commandable, displays the exact command.
   4. If the next action is blocked, displays the blocking decision instead of a continuation offer.

4. GitHub PRD visibility path:
   1. A PM approval or promotion command prepares the PRD issue body from `issue-body-prd.md`.
   2. If `tracker.provider: github`, command presents the create/update operation and waits for human confirmation.
   3. After creation/update, ledger records issue URL/ID and managed body hash.
   4. Future mutations re-read the issue first and stop on drift.

5. GitHub SDD/plan review path:
   1. `/gadd:design` and `/gadd:plan` prepare or update a review PR body from `pr-body-sdd-plan.md`.
   2. Branch naming uses existing `gadd/config.yml` branch templates.
   3. Human confirmation is required before PR creation/update.
   4. The repo-local SDD and plan remain canonical.

## Interfaces / Contracts

| Contract | Producer | Consumer | Compatibility notes |
| --- | --- | --- | --- |
| `/gadd:approve [work-item-id]` | New `gadd-approve` skill | Maintainers, `/gadd:next`, host adapters | Infers PRD vs SDD only when one approval gate is active. |
| `commands/gadd/approve.md` and `.toml` | GADD package | Claude/Gemini command routers | Thin adapters like existing commands. |
| `skills/gadd-approve/agents/openai.yaml` | GADD package | Codex skill UI | Follows existing metadata shape. |
| `execution_context.next_human_action` | Mutating GADD commands | `/gadd:next`, maintainers | Should name `/gadd:approve <work-item-id>` for PRD/SDD gates. |
| GitHub PRD issue body | PM approval/promotion flow | GitHub reviewers | Existing `issue-body-prd.md`, readable without repo access. |
| GitHub SDD/plan PR body | `/gadd:design` and `/gadd:plan` | GitHub reviewers | Existing `pr-body-sdd-plan.md`. |
| `sync.external_body_hash` | Any external projection update | Future external projection updates | Blocks overwrite on drift. |
| Bounded shared-understanding gate text | PM skills | Maintainers and validation | Must remain phase-bounded to prevent feature creep. |

## Migration / Compatibility

- Migration required: none for existing local Work Items.
- Rollout:
  - Add `/gadd:approve` package surface.
  - Update `/gadd:next`, `/gadd:refine`, and `/gadd:design` to route approval gates to `/gadd:approve`.
  - Update setup templates and docs for new command lists.
  - Add validation checks for approve command and bounded gates.
- Backout:
  - Remove `/gadd:approve` from manifests/adapters/validation.
  - Restore `/gadd:refine` and `/gadd:design` prompt wording to direct approval text.
  - Existing `prd_approved` and `sdd_approved` events remain valid.
- Default behavior:
  - Local mode skips GitHub mutations.
  - GitHub mode uses managed projections only after human confirmation.
- Compatibility tests:
  - Existing `GADD-0001` and archived `GADD-0002` ledgers remain readable by `/gadd:next`.
  - `GADD-0003` approval path works with `/gadd:approve GADD-0003`.

## Observability

- Logs: no runtime logs are required for local markdown skill operation.
- Metrics:
  - Reviewers can identify current phase and next action from `ledger.yml`.
  - Maintainers can classify required and optional gaps from the PRD.
- Alerts: none.
- Debugging affordances:
  - `execution_context.next_reason` explains approval/continuation routing.
  - `events` record `prd_approved`, `sdd_approved`, and approval invalidation.
  - GitHub drift state is visible in `sync.status` and timestamps/hashes.

## Security / Privacy

- Data touched:
  - Repo-local PRD/SDD/plan artifacts, ledger state, issue/PR body projections, external URLs and IDs.
- Permissions/authz:
  - Local mode needs no new permissions.
  - GitHub mode uses the host environment's GitHub authentication and must ask before mutations.
- Secrets:
  - Do not store GitHub tokens or credentials in ledgers, templates, or command output.
- Abuse cases:
  - Accidental approval of the wrong artifact is mitigated by requiring exactly one active PRD/SDD approval gate.
  - External overwrite is mitigated by drift checks before managed body updates.

## ADRs

- Existing: none.
- New: none.

No ADR is required. The design extends established command and ledger conventions. The most durable choice is adding a new command-shaped skill, which follows existing package architecture rather than changing it.

## Open Design Questions

| Question | Impact | Owner | Next action |
| --- | --- | --- | --- |
| Should `/gadd:approve` accept explicit artifact arguments in addition to inference? | Could help ambiguous edge cases, but not needed for the approved PRD. | Engineering design | Treat as follow-on unless implementation finds unavoidable ambiguity. |
| Should GitHub external state eventually support separate URLs per PRD issue, SDD/plan PR, and implementation PR? | Current ledger has one external URL slot per Work Item; richer tracking may need additive fields. | Engineering design | Defer until planning slices GitHub visibility. |

These questions do not block planning because the first implementation can use inference-only `/gadd:approve` and existing tracker fields, adding fields only if required by the GitHub slice.

## Review Checklist

- [x] Every material PRD goal has a corresponding design decision or explicit non-design note.
- [x] The design is grounded in current code and relevant ADRs.
- [x] No product scope has been added beyond the PRD.
- [x] New architectural decisions have ADRs or are clearly below the ADR threshold.
- [x] Interfaces, migration, observability, and security/privacy have been considered.
- [x] Open questions are either resolved or explicitly block plan approval.
