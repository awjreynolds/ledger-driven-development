---
work item: GADD-0002
prd: gadd/work-items/GADD-0002-pm-command-facilitation/prd.md
sdd: gadd/work-items/GADD-0002-pm-command-facilitation/sdd.md
created: 2026-05-13
updated: 2026-05-13
plan_html: gadd/work-items/GADD-0002-pm-command-facilitation/plan.html
adrs: []
---

# Implementation Plan: Strengthen GADD PM command facilitation

## Review Context

This plan translates the approved PRD and SDD into executable slices. It does not introduce new architecture decisions. The implementation changes command contract text only.

### PRD Summary

- Source: `gadd/work-items/GADD-0002-pm-command-facilitation/prd.md`
- Goals covered:
  - Strengthen `/gadd:scope`, `/gadd:elaborate`, and `/gadd:refine` as guided Product Manager workflows.
  - Preserve Product Manager boundaries and prevent solution-smuggling.
  - Keep PM facilitation self-contained inside each command-shaped skill.
  - Allow new draft scoping when no active draft exists, even if promoted Work Items are incomplete.
  - End each PM command with an explicit handoff gate.
- Non-goals to protect:
  - No external skill dependency.
  - No monolithic PRD command.
  - No changes to downstream engineering command ownership.
  - No duplicate workflow state.
  - No accidental mutation of unrelated promoted Work Items.

### SDD Summary

- Source: `gadd/work-items/GADD-0002-pm-command-facilitation/sdd.md`
- Design decisions to implement:
  - Embed the same minimal facilitation protocol shape in all three PM command skills.
  - Add phase-specific quality bars and anti-pattern checks.
  - Add explicit exit gates.
  - Keep adapter and manifest contracts unchanged.
- Interfaces/contracts to preserve:
  - `skills/gadd-*/SKILL.md` files are canonical.
  - Command adapters stay thin.
  - Repo-local ledgers remain canonical.
  - External tracker mutations still require human confirmation.
- Migration/compatibility requirements:
  - No schema migration.
  - Existing active Work Items remain valid.

### ADR Summary

- ADRs: []
- No ADR required; the design only clarifies existing command contracts.

## Slices

| Slice | Outcome | Files/modules | Tests/checks | Dependencies |
| --- | --- | --- | --- | --- |
| 1. Scope facilitation and draft-start contract | `/gadd:scope` clearly explains new-draft behavior, duplicate-draft handling, interaction modes, scope quality bar, and exit gate. | `skills/gadd-scope/SKILL.md` | `git diff --check`; manual grep for entry modes, duplicate draft behavior, no external skill dependency | None |
| 2. Elaborate facilitation and product-detail contract | `/gadd:elaborate` guides product detail inside existing scope and rejects scope expansion or implementation-specific criteria. | `skills/gadd-elaborate/SKILL.md` | `git diff --check`; manual grep for entry modes, problem/users/stories/draft criteria, no code-design input | Slice 1 only for shared wording consistency |
| 3. Refine facilitation and handoff contract | `/gadd:refine` guides handoff quality, resolves/owns questions, keeps acceptance criteria product-facing, and prompts PRD approval/promotion. | `skills/gadd-refine/SKILL.md` | `git diff --check`; manual grep for entry modes, quality checklist, approval prompt, no external skill dependency | Slices 1-2 for shared wording consistency |
| 4. Validation and Work Item evidence | GADD Work Item state records implementation evidence and the changed PM command contracts can be checked without relying on chat history. | `gadd/work-items/GADD-0002-pm-command-facilitation/children/*/ledger.yml`, optional validation script only if safe with concurrent work | `git diff --check`; targeted grep checks across the three PM skill files | Slices 1-3 |

Slice quality bar:

- Each slice changes one PM command surface or records implementation evidence.
- No slice adds a new external dependency.
- No slice changes engineering command ownership.
- No slice writes duplicate workflow state.

## Acceptance Criteria Traceability

| Acceptance criterion | Slice(s) | Verification |
| --- | --- | --- |
| New scoping can start when no active draft exists even if another promoted Work Item is incomplete. | 1 | `/gadd:scope` contract states promoted Work Items do not block new scoping and no active draft creates a draft. |
| New scoping does not mutate a promoted Work Item unless explicitly identified. | 1 | `/gadd:scope` contract states promoted Work Items are not updated unless identified. |
| Existing active draft blocks accidental duplicate scoping. | 1 | `/gadd:scope` stop conditions require resolving the existing draft. |
| PM commands provide self-contained guided interaction without external skills. | 1, 2, 3 | Each command embeds the facilitation protocol and no external skill dependency language is introduced. |
| PM commands offer guided, context-dump, and best-guess modes. | 1, 2, 3 | Each command names the three modes and assumption handling. |
| PM commands preserve ownership boundaries. | 1, 2, 3 | Each command has a phase-specific quality bar and anti-pattern list. |
| Product-facing acceptance criteria avoid technical design or command mechanics. | 2, 3 | `/gadd:elaborate` and `/gadd:refine` preserve product-facing criteria rules. |
| Each PM command ends with an explicit handoff gate. | 1, 2, 3 | Each command states artifact, ledger transition, questions, next command, and human decision. |
| No duplicate progress logs, session logs, or global workflow state. | 1, 2, 3, 4 | No implementation slice introduces new state files; verification checks focus on skill text and Work Item ledgers. |

## Files / Modules

| File/module | Expected change | Reason |
| --- | --- | --- |
| `skills/gadd-scope/SKILL.md` | Add facilitation protocol, quality bar, and exit gate for scope. | Main scope command behavior. |
| `skills/gadd-elaborate/SKILL.md` | Add facilitation protocol, quality bar, and exit gate for elaboration. | Main product-detail command behavior. |
| `skills/gadd-refine/SKILL.md` | Add facilitation protocol, quality bar, and exit gate for refinement. | Main handoff command behavior. |
| `gadd/work-items/GADD-0002-pm-command-facilitation/children/*` | Add child Work Item ledgers and implementation evidence. | Preserve GADD traceability. |

If implementation discovers different touch points, explain the variance in the implementation evidence.

## Test Strategy

- Unit tests: none; this is command-contract Markdown.
- Contract checks:
  - `git diff --check`
  - grep each PM skill for `Facilitation Protocol`, `Guided`, `Context dump`, `Best guess`, `Product Quality Bar`, and `Exit Gate`
  - grep for external skill dependency language and confirm none was introduced
- Regression checks:
  - Run `./scripts/validate-gadd-mvp.sh` if unrelated working-tree changes do not block it.
  - If unrelated working-tree changes block the full validator, report that separately and run targeted checks for this Work Item.
- Manual review:
  - Ensure `/gadd:scope` still creates one active draft and protects promoted Work Items.
  - Ensure `/gadd:elaborate` does not expand goals/non-goals.
  - Ensure `/gadd:refine` keeps acceptance criteria product-facing and asks for PRD approval.

## Planned Vertical Slices For `/gadd:decompose`

| Child Work Item | Type | Blocked by | Notes |
| --- | --- | --- | --- |
| Add scope facilitation contract | Autonomous | None | Updates only `/gadd:scope` command text. |
| Add elaborate facilitation contract | Autonomous | Scope facilitation contract | Updates only `/gadd:elaborate` command text. |
| Add refine facilitation contract and evidence checks | Autonomous | Scope and elaborate facilitation contracts | Updates `/gadd:refine` and records targeted verification evidence. |

## Review Checklist

- [x] The plan only implements the approved PRD and SDD.
- [x] Every PRD acceptance criterion maps to at least one slice and verification.
- [x] Every SDD interface/contract change appears in a slice.
- [x] Migration, compatibility, observability, and security/privacy work is included or explicitly not needed.
- [x] Slice order is dependency-safe and reviewable.
- [x] Any newly discovered architecture decision has been moved back to the SDD/ADR process.
