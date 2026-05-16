---
work item: GADD-0001
prd: gadd/work-items/_archive/GADD-0001-verify-context-header/prd.md
created: 2026-05-13
updated: 2026-05-13
adrs: []
---

# Software Design Document: Add GADD execution context and verification gate

## Context

This design implements the approved PRD for `GADD-0001`. The existing MVP already has command-shaped skills, repo-local per-Work Item ledgers, rich issue templates, and a local archive directory. It does not yet expose a compact execution context/header for a Work Item, and it does not yet have a separate verification gate between implementation completion and Work Item closure.

- PRD: `gadd/work-items/_archive/GADD-0001-verify-context-header/prd.md`
- Existing entry points:
  - `skills/gadd-*/SKILL.md`
  - `commands/gadd/*.md`
  - `commands/gadd/*.toml`
  - `agent-skills.json`
  - `.claude-plugin/plugin.json`
  - `gemini-extension.json`
  - `scripts/validate-gadd-mvp.sh`
- Relevant ADRs: none. No ADR directory exists yet.
- Terms from the codebase/domain glossary: Ledger, Product Requirement, Child Work Item, Vertical Slice, Workflow Navigation, Standalone Skill Contract, External Drift, Work Item Archive.

## Constraints

- Product constraints from the PRD:
  - GADD remains local-ledger-first.
  - The context/header must work before, during, and after SDD creation; it cannot be owned only by the SDD.
  - Verification is specific to child Work Item closure, not a general repository healthcheck.
  - Implementation completion and Work Item closure are separate states.
  - The feature must be standalone and agent-agnostic.
- Technical constraints from existing code:
  - Every installed command must carry its own workflow contract; there is no shared installed `gadd-core`.
  - Adapter files are thin routers and must continue to point to canonical `skills/gadd-*/SKILL.md` files.
  - `scripts/validate-gadd-mvp.sh` explicitly enumerates commands and package files.
  - Setup templates under `skills/gadd-setup/assets/templates/` are copied into target repos and must be updated with any new ledger/artifact contract.
- Operational constraints:
  - External tracker mutation requires human confirmation.
  - Existing repos may have ledgers without the new context or verification fields.
- Compatibility constraints:
  - Commands must tolerate missing new fields and derive state from existing artifact statuses where possible.
  - Existing `gadd/work-items/_archive/` behavior stays unchanged: normal workflow navigation ignores archived child work.
- Explicit non-goals:
  - No general repository healthcheck.
  - No full external tracker sync engine.
  - No multi-agent orchestration or swarm executor.
  - No global ledger.
  - No `progress.md`.

## Existing System

- Current flow:
  - `/gadd:setup` installs config, templates, and Work Item directories.
  - `/gadd:scope`, `/gadd:elaborate`, and `/gadd:refine` create and approve a Product Requirement.
  - `/gadd:design` writes this SDD.
  - `/gadd:plan` writes `plan.md` and `plan.html`.
  - `/gadd:decompose` creates independently grabbable child work items from an approved plan.
  - `/gadd:implement` executes one ready child work item using its built-in TDD loop.
  - `/gadd:next` reads ledgers and reports the next command.
- Current data/contracts:
  - `ledger.yml` records Work Item IDentity, artifact paths/statuses, child links, sync state, and compact events.
  - `issue-body-prd.md` and `issue-body-child.md` are rich external projections.
  - `pr-body-implementation.md` captures implementation conformance but does not decide closure.
- Extension points:
  - New command-shaped skills can be added by creating `skills/gadd-verify/`, adapter files, agent metadata, and manifest entries.
  - Ledger schema can be extended because commands already treat the repo-local ledger as canonical.
  - Templates can be expanded for new target repos.
- Fragile or risky areas:
  - Command lists are duplicated in manifests, adapters, README, Gemini/Claude metadata, and validation.
  - `/gadd:next` currently does not model verification-required states.
  - `/gadd:implement` currently says it updates ledgers after approval, but it does not define a closure gate.
- Prior art to follow:
  - The current ledger keeps workflow state compact and machine-readable.
  - Decomposition previews child Work Items before creation.
  - Implementation embeds its own TDD loop instead of depending on an external skill.

## Decision Summary

| Decision | Rationale | Source |
| --- | --- | --- |
| Add an `execution_context` section to each Work Item ledger rather than a separate context file. | The PRD rejects global state and says the context cannot be owned only by the SDD. The existing ledger is already the canonical per-Work Item state and avoids another artifact to keep synchronized. | PRD, `CONTEXT.md`, local ledger MVP design |
| Add `/gadd:verify` as a standalone command-shaped skill. | Verification is a distinct gate between implementation completion and closure. Folding it into `/gadd:implement` would hide the human closure boundary. | PRD |
| Store verification results as `verification.md` plus ledger status fields on child work items. | Reviewers need readable output, while workflow navigation needs machine-readable status. | PRD, existing artifact pattern |
| Keep closure/archive/external close separate from verification pass. | The PRD requires implementation completion, verification, and closure to be distinct. Verification can recommend closure, but external mutation and archive still require human approval. | PRD, existing external mutation rule |
| Update `/gadd:next` to prioritize verify-required child work before additional implementation. | Maintainers need the next gate visible without reconstructing chat history. | PRD |
| Do not create an ADR for this design. | The choices extend the existing ledger-first architecture rather than changing ownership boundaries or introducing a surprising cross-cutting rule. | SDD template ADR threshold |

## Alternatives Considered

| Alternative | Why not | Tradeoff accepted |
| --- | --- | --- |
| Separate `context.yml` per Work Item. | It creates a second canonical state surface and increases drift risk with `ledger.yml`. | The ledger grows slightly, but remains the single machine-readable Work Item state. |
| Put execution context only in SDD frontmatter. | The PRD says context must be usable before, during, and after SDD creation. SDD-only context would not help early phases or child Work Items. | SDDs stay focused on engineering design. |
| Treat verification as part of `/gadd:implement`. | That would collapse implementation completion and closure verification into one phase. | A new command adds package surface but preserves the gate. |
| Add a general `/gadd:healthcheck`. | The PRD explicitly excludes a broad repository healthcheck. | Verification remains narrower and easier to test. |
| Auto-close/archive after verification passes. | External mutations and archive decisions require human confirmation. | Passing verification still needs a short approval step before closure. |

## Proposed Design

### New or changed responsibilities

- `ledger.yml`
  - Gains an `execution_context` section for compact, current handoff state.
  - Child ledgers gain verification and closure fields.
- `/gadd:next`
  - Reads `execution_context` when present.
  - Derives context from artifact statuses when the field is absent.
  - Reports `/gadd:verify <child-work-item-id>` when implementation is complete but closure is not verified.
- `/gadd:implement`
  - Continues to implement one ready child work item.
  - On completed implementation evidence, marks implementation complete and closure verification required.
  - Does not archive or externally close child work.
- `/gadd:verify`
  - Reads the child ledger, parent ledger, approved PRD, approved SDD, approved plan, child Work Item body, implementation evidence, check evidence, and external drift metadata.
  - Writes `verification.md` in the child Work Item directory.
  - Updates child ledger verification status to `passed`, `failed`, or `override_required`.
  - Recommends closure only when evidence, checks, traceability, and drift checks pass.
- `/gadd:setup`
  - Copies updated ledger and verification templates into target repos.
- Package manifests and adapters
  - Add `gadd-verify` wherever other command-shaped skills are listed.

### State/data changes

Parent and child ledgers support this optional section:

```yaml
execution_context:
  phase: design | plan | decompose | implement | verify | done
  current_gate: prd_approval | design_review | plan_review | decomposition_review | implementation | verification | closure
  next_command: /gadd:design
  next_human_action: null
  next_reason: PRD is approved and SDD is missing.
  approved_artifacts:
    prd: gadd/work-items/_archive/GADD-0001-verify-context-header/prd.md
    sdd: null
    plan: null
  boundaries:
    product: gadd/work-items/_archive/GADD-0001-verify-context-header/prd.md
    design: null
    plan: null
  updated_at: 2026-05-13T00:00:00Z
```

Child ledgers additionally support:

```yaml
artifacts:
  verification:
    path: gadd/work-items/GADD-0001/children/GADD-0001-001/verification.md
    status: missing | pending | passed | failed | overridden

closure:
  status: open | verification_required | verified | archived | externally_closed
  verified_at: null
  archived_at: null
  external_closed_at: null
  override_reason: null
```

Existing ledgers without these fields remain valid. Commands derive equivalent context from `Work Item.status`, artifact statuses, `children`, and sync state.

### Boundary changes

- Product Requirement closure remains out of scope for the MVP except for parent roll-up visibility from child states.
- Verification operates on child work items, not parent PRDs.
- External trackers remain projections; verification reads drift metadata and blocks closure if drift is unresolved, but it does not reconcile external changes.

### Error handling

- Missing implementation evidence: `/gadd:verify` writes a failed verification report and leaves `closure.status` as `verification_required`.
- Failed checks: `/gadd:verify` records the failed checks and blocks closure.
- Scope/design/plan drift: `/gadd:verify` identifies the earliest affected command and stops.
- External drift: `/gadd:verify` stops before closure recommendation and asks for human reconciliation.
- Missing new ledger fields: commands derive state and may backfill `execution_context` during the next mutating command.

### Backwards compatibility

- Existing target repos do not need migration before normal commands run.
- `/gadd:setup` updates templates for new installations only.
- The implementation plan should include a narrow template-update slice and a separate active-ledger backfill slice for this repo's dogfood Work Item.

## Data Flow / Control Flow

1. Main parent Work Item path:
   1. `/gadd:design` writes `sdd.md`.
   2. The ledger records `artifacts.sdd.status: draft` and updates `execution_context.next_human_action` to design approval.
   3. `/gadd:plan` writes `plan.md` and `plan.html`.
   4. `/gadd:decompose` previews and then creates child work items.
2. Main child Work Item implementation path:
   1. `/gadd:implement <child-id>` completes implementation evidence and checks.
   2. Child ledger records implementation completion and `closure.status: verification_required`.
   3. `/gadd:next` reports `/gadd:verify <child-id>`.
   4. `/gadd:verify <child-id>` writes `verification.md`.
   5. If verification passes, the child ledger records `artifacts.verification.status: passed` and `closure.status: verified`.
   6. After human approval, archive and external close may proceed.
3. Failure path:
   1. `/gadd:verify` finds missing evidence, failed checks, drift, or scope/design mismatch.
   2. It writes the blocking reason to `verification.md`.
   3. The child remains active and unclosed.
   4. `/gadd:next` continues to report the appropriate corrective gate.

## Interfaces / Contracts

| Contract | Producer | Consumer | Compatibility notes |
| --- | --- | --- | --- |
| `execution_context` ledger section | Mutating `/gadd:*` commands | `/gadd:next`, maintainers, implementation agents | Optional for old ledgers; derived when absent. |
| `artifacts.verification` ledger status | `/gadd:verify` | `/gadd:next`, maintainers, closure/archive flow | Child ledgers only for MVP. |
| `closure` ledger section | `/gadd:implement`, `/gadd:verify`, closure/archive step | `/gadd:next`, external sync flow | Missing section means open/not yet implemented. |
| `verification.md` | `/gadd:verify` | Product reviewers, engineering reviewers, maintainers | Human-readable report, not canonical state by itself. |
| `/gadd:verify` skill | Agent Skills package | Codex, Claude Code, Gemini CLI, future agents | Must be standalone like existing command-shaped skills. |
| Updated `agent-skills.json` and adapter manifests | GADD package source | Installers and host agents | Additive command surface. |
| Updated validation script | Repo maintainers | CI/local validation | Must require `gadd-verify` package files and ban external skill dependencies. |

Minimum evidence for `/gadd:verify` to recommend closure:

- Child work item ID and parent Product Requirement link.
- Approved parent PRD, SDD, and plan.
- Child acceptance criteria and covered user stories.
- Implementation evidence such as commit, diff, PR, or local changed-file summary.
- Check evidence such as automated test output, validation command output, or explicit manual verification notes.
- Drift evidence showing no unresolved external issue body change when an external tracker is configured.

## Migration / Compatibility

- Migration required: none before use. New fields are optional and can be backfilled by the next mutating GADD command.
- Rollout/backout:
  - Roll out as additive package files and template updates.
  - Backout removes `/gadd:verify` from manifests and returns `/gadd:implement` to its current post-implementation behavior, but existing `verification.md` files may remain as inert artifacts.
- Default behavior:
  - For ledgers without child verification fields, `/gadd:next` derives the next action from implementation status and artifact presence.
  - For child work with implementation evidence but no verification, closure is treated as not verified.
- Compatibility tests:
  - Existing package validation still passes.
  - Validation requires the new command files and manifest entries.
  - Hostile test fixtures cover missing evidence, failed checks, drift, and attempted closure before verification.

## Observability

- Logs: no runtime logging is added; command output states the next gate and reasons.
- Metrics: no automated metrics in MVP. The success metric is reviewability from `ledger.yml`, `execution_context`, and `verification.md`.
- Alerts: none.
- Debugging affordances:
  - `execution_context.next_reason` explains why `/gadd:next` selected the gate.
  - `verification.md` records pass/fail findings and blocking evidence.
  - Ledger events record important transitions such as `verification_failed`, `verification_passed`, and `child_archived`.

## Security / Privacy

- Data touched:
  - Repo-local Work Item metadata, artifact paths, implementation evidence summaries, and verification reports.
  - External tracker IDs, URLs, timestamps, and body hashes when configured.
- Permissions/authz:
  - No new permissions are required for local mode.
  - External close/update still requires human confirmation and the host agent's existing tracker credentials.
- Secrets:
  - No secrets are stored in the ledger, `execution_context`, or `verification.md`.
- Abuse cases:
  - A generated verification report could overstate evidence. The command must list concrete evidence paths/commands and block when evidence is missing.
  - An external issue could be closed despite local failure. The command must not mutate external trackers unless the ledger says verification passed or the human explicitly records an override.

## ADRs

- Existing: none.
- New: none.

The design is additive inside the existing ledger-first command package. It does not change the source-of-truth rule, package ownership boundary, or external tracker model, so it stays below the ADR threshold for this MVP.

## Open Design Questions

| Question | Impact | Owner | Next action |
| --- | --- | --- | --- |
| None. | Planning can proceed. | Engineering | Use this SDD to create an implementation plan. |

## Review Checklist

- [x] Every material PRD goal has a corresponding design decision or explicit non-design note.
- [x] The design is grounded in current code and relevant ADRs.
- [x] No product scope has been added beyond the PRD.
- [x] New architectural decisions have ADRs or are clearly below the ADR threshold.
- [x] Interfaces, migration, observability, and security/privacy have been considered.
- [x] Open questions are either resolved or explicitly block plan approval.
