---
work item: GADD-0001
prd: gadd/work-items/_archive/GADD-0001-verify-context-header/prd.md
sdd: gadd/work-items/_archive/GADD-0001-verify-context-header/sdd.md
created: 2026-05-13
updated: 2026-05-13
plan_html: gadd/work-items/_archive/GADD-0001-verify-context-header/plan.html
adrs: []
---

# Implementation Plan: Add GADD execution context and verification gate

## Review Context

This plan translates the approved PRD and SDD into executable slices. It does not add new architecture beyond the SDD. Child Work Items will be created later by `/gadd:decompose`; this plan only defines the slices and traceability.

### PRD Summary

- Source: `gadd/work-items/_archive/GADD-0001-verify-context-header/prd.md`
- Goals covered:
  - Add a compact GADD execution context/header for active Work Items.
  - Add a verification gate after implementation and before closure.
  - Keep GADD local-ledger-first, standalone, and agent-agnostic.
  - Improve resume, audit, and handoff across agents.
- Non-goals to protect:
  - No general repository healthcheck.
  - No full external tracker sync engine.
  - No multi-agent orchestration.
  - No global ledger or `progress.md`.
  - No SDD-owned workflow state.
- Acceptance criteria:
  - Active Work Items expose compact phase, boundary, approved-input, and next-gate context.
  - Implementation completion and closure are separate states.
  - Verification reports whether child work is ready to mark done, archive, and close externally.
  - Closure is blocked by missing evidence, failed checks, drift, or unresolved external changes.
  - `/gadd:next` identifies verification as the next gate when implementation is complete but closure is unverified.
  - Verification is specific to child Work Item closure, not general repository health.
  - The workflow remains local-ledger-first and standalone.

### SDD Summary

- Source: `gadd/work-items/_archive/GADD-0001-verify-context-header/sdd.md`
- Design decisions to implement:
  - Add optional `execution_context` to each Work Item ledger.
  - Add standalone `/gadd:verify`.
  - Store human-readable verification results in `verification.md` and machine-readable state in child ledgers.
  - Keep closure/archive/external close separate from verification pass.
  - Update `/gadd:next` to prioritize verification-required child work.
- Interfaces/contracts to preserve:
  - Repo-local `ledger.yml` remains canonical.
  - Adapter files stay thin routers to canonical skill files.
  - External tracker mutation still requires human confirmation.
  - Existing ledgers without new fields remain valid.
- Migration/compatibility requirements:
  - No mandatory migration before use.
  - Template updates affect new installations.
  - Active dogfood Work Item can be backfilled by the current GADD command flow.

### ADR Summary

- ADRs: []
- Design rules that affect implementation:
  - No ADR required; the design is additive within the existing ledger-first architecture.
  - If implementation discovers a durable source-of-truth or ownership change, stop and return to `/gadd:design`.

## Slices

Use thin vertical slices where possible. Each slice leaves the repo in a reviewable state and includes its own verification.

| Slice | Outcome | Files/modules | Tests/checks | Dependencies |
| --- | --- | --- | --- | --- |
| 1. Add `/gadd:verify` package surface | `/gadd:verify` is installable across Codex, Claude Code, and Gemini, and appears in package metadata without changing behavior in other commands yet. | `agent-skills.json`, `README.md`, `GEMINI.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `gemini-extension.json`, `commands/gadd/verify.md`, `commands/gadd/verify.toml`, `skills/gadd-verify/SKILL.md`, `skills/gadd-verify/agents/openai.yaml`, `scripts/validate-gadd-mvp.sh` | `./scripts/validate-gadd-mvp.sh`; JSON validation already inside script; `git diff --check` | None |
| 2. Add ledger execution context and verification templates | New target repos receive `execution_context`, child verification/closure fields, and a `verification.md` template. Existing copied `gadd/templates` in this repo match the source templates. | `skills/gadd-setup/assets/templates/ledger.yml`, `skills/gadd-setup/assets/templates/verification.md`, `gadd/templates/ledger.yml`, `gadd/templates/verification.md`, `skills/gadd-setup/SKILL.md`, `README.md`, `CONTEXT.md` | `./scripts/validate-gadd-mvp.sh`; inspect template copies for parity; `git diff --check` | Slice 1 can run in parallel, but validation updates may land with either slice |
| 3. Teach `/gadd:next` and `/gadd:implement` the verification gate | Workflow navigation reports `/gadd:verify <child-id>` when implementation is complete but closure is unverified. Implementation marks verification required and does not archive/close. | `skills/gadd-next/SKILL.md`, `skills/gadd-implement/SKILL.md`, `commands/gadd/next.*` only if adapters need non-canonical text changes, `commands/gadd/implement.*` only if adapters need non-canonical text changes | `./scripts/validate-gadd-mvp.sh`; targeted hostile scenario review using fixture ledgers or documented examples; `git diff --check` | Slices 1 and 2 |
| 4. Define `/gadd:verify` workflow and report contract | `/gadd:verify` can be followed by any supported agent without external skills. It reads evidence, checks drift, writes `verification.md`, updates ledger verification state, and blocks closure when evidence is insufficient. | `skills/gadd-verify/SKILL.md`, `skills/gadd-setup/assets/templates/verification.md`, `gadd/templates/verification.md`, `scripts/validate-gadd-mvp.sh` | `./scripts/validate-gadd-mvp.sh`; hostile scenario review for missing evidence, failed checks, unresolved drift, and attempted external close before verification; `git diff --check` | Slices 1 and 2 |
| 5. Update docs and validation for the new end-to-end workflow | Public docs, glossary, validation, and the active GADD ledger reflect the full scope/design/plan/decompose/implement/verify path. | `README.md`, `CONTEXT.md`, `docs/superpowers/specs/2026-05-12-local-ledger-mvp-design.md`, `gadd/work-items/_archive/GADD-0001-verify-context-header/ledger.yml`, `scripts/validate-gadd-mvp.sh` | `./scripts/validate-gadd-mvp.sh`; `git diff --check`; `/gadd:next` should report plan approval or decompose after plan approval | Slices 1-4 |

Slice quality bar:

- Each slice is reviewable without needing all later slices.
- Package metadata changes and command semantics are separated enough to keep review focused.
- No slice depends on external installed skills.
- No slice auto-mutates an external tracker.

## Acceptance Criteria Traceability

| Acceptance criterion | Slice(s) | Verification |
| --- | --- | --- |
| Active Work Item exposes compact context identifying current phase, approved inputs, boundaries, and next gate. | 2, 3, 5 | Ledger template contains `execution_context`; active ledger is backfilled; `/gadd:next` uses or derives the context. |
| Implementation completion and Work Item closure are separate workflow states. | 2, 3, 4 | Child ledger template includes `closure.status`; `/gadd:implement` marks verification required rather than closed; `/gadd:verify` marks verified separately. |
| Verification reports whether child work is ready to mark done, archive, and close externally. | 1, 4 | `/gadd:verify` skill and `verification.md` template include closure recommendation and evidence summary. |
| Closure is blocked when evidence is missing, checks fail, drift is detected, or external issue drift is unresolved. | 3, 4 | `/gadd:verify` stop conditions and report sections cover each blocker; validation checks command text. |
| When implementation evidence exists but closure is unapproved, GADD indicates verification as the next gate. | 3 | `/gadd:next` decision tree prioritizes verification-required child work. |
| Verification is specific to child Work Item closure and not a general healthcheck. | 1, 4, 5 | Command description, README, and validation use child Work Item closure language and avoid healthcheck framing. |
| Workflow remains local-ledger-first and does not require external skills or agent-specific orchestration. | 1, 4, 5 | Validation continues to ban external skill dependency language; command package includes standalone verify instructions. |

## Files / Modules

| File/module | Expected change | Reason |
| --- | --- | --- |
| `agent-skills.json` | Add `gadd-verify` skill and adapter metadata. | Make `/gadd:verify` installable from the canonical manifest. |
| `skills/gadd-verify/SKILL.md` | New standalone verification command contract. | Implement the verification gate. |
| `skills/gadd-verify/agents/openai.yaml` | New OpenAI/Codex adapter metadata. | Keep command package parity. |
| `commands/gadd/verify.md` | New Claude Code slash-command adapter. | Route Claude command to canonical skill. |
| `commands/gadd/verify.toml` | New Gemini CLI command adapter. | Route Gemini command to canonical skill. |
| `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` | Add verify command entry if required by current plugin shape. | Keep Claude plugin install complete. |
| `gemini-extension.json` and `GEMINI.md` | Add verify command surface. | Keep Gemini extension complete. |
| `README.md` | Add `/gadd:verify` to commands, install list, workflow, and source-of-truth notes. | Document the new phase. |
| `CONTEXT.md` | Add verification, closure, execution context terms and relationships. | Keep domain language precise. |
| `docs/superpowers/specs/2026-05-12-local-ledger-mvp-design.md` | Update MVP flow and schema notes. | Keep the current workflow design aligned. |
| `skills/gadd-setup/SKILL.md` | Include `verification.md` template in setup output. | Ensure new target repos receive the report template. |
| `skills/gadd-setup/assets/templates/ledger.yml` | Add optional `execution_context`, `artifacts.verification`, and `closure` shape. | Provide canonical template for new ledgers. |
| `skills/gadd-setup/assets/templates/verification.md` | New verification report template. | Standardize closure-gate output. |
| `gadd/templates/ledger.yml` and `gadd/templates/verification.md` | Mirror source templates for this dogfood repo. | Keep installed target templates current. |
| `skills/gadd-next/SKILL.md` | Add decision logic for verification-required child work and `execution_context`. | Route work to `/gadd:verify`. |
| `skills/gadd-implement/SKILL.md` | Clarify implementation completion evidence and verification-required closure status. | Keep implementation from closing work directly. |
| `scripts/validate-gadd-mvp.sh` | Require verify files and key contract text; keep external-skill dependency ban. | Protect package completeness. |
| `gadd/work-items/_archive/GADD-0001-verify-context-header/ledger.yml` | Mark SDD approved, plan drafted, and current gate as plan review. | Keep dogfood workflow state current. |

If implementation discovers different touch points, explain the variance in the implementation PR body.

## Test Strategy

Describe the minimum credible test set before coding starts.

- Unit tests:
  - None expected; this repo is primarily a command-skill package.
- Integration/contract tests:
  - Extend `./scripts/validate-gadd-mvp.sh` to require `/gadd:verify` package files, adapters, manifest entries, template files, and standalone command contract wording.
  - Keep existing JSON validation for package manifests.
  - Add validation checks for `execution_context`, `closure`, `verification.md`, and child Work Item closure language.
- Regression tests:
  - Existing validation must still pass for setup/next/scope/elaborate/refine/design/plan/decompose/implement.
  - Existing external skill dependency ban remains active.
- Manual checks:
  - Review hostile scenarios:
    - Child has implementation evidence but no verification: `/gadd:next` should point to `/gadd:verify`.
    - Verification evidence missing: `/gadd:verify` blocks closure.
    - Checks failed: `/gadd:verify` blocks closure.
    - External drift unresolved: `/gadd:verify` blocks external close.
    - Verification passed: child can be recommended for human-approved archive/external close.
  - Confirm adapter files remain thin routers and do not duplicate behavior.
- Not testing, with reason:
  - No live GitHub/Linear/Jira closure path in this MVP; external sync engines remain out of scope.
  - No actual multi-agent execution; orchestration is explicitly out of scope.

Quality bar: tests prove behavior and contract conformance, not internal line-by-line implementation.

## Planned Vertical Slices For `/gadd:decompose`

The child Work Items should follow the five slices above. Suggested classifications:

| Child Work Item | Type | Blocked by | Notes |
| --- | --- | --- | --- |
| Add `/gadd:verify` package surface | Autonomous | None | Mostly manifest/adapter/package plumbing. |
| Add ledger execution context and verification templates | Autonomous | None | Template and glossary work with narrow validation. |
| Teach `/gadd:next` and `/gadd:implement` the verification gate | Autonomous | Package surface and ledger template slices | Command semantics update. |
| Define `/gadd:verify` workflow and report contract | Autonomous | Package surface and template slice | Core verification skill behavior. |
| Update docs and validation for end-to-end workflow | Human-review | Prior slices | Cross-cutting docs/validation review; human should inspect language. |

## Review Checklist

- [x] The plan only implements the approved PRD and SDD.
- [x] Every PRD acceptance criterion maps to at least one slice and verification.
- [x] Every SDD interface/contract change appears in a slice.
- [x] Migration, compatibility, observability, and security/privacy work is included or explicitly not needed.
- [x] Slice order is dependency-safe and reviewable.
- [x] Any newly discovered architecture decision has been moved back to the SDD/ADR process.
