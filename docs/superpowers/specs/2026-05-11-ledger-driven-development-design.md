# Ledger-Driven Development — Design

**Date:** 2026-05-11
**Status:** Draft, awaiting review
**Author:** awjreynolds (with AI-assisted brainstorming)

## 1. Thesis

Ledger-Driven Development (LDD) is the synthesis of three existing approaches to AI-assisted software engineering:

- **Matt Pocock's skills** — pragmatic AI-skill ergonomics, ledger-aware tooling, per-repo configuration.
- **QRSPI (Lavaee)** — structural alignment discipline, engineer-reviewed plans, ticket-blind research.
- **Agile SDLC** — role-aware artifact hierarchy (Initiative → PRD → Epic → Story → Task → PR), team-coordination semantics, stakeholder visibility.

LDD connects these under a single first principle: **the ledger is the source of truth, and the workflow lives as labelled state transitions on tickets that carry structured, role-owned, human-renderable artifacts.**

LDD is intentionally **agent- and model-agnostic**. The workflow lives in artifacts and labels on disk and in the ledger, not in any particular AI platform. Any modern coding agent capable of reading markdown and dispatching subagents (with fallback to phased prompting) can execute LDD.

## 2. The Gap Analysis

LDD exists because the existing approaches each leave concrete gaps when applied to team-shaped software work.

| # | Gap | Where it exists | LDD's answer |
|---|---|---|---|
| 1 | QRSPI has no ledger and no roles | QRSPI is solo-engineer-shaped | Wrap QRSPI's phase rigour in agile artifacts + role-owned sections |
| 2 | Pocock conflates PRD and plan | `/to-prd` produces one thing | Separate PRD (the *what*) from plan (the *how*); different artifacts, different reviewers |
| 3 | Pocock's grilling is unbounded | One large PRD grill, scope creeps | Bounded grills per section, per role; each enforces a role's surface area only |
| 4 | Agile SDLC has no structural alignment depth | "Acceptance criteria" ≠ technical alignment | Insert QRSPI's research + plan-review gates *before* implement — operationalised as a plan-PR |
| 5 | No approach renders artifacts for humans | All ship raw markdown | Structured-source → HTML view as the cognitive-load lever |
| 6 | PRD-in-issue doesn't scale to JIRA | Walls-of-text in ticket descriptions | Ticket-as-index + repo-committed artifacts decouples ledger UX from artifact depth |
| 7 | None reconcile stakeholder vs engineer views | Engineers want depth; TPMs want summary | Macro × micro phases + label namespaces give both audiences a view of the same ticket |
| 8 | Cognitive overload at code review | Plan and code reviewed together, late | Shift review to plan-PR; code-PR becomes a spot-check |
| 9 | None handle epic → ticket decomposition with carried context | Pocock's `/to-issues` is one-shot, loses parent framing | `/ldd:scope` Branch C (decomposition) preserves parent PRD context as inherited frontmatter and scope envelope |
| 10 | None offer a clean trunk of traceability | Spec ↔ plan ↔ PR ↔ release links are manual | Labels + frontmatter create a graph: ticket ↔ design.md commit ↔ plan-PR ↔ code-PR |

## 3. What LDD is *not*

- **Not a wrapper around Pocock.** Borrows the ergonomic patterns (per-repo setup, ledger backends, label-driven state); ships its own skill set tuned to LDD's model.
- **Not a code-generation tool.** It's an alignment + traceability tool that produces code as a side effect.
- **Not a JIRA plugin.** Ledger-agnostic by design.
- **Not a methodology document.** Executable skills + templates + a small renderer.
- **Not a replacement for craft skills.** Disciplines like TDD and bug-diagnosis live inside LDD's workflow skills (`/ldd:implement`, `/ldd:design`). Users who want pure-discipline tools can install Pocock or others alongside; namespacing prevents conflict.
- **Not Scrum-dependent.** Scrum-compatible — labels can mirror sprint board columns — but the workflow runs on artifact state, not sprint cadence. AI is hollowing out coordination ceremonies; LDD doesn't depend on them existing.

## 4. Architecture

### 4.1 Six moving parts

1. **Ledger** — source of truth for ticket *status*. JIRA, GitHub Issues, Linear, or local files (chosen at setup).
2. **Artifacts** — source of truth for ticket *content*. Committed markdown in `docs/tickets/<KEY>/`, with auto-generated HTML companions.
3. **Labels** — universal state machine. Works identically across ledger backends.
4. **Skills** — bounded, atomic, portable markdown operations.
5. **Health checks + overrides** — gates by default, escape on record.
6. **Subagent dispatch + tier-based model selection** — platform-adaptive orchestration.

### 4.2 Core abstraction

LDD models software work as a directed graph of artifacts anchored to ledger tickets:

```
                     ┌────────────────┐
                     │  Ledger ticket │  ← source of truth (status, labels, links)
                     │  (GH/JIRA/...) │
                     └───────┬────────┘
                             │ links to
                             ▼
  docs/tickets/PROJ-123/
  ├── ticket.md            ← role-owned sections, mirrors ledger content
  ├── design.md → .html    ← architectural decisions, structure outline
  ├── plan.md   → .html    ← ordered execution slices (reviewed via plan-PR)
  ├── progress.md          ← appended during implement
  ├── audit.yml            ← append-only invocation log
  └── (optional) prd.md   ← inherited from parent epic, frontmatter-linked
```

The ledger holds *status*; the repo holds *content*. Conflicts resolve to repo for content, ledger for state.

### 4.3 The two-PR pattern (plus PRs for epic-scale events)

```
ticket created ──► /ldd:triage (bugs only) ──► /ldd:scope ──► /ldd:elaborate ──► /ldd:refine ──► /ldd:design ──► /ldd:plan
                                                                                                                    │
                                                                                                                    ▼
                                                                                                             ┌──────────────┐
                                                                                                             │  Plan PR     │  ← engineer reviews
                                                                                                             │  (plan.md)   │     before any code
                                                                                                             └──────┬───────┘
                                                                                                                    │ merged
                                                                                                                    ▼
                                                                                                             /ldd:implement
                                                                                                                    │
                                                                                                             opens  ▼
                                                                                                             ┌──────────────┐
                                                                                                             │  Code PR     │  ← spot-check
                                                                                                             │  (impl+tests)│     (alignment already done)
                                                                                                             └──────────────┘
```

Story-level tickets: two PRs (plan-PR, code-PR). Scope, elaborate, and refine commit to main; their effects are visible at the plan-PR review gate.

Epic-level work involves additional PRs:
- **PRD-PR** — opened when `/ldd:refine` completes PRD polishing; reviewed by PM/EM/stakeholders before decomposition
- **Decomposition-PR** — opened by `/ldd:scope` when it slices an approved PRD into child tickets; reviewed before child tickets enter the workflow
- **Design-PR** (optional per-child) — opened by `/ldd:design` so architectural decisions are reviewed before the execution plan is written

The progression: scope sets boundaries; elaborate produces first-draft content; refine sharpens it. Then design and plan create the technical contract; implement turns the contract into code. Each gate reviews a different concern at a different cognitive scale.

### 4.4 Health checks with overrides (cross-cutting)

Every LDD skill follows this shape:

```
┌───────────────────────────────────────────────────────────────────────┐
│  Skill execution                                                      │
├───────────────────────────────────────────────────────────────────────┤
│  1. Preflight checks   (refuse if invalid; suggest fix)               │
│  2. Body               (the actual work)                              │
│  3. Phase-local self-review   (skill-specific quality checks; see §6) │
│  4. Postcondition verification   (was the work durable?)              │
│  5. Audit record   (frontmatter / ticket comment)                     │
└───────────────────────────────────────────────────────────────────────┘
```

**Override classes.** Not all checks are equally negotiable. LDD distinguishes three override surfaces:

| Class | Flag | What it bypasses | Audit weight |
|---|---|---|---|
| **Preflight override** | `--override-preflight="<reason>"` | Preflight check refusals (e.g., wrong phase label, missing parent artifact) | Logged in audit + ticket comment |
| **Self-review override** | `--override-review="<reason>"` | Phase-local self-review failures (e.g., an AC the skill judged non-testable) | Logged in audit + ticket comment + explicit `review-overridden:true` flag in artifact frontmatter |
| **Hotfix override** | `--hotfix="<incident-ref>"` | Multiple preconditions across the workflow (skips phases entirely; see §7.3); requires an incident reference | Logged + opens a follow-up "retroactive artifact" ticket linked to the original |

Some checks are **halt-only** — no override class accepts them. These cover invariants that must not be violated for the workflow to remain coherent:

- Tests fail in `/ldd:implement` (red tests must be green before code-PR; no override produces green CI on broken tests)
- Worktree contains uncommitted unrelated changes (override `--allow-dirty="<reason>"` exists but applies *only* to specific known files; can't blanket-skip)
- Scope-locked region modified without `/ldd:scope` invocation (mechanical guard; halts unconditionally)
- Postcondition verification failure (the work didn't durably land — fix the underlying issue, don't override)

Overrides of any class are captured durably in artifact frontmatter and mirrored as a ticket comment. **Overrides of the right class are always allowed; they are never silent. Halt-only checks have no override path.**

**Phase-local self-review** runs *before* commit/PR for any writing skill. Each writing skill defines its own checks (see Section 6 — for example, `/ldd:elaborate` checks no scope expansion; `/ldd:refine` checks AC are testable; `/ldd:design` checks no scope smuggling and risk-appropriate concerns). Self-review failures halt the skill and surface the specific violation rather than silently weakening checks. Self-review is the answer to "how do we keep each phase honest without external review at every step?" — commit timing stays aggressive (ledger-driven model), but each phase polices itself before committing.

`--dry-run` runs preflight + self-review reporting only, without committing — useful for CI gates and "what would `/ldd:refine` complain about if I ran it now?" queries.

### 4.5 Subagent dispatch and model tiers

LDD skills are *orchestrators*. The main agent does coordination + final synthesis; subagents do heavy lifting in isolated context windows. This enables:

- **Ticket-blind research** — fresh-context subagent investigates the codebase with no ticket reference, then findings are synthesised back into the main agent's context.
- **Parallel alternatives exploration** — multiple subagents explore design options concurrently.
- **Cost-aware routing** — different sub-tasks dispatched to different model tiers based on cognitive load required.

Three model tiers:

| Tier | Purpose |
|---|---|
| `fast` | High-volume, pattern-matching, low-stakes |
| `balanced` | Structured generation, conversation, most operational work |
| `reasoning` | High-leverage decisions, synthesis, alternatives weighing |

Users map tiers to their platform's available models at setup time. Skills only reference tiers — never concrete model IDs.

For platforms without subagent primitives, LDD falls back to **phased prompting** (the main agent is instructed to investigate without referencing the ticket as a first phase, then revealed the ticket as a second phase). Lower rigour but workable.

## 5. Phase Model

### 5.1 Eight macro phases

Tickets move through these phases. Each is represented by a `phase:*` label.

| Phase | Label | What happens | When |
|---|---|---|---|
| Scoping | `phase:scoping` | Boundary decisions — PRD goals/non-goals, ticket out-of-scope, epic decomposition into children | Pre-sprint |
| Elaboration | `phase:elaboration` | First-pass detail — drafts of problem framing, user stories, AC, success metrics, affected modules | Pre-sprint |
| Refinement | `phase:refinement` | Polish and sharpen — testable AC, measurable metrics, resolved ambiguities, edge cases, verified module pointers | Pre-sprint |
| Design | `phase:design` | Codebase research + architectural decisions + structure outline → `design.md` | In-sprint |
| Plan | `phase:plan` | Ordered execution slices → `plan.md`, plan-PR opened | In-sprint |
| Implement | `phase:implement` | TDD execution following the merged plan, code-PR opened | In-sprint |
| Verify | `phase:verify` | PR review + CI + acceptance-criteria validation | In-sprint |
| Close | `phase:close` | Ticket closed, traceability complete | In-sprint |

**Why three pre-design phases:** scoping (boundary), elaboration (first draft), and refinement (polish) are distinct cognitive activities. Scoping decisions are costly to reverse; elaboration produces content within boundaries; refinement sharpens content for testability. Conflating them into one skill loses the separation of concerns and re-introduces scope creep risk.

### 5.2 Label namespaces

Universal across ledger backends. Set/modified by skills and PR-merge webhooks.

- **`phase:*`** — current macro phase (mutually exclusive)
- **`kind:*`** — `bug`, `feature`, `refactor`, `epic`
- **`risk:*`** — `low`, `med`, `high`
- **`plan:*`** — `draft`, `in-review`, `approved`
- **`gate:*`** — sticky markers that a gate cleared (`gate:prd-approved`, `gate:design-approved`, `gate:plan-approved`, `gate:tests-green`)
- **`triage:*`** — `accepted`, `needs-info`, `duplicate-of:#N`, `wontfix` (bug intake only)

Setup maps these canonical labels to ledger-specific strings (since JIRA labels ≠ GH labels ≠ Linear labels).

### 5.3 Board column mapping

`/ldd:setup` writes a default mapping that users override to match their existing board:

```
phase:scoping     → "Scoping"
phase:elaboration → "Elaboration"
phase:refinement  → "Ready"
phase:design      → "Design"
phase:plan        → "Plan in Review"
phase:implement   → "In Progress"
phase:verify      → "In Review"
phase:close       → "Done"
```

Many teams collapse scoping/elaboration/refinement into a single "Backlog" or "Ready" column on the visible board, with the phase label distinguishing them internally. The default mapping above keeps them separate; collapse via the override at setup time if your team prefers fewer columns.

### 5.4 Ceremony controls

LDD keeps the cognitive phases, but scales the ceremony around them. The rule is: **do not collapse the thinking boundaries; collapse unnecessary handoffs, questions, and artifact bulk.**

**Risk-tiered depth.**

| Risk | Workflow depth | Default review posture |
|---|---|---|
| `risk:low` | Compressed artifacts; ticket-blind research off unless brown-field; one design option acceptable; `plan.md` usually 1-2 slices | `/ldd:prepare` may run scope → elaborate → refine → design → plan in one invocation; plan-PR optional by team config |
| `risk:med` | Normal LDD path; bounded questions; 2-3 design alternatives where useful | Plan-PR required; package review by PR description/checklist |
| `risk:high` | Full research; alternatives mandatory; migration/backward-compat, rollout/revert, observability required | Plan-PR required; stricter self-review; no compressed wrapper unless `--override-preflight` records why |

**Question budgets.** Skills ask only the questions needed for their phase. When a budget is exhausted, the skill must proceed with an explicit assumption, capture an open question with an owner, or halt if the missing answer is a halt-only invariant.

| Skill | Default budget |
|---|---|
| `/ldd:scope` | 3 questions |
| `/ldd:elaborate` | 5 questions |
| `/ldd:refine` | 2 questions; mostly self-review/research |
| `/ldd:design` | 2 questions after codebase research |
| `/ldd:plan` | 0 questions unless a contradiction is found |

**Artifact budgets.** The rendered artifact should be deep enough to review, not large enough to become a second project.

- `risk:low` ticket scope: 3-5 bullets; AC: 1-4 criteria; design: one screen/page; plan: 1-2 slices.
- `risk:med` ticket scope: 3-7 bullets; AC: 3-8 criteria; design: up to three screens/pages unless complexity demands more; plan: enough slices that each lands a green test.
- `risk:high` has no fixed size limit, but every extra section must map to a concrete risk trigger.

**Escalation triggers.** Extra ceremony requires a reason. Full treatment is triggered by `risk:high`, external dependencies, data migration, security/auth/payment/privacy impact, cross-team ownership, production-path changes, previous incident/regression area, or ambiguous ownership. If none apply, the skill should default to the lightest artifact that satisfies its self-review.

**Ceremony metrics.** `audit.yml` records question count, artifacts touched, PRs opened, elapsed time before implementation, override flags used, and whether `/ldd:prepare` was used. These are reviewable at retro time. If low-risk tickets regularly require many questions or multiple PRs, the process is too heavy and setup defaults should be adjusted.

## 6. Skill Inventory

Eight macro skills plus one convenience wrapper. Each macro skill is a single user-facing verb that orchestrates internal sub-steps and subagent dispatches. The wrapper reduces handoffs for low-risk work without changing the underlying artifacts.

### 6.0 Skill ↔ phase mapping at a glance

| Skill | Applies to | Phase transition produced | Notes |
|---|---|---|---|
| `/ldd:setup` | repo, one-time | — | Bootstrap; not part of any ticket's phase flow |
| `/ldd:triage` | `kind:bug` only | (unlabelled) → `phase:scoping` | Continuous; not sprint-bound |
| `/ldd:scope` | any artifact | `phase:scoping` → `phase:elaboration` (for stories); also produces decomposition (for epics) | Sets boundaries: PRD goals/non-goals, ticket out-of-scope, epic→child decomposition |
| `/ldd:elaborate` | any ticket | `phase:elaboration` → `phase:refinement` | First-pass detail-filling within scoped envelope |
| `/ldd:refine` | any ticket | `phase:refinement` → `phase:design` | Polishes drafts — makes AC testable, metrics measurable, ambiguities resolved |
| `/ldd:design` | any ticket with `phase:design` | `phase:design` → `phase:plan` | Subagent-driven ticket-blind research by default |
| `/ldd:plan` | any ticket with `phase:plan` | `phase:plan` → (via plan-PR merge) `phase:implement` | Opens plan-PR |
| `/ldd:implement` | any ticket with `phase:implement` + `gate:plan-approved` | `phase:implement` → `phase:verify` → (on code-PR merge) `phase:close` | Opens code-PR; TDD-driven |
| `/ldd:prepare` | `risk:low` ticket by default | Runs scope → elaborate → refine → design → plan in one invocation | Convenience wrapper; writes the same artifacts, respects self-review and budgets, records `prepared_by_wrapper:true` |

Verify and close are not skills — they happen via PR review + CI + automated label flips on merge.

**Why scope, elaborate, and refine are three skills:** these are three distinct cognitive activities. **Scope** sets boundaries — a high-stakes decision that's costly to reverse. **Elaborate** produces first-draft content within boundaries — generative, low-stakes. **Refine** polishes the draft for testability and clarity — convergent, low-stakes but high-precision. Conflating them lets scope creep in via "while I'm refining I might as well also expand…"; separating them forces explicit boundary decisions that elaboration and refinement honour.

**Why `/ldd:prepare` exists:** low-risk work should not require five manual handoffs to preserve five thinking boundaries. The wrapper executes the same sequence, runs each phase-local self-review, writes the same artifact set, and stops at the first failed check. It is disabled by default for `risk:high`; teams can also disable it entirely in setup if they want every phase manually invoked.

### 6.1 `/ldd:setup` — bootstrap

**Inputs:** invoked once per repo; user answers configuration questions interactively.

**Outputs:**
- `.ldd/config.yml` — ledger backend, render target, label mapping, role definitions, board column mapping, model tier resolution
- `.ldd/labels.yml` — canonical labels mapped to ledger-specific strings
- `.ldd/templates/{bug,feature,refactor,epic}.md` — ticket templates per kind
- `.ldd/renderer/` — HTML rendering templates
- `.github/workflows/ldd-render.yml` (or platform equivalent) — CI hook to regenerate HTML on commit
- `docs/tickets/` — directory created
- Canonical labels created in the ledger via API

**Re-runnable:** yes, idempotent.

### 6.2 `/ldd:triage` — bug intake (orthogonal)

**Inputs:** a `kind:bug` ticket (or unlabelled ticket suspected to be a bug).

**Process:**
1. Attempt reproduction (subagent, `fast` tier)
2. Detect duplicates by signature (subagent, `fast` tier)
3. Recommend severity and decision (`balanced` tier)

**Outputs:**
- Ticket labels: `kind:bug`, `risk:*`, one of `triage:accepted` | `triage:needs-info` | `triage:duplicate-of:#N` | `triage:wontfix`
- If accepted: also sets `phase:scoping` (the bug then walks through scope → elaborate → refine like any other ticket; triage only assesses validity and severity, not scope), creates `docs/tickets/PROJ-NNN/` skeleton
- Ticket comment with triage notes (repro outcome, severity reasoning, duplicate links)
- Audit record

**Continuous, not sprint-bound.** Bugs arrive on their own schedule.

### 6.3 `/ldd:scope` — boundary-setting (three internal branches)

The skill detects input type and branches internally:

```
input is conversation context only (no ticket reference)              → Branch A (new PRD scope)
input is a ticket with kind:epic AND no prd.md                        → Branch A (new PRD scope)
input is a ticket with kind:epic AND gate:prd-approved set            → Branch C (decompose)
input is a ticket with kind:feature|refactor|bug AND no scope set     → Branch B (ticket scope)
input is an already-scoped ticket needing scope adjustment            → Branch B (re-scope)
none of the above                                                      → refuse with helpful error
```

Users can force a specific branch with `--as=prd-scope|ticket-scope|decompose`.

**Branch A: PRD scope** (input: idea/chat OR epic ticket without PRD)
- Bounded grill at PRD-boundary scope (`balanced` tier): asks only about goals, non-goals, success criteria envelope. Does *not* ask about user stories, AC, or detail — those are elaboration's job.
- Outputs: `docs/tickets/PROJ-NNN/prd.md` with **only the Goals and Non-goals sections filled**; remaining sections marked as placeholders for `/ldd:elaborate`; new epic ticket if absent; `kind:epic`, `phase:scoping`
- Sets `phase:scoping` → `phase:elaboration` on completion

**Branch B: Ticket scope** (input: ticket with `kind:feature|refactor|bug`)
- Bounded grill at ticket-boundary scope (`balanced` tier): asks only about out-of-scope, sizing, dependencies. Does *not* ask about problem framing, AC, or affected modules.
- Outputs: `ticket.md` with **only the Out-of-scope section filled** (plus optional `risk:` and `depends_on:` frontmatter)
- Sets `phase:scoping` → `phase:elaboration` on completion

**Branch C: Decomposition** (input: epic with `gate:prd-approved`)
- Slices the approved PRD into proposed child tickets (`reasoning` tier — bad decomposition costs days)
- **Does not create ledger child tickets immediately.** Instead, creates each proposed child as a `docs/tickets/PROJ-NNN/ticket.md` file on a `ldd/decompose/PROJ-100` branch, with `kind:feature`, `parent: PROJ-100`, frontmatter inheriting parent context, and the Out-of-scope section pre-populated from the slice boundary
- **Opens the decomposition-PR** with all proposed child `ticket.md` files for reviewer sign-off
- On decomposition-PR merge: ledger child tickets are created (via the merge webhook or a post-merge CI job), each labelled `kind:feature`, `parent: PROJ-100`, **`phase:elaboration`** (scope already inherited from decomposition — children skip `/ldd:scope` and start at `/ldd:elaborate`); parent epic gets `decomposed:true` + child links
- This create-on-merge sequencing prevents the "ticket exists in ledger but scope envelope rejected by reviewer" race condition

**Pre-commit self-review** (every branch runs this before commit/PR):
- Branch A: are goals measurable? Are non-goals concrete (not "general improvements")? Are the goals + non-goals together a complete envelope (no obvious adjacent areas left ambiguous)?
- Branch B: is out-of-scope concrete (specific things, not vague categories)? Is sizing realistic?
- Branch C: does each child have a minimum-viable scope envelope? Does any child duplicate another's scope? Does the union of child scopes equal the PRD scope minus explicitly-deferred items?

Failures halt the skill and surface the issue; the engineer either fixes the input or, for non-halt-only review failures, invokes `--override-review="<reason>"`.

**Why scope is its own skill:** boundary decisions get made *cleanly*, without bleed-over into detail-filling. A reviewer of a decomposition-PR is asked exactly one question — "are these the right boundaries?" — not also "are the AC well-formed?". Each gate reviews one concern.

### 6.4 `/ldd:elaborate` — first-pass content

**Inputs:** an artifact with `phase:elaboration` (scope already set).

**Process:**
1. Read the scoped artifact (PRD or ticket) — Goals/Non-goals or Out-of-scope already present
2. Bounded grill at *content* scope (`balanced` tier): asks the questions that produce first-draft content for the remaining sections. Crucially, the grill *cannot* propose changes to scope sections — they're locked.
3. Generate first-draft content for each unfilled section

**Pre-commit self-review** (runs before committing the elaborated artifact):
- All new content lies *outside* scope-locked regions
- Any placeholders left in are intentional (e.g., awaiting human input on a decision) and explicitly flagged in the section
- No new tickets were created (decomposition is scope's job)
- No content implicitly expands scope (e.g., a user story that requires a goal not in the locked Goals section)
- All required sections for this artifact kind have at least a first-draft entry (no silently empty sections)

Failure of any check halts the skill and surfaces the specific violation. Common remediation: re-run `/ldd:scope` to address a scope gap, then re-run `/ldd:elaborate`.

**Outputs (PRD):** `prd.md` with Problem, User stories, Success metrics, Open questions sections filled (first draft); status `phase:elaboration` → `phase:refinement`

**Outputs (ticket):** `ticket.md` with Problem framing, Acceptance criteria, Affected modules sections filled (first draft); status `phase:elaboration` → `phase:refinement`

**No PR.** First-draft content commits to main; reviewers see it polished by `/ldd:refine` before any review gate.

**Constraints:**
- Cannot modify scope sections (Goals/Non-goals/Out-of-scope) — those are locked as `# scope-locked` regions; if elaboration surfaces a scope problem, the skill halts and recommends re-running `/ldd:scope` with the discovered issue
- Cannot create new tickets (decomposition is scope's job, not elaboration's)

### 6.5 `/ldd:refine` — polish and sharpen

**Inputs:** an artifact with `phase:refinement` (scope and elaboration already done).

**Process:**
1. Read the elaborated artifact
2. Pass through each non-scope section and apply polish:
   - **Acceptance criteria** → make each criterion testable; flag any with subjective language ("intuitive", "fast")
   - **Success metrics** → make each measurable; require units and a baseline
   - **User stories** → tighten to "As X I want Y so Z" form; remove vague qualifiers
   - **Problem framing** → ensure it's user-facing, not solution-facing
   - **Affected modules** → verify against the codebase (subagent pass, `fast` tier); flag any that don't exist or have moved
   - **Open questions** → either resolve via codebase research or escalate explicitly
3. Edge case sweep (`balanced` tier): for each AC, propose 2–3 edge cases worth testing; add to AC or to a separate Edge cases section

**Pre-commit self-review** (runs before committing the refined artifact / opening the PRD-PR):
- Every acceptance criterion is testable — concrete subject, concrete verb, concrete expected outcome, no subjective qualifiers
- Every success metric has units, a measurement method, and a baseline value
- Every "affected module" path was verified to exist in the codebase (or explicitly marked as new)
- Every open question is either resolved (with the resolution captured) or explicitly escalated (with the owner named)
- Scope-locked sections were not modified
- No new content was added beyond polish — only sharpening of elaboration output

Failure surfaces the specific violation. Common remediation: escalate an unresolved question to a human rather than inventing an answer.

**Outputs:**
- Updated `prd.md` or `ticket.md` with polished content; status `phase:refinement` → `phase:design` on completion
- For PRDs: **PRD-PR opened** (`ldd/prd/PROJ-100` branch) containing the polished `prd.md` for PM/EM/stakeholder sign-off; PRD-PR merge sets `gate:prd-approved` and unblocks `/ldd:scope` Branch C (decomposition)
- For tickets: no PR — polished ticket.md commits to main; reviewed implicitly at design-PR or plan-PR

**Constraints:**
- Cannot modify scope sections (those are locked)
- Cannot add new high-level content (that's elaboration's job)
- Can surface ambiguities for human resolution but cannot resolve them by inventing answers

### 6.6 `/ldd:design`

**Inputs:** a ticket with `phase:design`.

**Process:**
1. **Ticket-blind research subagent** (`balanced` tier, fresh context, no ticket reference) characterises affected modules objectively. Default-on for `kind:bug`, `kind:refactor`, `risk:high`, and brown-field feature work. Off for green-field features in fresh modules. Overridable with `--research-mode=blind|sighted|skip`.
2. **Alternatives exploration** (parallel subagents, `balanced` tier) — 2–3 design options compared.
3. **Design synthesis** (main agent, `reasoning` tier) produces `design.md` with three mandatory sections:
   - **Research** — ticket-blind findings (objective characterisation of the codebase)
   - **Decisions** — chosen architectural approach with alternatives considered
   - **Structure** — proposed interface shape (signatures, types, module boundaries)

**Pre-commit self-review** (runs before committing `design.md` / opening any design-PR):
- The design satisfies every acceptance criterion in the refined ticket — for each AC, the design's Structure section either provides a code path that meets it or explicitly notes where it will (deferred to plan)
- Error handling is addressed — what happens on bad input, partial failure, timeout, retry; not just the happy path
- Test surface is addressed — what's unit-testable, what needs integration tests, what relies on external systems
- Data flow is traced — for each significant change in state, who writes, who reads, in what order
- No scope smuggling — the design does not introduce capabilities or modules not implied by the ticket's scope envelope; if scope expansion is genuinely needed, the skill halts and recommends re-running `/ldd:scope`
- For `risk:high` tickets: migration / backward-compat strategy, rollout/revert plan, and observability requirements are explicitly addressed

Failure surfaces the specific violation. The skill does not silently weaken a check.

**Outputs:**
- `docs/tickets/PROJ-NNN/design.md` → `design.html` (collapsible sections, diagrams, file pills)
- `phase:design` → `phase:plan` on completion
- For `kind:epic`: separate design-PR opened (`ldd/design/PROJ-NNN` branch) with `design.md`
- For story-level work (`kind:feature|refactor|bug`): no separate PR; `design.md` commits to main and is referenced (via link and summary in the plan-PR description) for reviewer awareness at the upcoming plan-PR gate. The plan-PR diff itself contains only `plan.md` — package review at the plan-PR is description-and-checklist-driven, not GitHub-diff-driven (see §6.7)
- On design-PR merge (epics only): `gate:design-approved`

### 6.7 `/ldd:plan`

**Inputs:** a ticket with `phase:plan` and `design.md` present.

**Process:**
1. Read design.md
2. Generate ordered vertical slices (`balanced` tier) — each slice with name, files touched, red-test description, acceptance for that slice
3. **Plan-review pass (built-in self-review)** (`reasoning` tier) — catches plan-reading illusions before commit:
   - Does each slice end with a green test that's traceable to an AC from the ticket?
   - Are slice file lists disjoint enough that slices can land independently?
   - Are slice dependencies acyclic and explicit (`blocked_by:` on each slice)?
   - Does the union of slices cover every AC from the refined ticket? No AC silently dropped?
   - Does the union of slices stay within the design's Structure section — no slices smuggling in unspecified components?
   - For `risk:high` tickets: does the plan include a slice for migration steps and a slice for revert verification?

Failure halts before commit. Plan-review is unique among writing skills in running its self-review at `reasoning` tier — plan flaws are expensive to discover at code-review time.

**Outputs:**
- `docs/tickets/PROJ-NNN/plan.md` → `plan.html`
- Branch `ldd/plan/PROJ-NNN` created
- **Plan-PR is description-and-checklist-driven for package review** (not GitHub-diff-driven):
  - The PR diff contains only `plan.md` — that's all GitHub will display in the Files tab
  - The PR description carries links and short summaries of the prior artifacts (`ticket.md` with scope+elaboration+refinement; `design.md` with research+decisions+structure) and is the primary surface for package evaluation
  - PR template includes two checklists: a "slice-by-slice" checklist (one box per plan slice) AND a "package coherence" checklist asking reviewers to confirm: does the plan honour the design; does the design satisfy the refined ticket; does the ticket sit cleanly inside its scope envelope; were any scope-locked regions touched
  - Reviewers click through the description links to read prior artifacts at their `@<sha>` commits; the description anchors the package, not the diff
- Ticket: `plan:in-review` set when PR opens
- On plan-PR merge: `plan:approved`, `gate:plan-approved`, `phase:implement`

### 6.8 `/ldd:prepare` — low-risk wrapper

**Inputs:** a ticket with `risk:low` and no unresolved halt-only preflight failures. Teams may allow `risk:med` via config; `risk:high` refuses unless `--override-preflight="<reason>"` is supplied.

**Process:**
1. Runs `/ldd:scope`, `/ldd:elaborate`, `/ldd:refine`, `/ldd:design`, and `/ldd:plan` in sequence inside one invocation.
2. Applies the question and artifact budgets from §5.4 at each phase.
3. Runs each phase-local self-review before moving to the next phase.
4. Stops immediately on any halt-only failure or exhausted question budget that cannot be converted into an explicit assumption/open question.

**Outputs:**
- The same `ticket.md`, `design.md`, and `plan.md` artifacts the macro skills would have written
- `audit.yml` records `prepared_by_wrapper:true`, per-phase question counts, per-phase elapsed time, and any assumptions made
- If team config has `low_risk_plan_pr: required`, opens the normal plan-PR
- If team config has `low_risk_plan_pr: auto_approve`, does not open a plan-PR; instead marks `plan:approved`, sets `gate:plan-approved`, moves to `phase:implement`, and writes `plan_auto_approved:true` plus the config reason into `plan.md` frontmatter and `audit.yml`

**Constraints:**
- The wrapper cannot skip phase-local self-review.
- The wrapper cannot create fewer artifacts; it can only keep them terse.
- The wrapper cannot auto-approve `risk:high`.
- Any scope expansion discovered after `/ldd:scope` still halts and recommends rerunning `/ldd:scope`; the wrapper does not blur scope boundaries.

### 6.9 `/ldd:implement`

**Inputs:** a ticket with `phase:implement` and `gate:plan-approved`.

**Process:**
1. Read approved plan.md
2. For each slice, walk TDD red → green → refactor:
   - Red test (`balanced` tier — test design quality matters)
   - Implementation code (`fast` tier; escalate to `balanced` on test failure)
   - Refactor pass (`balanced` tier)
3. Append progress per slice to `progress.md`
4. Post progress comment on ticket per completed slice
5. On all slices complete: code-PR self-review (see below)
6. On self-review pass: open code-PR

**Pre-PR self-review** (runs after all slices complete, before opening code-PR):
- Every slice in the plan has corresponding commits on the implementation branch
- Every plan-listed test file exists and passes
- No files were modified outside the plan's "files touched" list (any deviation → halt and request `--override-review="<reason>"`; unrelated dirty files remain halt-only unless explicitly covered by `--allow-dirty="<reason>"`)
- All ACs from the ticket have a passing test that maps to them (verified via test name matching or explicit traceability comments)
- For `risk:high` tickets: migration steps from the plan executed; revert steps documented in PR description
- `git status` clean on the implementation branch (no unstaged or untracked changes)

Failure halts and surfaces the violation. Common remediation: add a missing test, or invoke `--override-review="<reason>"` if the deviation is intentional and not halt-only (deviation is logged in the code-PR description).

**Outputs:**
- Code commits on branch `ldd/impl/PROJ-NNN`
- Test files (unit + integration as plan specified)
- `docs/tickets/PROJ-NNN/progress.md` — appended per slice
- Code-PR opened against main with frontmatter:
  ```yaml
  ticket: PROJ-NNN
  plan: docs/tickets/PROJ-NNN/plan.md@<sha>
  design: docs/tickets/PROJ-NNN/design.md@<sha>
  prd: docs/tickets/PROJ-100/prd.md@<sha>   # parent if applicable
  ```
- Ticket: `phase:implement` (in progress) → `phase:verify` when code-PR opens
- On code-PR merge: `gate:tests-green`, `phase:close`, ticket auto-closed

## 7. Workflow Sequences

### 7.1 Direct ticket (bug / feature / refactor without epic parent)

```
/ldd:triage (bugs only) ──► /ldd:scope ──► /ldd:elaborate ──► /ldd:refine ──► /ldd:design ──► /ldd:plan
                                                                                                  │
                                                                                                  ▼
                                                                                           [Plan PR review]
                                                                                                  │
                                                                                                  ▼
                                                                                           /ldd:implement
                                                                                                  │
                                                                                                  ▼
                                                                                           [Code PR review]
                                                                                                  │
                                                                                                  ▼
                                                                                               [Close]
```

### 7.2 PRD-initiated work (epic with decomposition)

```
/ldd:scope (PRD scope branch)             # sets Goals + Non-goals only
       │
       ▼
/ldd:elaborate                             # fills Problem, User stories, Success metrics, Open questions (draft)
       │
       ▼
/ldd:refine                                # polishes; opens PRD-PR
       │
       ▼
[PRD-PR review]                            # PM/EM/stakeholder sign-off → gate:prd-approved
       │
       ▼
/ldd:scope (decompose branch)              # slices PRD into child tickets with scope envelopes; opens decomposition-PR
       │
       ▼
[Decomposition-PR review]                  # boundary-only review → children admitted
       │
       ▼
┌────────────────────────────┼────────────────────────────┐
▼                            ▼                            ▼
child PROJ-101         child PROJ-102               child PROJ-103
/ldd:elaborate         /ldd:elaborate         /ldd:elaborate     # scope inherited from decomposition
/ldd:refine            /ldd:refine            /ldd:refine
/ldd:design            /ldd:design            /ldd:design
/ldd:plan              /ldd:plan              /ldd:plan
[plan-PR]              [plan-PR]              [plan-PR]
/ldd:implement         /ldd:implement         /ldd:implement
[code-PR]              [code-PR]              [code-PR]
```

Sibling children proceed in parallel after decomposition. Only explicit `depends_on:` frontmatter imposes ordering. Each child inherits its scope envelope from the decomposition; no separate `/ldd:scope` invocation per child unless scope changes mid-flight.

### 7.3 Hotfix override (production incident)

```
ticket created (kind:bug, risk:high)
       │
       ▼
/ldd:triage --hotfix="INC-42"          # admits without normal scope phase
       │
       ▼
/ldd:implement --hotfix="INC-42"       # bypasses phase:implement and gate:plan-approved preconditions
       │
       │  produces minimum required artifacts before any code:
       │   - one-line ticket.md with problem framing only
       │   - one-line plan.md with a single slice describing the fix + a red test
       │  (these are mandatory; --hotfix does not waive them, only the gates)
       │
       ▼
[Code PR, fast-track review with hotfix-incident label]
       │
       ▼ (post-merge)
auto-creates retroactive ticket: "Retrofit artifacts for INC-42"
       │
       ▼
/ldd:scope + /ldd:elaborate + /ldd:refine + /ldd:design (with research and full design.md)
       │
       ▼ committed to original ticket directory with retrofit:true frontmatter
       │
       ▼
original ticket remains phase:close; retrofit ticket closes when retrofit artifacts merged
```

**Hotfix override semantics:**
- `--hotfix="<incident-ref>"` is the only flag that bypasses `gate:plan-approved` and the `phase:implement` precondition on `/ldd:implement`
- Requires an incident reference (e.g., `INC-42`); refuses without one
- Does **not** waive the minimum artifact requirement: one-line ticket.md (problem) and one-line plan.md (single slice + red test) must be produced before any code commits. These are halt-only checks
- Auto-creates a retrofit ticket on code-PR merge; the original incident ticket can close for production bookkeeping, while the retrofit ticket remains open as the audit obligation until retrofit artifacts land
- Retroactive artifacts use `retrofit: true` frontmatter and append to the original ticket's `docs/tickets/<KEY>/` directory; they do not change the original ticket's `phase:close` state

The retroactive pass produces the full pre-design artifact set so future engineers see the same trail of decisions a non-hotfix ticket would carry. The retrofit ticket is the audit gate; the original is not reopened.

### 7.4 Low-risk compressed path

```
ticket accepted (kind:feature|refactor|bug, risk:low)
       │
       ▼
/ldd:prepare
       │
       ├─ writes terse ticket.md, design.md, plan.md
       ├─ runs every phase-local self-review
       └─ records question/artifact budgets in audit.yml
       │
       ▼
if low_risk_plan_pr: required       if low_risk_plan_pr: auto_approve
       │                                      │
       ▼                                      ▼
[Plan PR review]                    gate:plan-approved set by self-review
       │                                      │
       └──────────────────────┬───────────────┘
                              ▼
                       /ldd:implement
                              │
                              ▼
                       [Code PR review]
```

This is the anti-ceremony path. It preserves the artifact trail and phase-local checks, but removes manual phase invocation and, if configured, the separate plan-PR. If an escalation trigger appears mid-run, `/ldd:prepare` stops and hands the ticket back to the normal macro-skill path.

## 8. Artifact Schemas

All artifacts are structured markdown with YAML frontmatter. HTML companions are auto-generated.

### 8.1 PRD (`prd.md`)

Sections are owned by specific skills (annotation in parens):

```yaml
---
ticket: PROJ-100
kind: epic
created: 2026-05-11
authors: [pm-name]
status: phase:refinement
scope_locked_at: 2026-05-11T10:00:00Z   # set when /ldd:scope completes Branch A
---

# <Product feature name>

<!-- # scope-locked -->
## Goals                          (filled by /ldd:scope)
Business outcomes this enables (metrics, OKR ties).

## Non-goals                      (filled by /ldd:scope)
Explicitly out of scope; what this PRD is *not* trying to solve.
<!-- # end scope-locked -->

## Problem                        (drafted by /ldd:elaborate, polished by /ldd:refine)
Who is affected, what they currently can't do, why it matters now.

## User stories                   (drafted by /ldd:elaborate, polished by /ldd:refine)
- As X, I want Y, so that Z.

## Success metrics                (drafted by /ldd:elaborate, polished by /ldd:refine)
How we'll know it worked. Each metric measurable with units and a baseline (refine enforces).

## Open questions                 (surfaced by /ldd:elaborate, resolved or escalated by /ldd:refine)
Unresolved items that need PM/EM/stakeholder input.
```

The `scope-locked` HTML-comment markers are mechanical guards: `/ldd:elaborate` and `/ldd:refine` refuse to modify content between those markers. To change scope, re-invoke `/ldd:scope`.

### 8.2 Ticket (`ticket.md`)

```yaml
---
ticket: PROJ-101
parent: PROJ-100         # if decomposed from epic
kind: feature
risk: med
created: 2026-05-11
status: phase:refinement
scope_locked_at: 2026-05-11T10:30:00Z   # set when /ldd:scope Branch B completes
depends_on: []           # set by /ldd:scope when relevant
---

# <Ticket title>

<!-- # scope-locked -->
## Out of scope                   (filled by /ldd:scope)
What this ticket is *not* doing. Future work split into new tickets.
<!-- # end scope-locked -->

## Problem framing                (drafted by /ldd:elaborate, polished by /ldd:refine)
User-facing problem. Why this ticket exists.

## Acceptance criteria            (drafted by /ldd:elaborate, polished by /ldd:refine)
- [ ] Testable condition 1
- [ ] Testable condition 2

## Affected modules               (drafted by /ldd:elaborate, verified by /ldd:refine)
File/module pointers, verified to exist in the codebase during refinement.

## Edge cases                     (surfaced by /ldd:refine)
Edge cases worth testing — added during refinement when AC are sharpened.
```

### 8.3 Design (`design.md`)

```yaml
---
ticket: PROJ-101
parent_prd: PROJ-100                          # if decomposed from epic; null otherwise
refined_ticket_sha: <sha of ticket.md at start of design>
created: 2026-05-11
updated: 2026-05-11
status: phase:plan                            # current phase after this artifact completes
research_mode: blind                          # blind | sighted | skip
design_pr: null                               # set for epics when /ldd:design opens design-PR
gate_design_approved_at: null                 # set on design-PR merge (epics only)
review_overrides: []                          # populated if --override-review used during design
---

# Design — <Ticket title>

## Research (ticket-blind findings)
Objective characterisation of the affected modules, produced by a subagent
without ticket context. What the code actually contains and does today.

## Decisions
Chosen architectural approach. Components, relationships, data flow.

### Alternatives considered
- Option A: ... (rejected because ...)
- Option B: ... (rejected because ...)
- Option C: chosen.

## Structure
Proposed interface shape — signatures, types, module boundaries.
Reads like a C header file or .d.ts before implementation.

## Migration / Backward-compat            (required for risk:high)
What existing behaviour changes, how callers are affected, what bridge code is needed.

## Rollout / Revert                       (required for risk:high)
How the change is deployed (feature flag? gradual?); how to revert if it goes wrong.

## Observability                          (required for risk:high or touching prod paths)
What logs/metrics/alerts must exist before this lands.

## Security / Dependencies                (required for new deps or auth/data changes)
New attack surface; new dependencies and their supply-chain status.
```

### 8.4 Plan (`plan.md`)

```yaml
---
ticket: PROJ-101
parent_prd: PROJ-100                          # inherited; null for top-level tickets
refined_ticket_sha: <sha of ticket.md>        # version of ticket the plan was built from
design_sha: <sha of design.md>                # version of design the plan was built from
created: 2026-05-11
updated: 2026-05-11
status: phase:implement                       # current phase after this artifact lands
plan_pr: null                                 # set when /ldd:plan opens plan-PR
plan_auto_approved: false                     # true only when /ldd:prepare uses low_risk_plan_pr:auto_approve
prepared_by_wrapper: false                    # true when generated by /ldd:prepare
gate_plan_approved_at: null                   # set on plan-PR merge
code_pr: null                                 # set when /ldd:implement opens code-PR
gate_tests_green_at: null                     # set on code-PR merge
review_overrides: []                          # populated if --override-review used during plan
---

# Plan — <Ticket title>

## Slice 1: <name>
- Files touched: src/auth/oauth_config.ts (new), src/auth/oauth_config.test.ts (new)
- Red test: "OAuth config rejects missing client_id"
- AC traced: PROJ-101 AC #1 ("config must require client_id")
- Blocked by: none
- Acceptance: red test green; config type exported

## Slice 2: <name>
...
```

### 8.5 What lives where

Three storage tiers per ticket; each has a defined responsibility:

| Where | Lifecycle | What lives there |
|---|---|---|
| **Artifact frontmatter** (per file) | Stable, occasionally updated | Identity (ticket, parent), referential SHAs (design_sha, refined_ticket_sha), gate timestamps, status, list of review-override summaries |
| **`audit.yml`** (per ticket, append-only) | Event log; never edited | Every skill invocation with timestamp, actor, model tier used, override flags used, before/after labels, time taken. The full history of decisions on this ticket. |
| **Ledger ticket** (canonical) | Live state | Current `phase:*` and other labels, comments (which include short audit summaries), links to PRs |

When a frontmatter field and a ledger label disagree, the **ledger wins for status; the repo wins for content**. Audit.yml is authoritative for "what happened when."

## 9. Configuration (`/ldd:setup`)

The setup skill asks the user a sequence of questions and writes `.ldd/config.yml`. Re-runnable to reconfigure.

### 9.1 Questions asked

1. **Ledger backend** — GitHub Issues | JIRA | Linear | local files
2. **Ledger credentials** — env var name where the token lives
3. **Artifact location** — default `docs/tickets/`, customisable
4. **Render target** — GitHub Pages | none (raw markdown only) | custom URL | Confluence push
5. **Label vocabulary mapping** — for each canonical LDD label, what's the ledger-specific string? (Default mapping provided for each backend.)
6. **Board column mapping** — for each `phase:*`, which board column does it correspond to? (Default mapping provided.)
7. **Role definitions** — does your team have a PM/PO? An EM separate from senior engineers? (Affects default ownership of scope/elaborate/refine.)
8. **Agent platform** — Claude Code | Codex CLI | Gemini CLI | Cursor | Continue.dev | Generic. (Determines skill install location and subagent primitive.)
9. **Subagent capability** — auto-detect; user can force off if their platform lacks support.
10. **Model tier resolution** — for each of `fast`, `balanced`, `reasoning`, what's the concrete model ID on your platform?
11. **Ceremony controls** — allow `/ldd:prepare`? Should low-risk plans require PR review or auto-approve after plan self-review? Override default question/artifact budgets?

### 9.2 Output

```yaml
# .ldd/config.yml
ledger:
  backend: github-issues          # or jira | linear | files
  credentials_env: GITHUB_TOKEN
  repo: org/repo                  # backend-specific

artifacts:
  location: docs/tickets/
  render_target: github-pages
  render_url: https://org.github.io/repo/tickets/

labels:
  # canonical → ledger-specific
  "phase:refinement": "phase: refinement"
  "phase:design": "phase: design"
  # ... etc

board:
  "phase:refinement": "Ready"
  "phase:design": "Design"
  # ... etc

roles:
  pm: true
  em_separate_from_se: false
  qa_lead: false

agent:
  platform: claude-code            # or codex-cli | gemini-cli | cursor | continue-dev | generic
  subagents_supported: true
  fallback_strategy: phased-prompt

models:
  triage_repro: fast
  triage_severity: balanced
  refine_grill: balanced
  refine_decompose: reasoning
  design_research_subagent: balanced
  design_synthesis: reasoning
  design_alternatives: balanced
  plan_generation: balanced
  plan_review: reasoning
  implement_test: balanced
  implement_code: fast
  implement_refactor: balanced

tier_resolution:
  fast: "<your-fast-model-id>"
  balanced: "<your-balanced-model-id>"
  reasoning: "<your-reasoning-model-id>"

cost_ceilings:
  per_skill_invocation_usd: null   # optional

ceremony:
  prepare_enabled: true
  prepare_allowed_risks: ["low"]
  low_risk_plan_pr: auto_approve    # required | auto_approve
  question_budgets:
    scope: 3
    elaborate: 5
    refine: 2
    design: 2
    plan: 0
  artifact_budgets:
    low:
      scope_bullets: [3, 5]
      acceptance_criteria: [1, 4]
      design_pages: 1
      plan_slices: [1, 2]
    med:
      scope_bullets: [3, 7]
      acceptance_criteria: [3, 8]
      design_pages: 3
      plan_slices: null
  escalation_triggers:
    - risk:high
    - external_dependency
    - data_migration
    - security_auth_payment_privacy
    - cross_team_ownership
    - production_path
    - previous_incident_area
```

## 10. Platform Adapters

Skills are written in plain markdown with YAML frontmatter — readable and executable by any modern coding agent. The installer detects platform and places them in the right location.

| Platform | Skill location | Adapter doc |
|---|---|---|
| Claude Code | `.claude/skills/ldd/` | `docs/ldd/adapters/claude-code.md` |
| Codex CLI | `~/.codex/skills/ldd/` (or equivalent) | `docs/ldd/adapters/codex-cli.md` |
| Gemini CLI | `.gemini/skills/ldd/` (or equivalent) | `docs/ldd/adapters/gemini-cli.md` |
| Cursor | `.cursorrules` snippets + `docs/` | `docs/ldd/adapters/cursor.md` |
| Continue.dev | `.continue/` | `docs/ldd/adapters/continue-dev.md` |
| Generic / fallback | `docs/ldd/skills/` (user includes in system prompt) | `docs/ldd/adapters/generic.md` |

Each adapter doc maps platform-specific concerns (subagent dispatch primitives, tool naming, slash-command syntax) to the generic LDD model.

## 11. Renderer

A small Markdown → HTML renderer ships with LDD (Python + Jinja templates, ~200 lines target). Triggered automatically by a CI hook on every commit to a `docs/tickets/**/*.md` file.

### 11.1 HTML capabilities

- Collapsible sections (large plans become scannable)
- Risk/status badges (color-coded for TPM scanning)
- Mermaid → SVG for sequence/architecture diagrams
- Auto-generated TOC + anchors (deep-linking from tickets)
- Tabs for "current vs proposed" code comparisons
- File pills (`auth.py:42` rendered as clickable repo links)
- Syntax-highlighted code blocks
- Print-friendly view

### 11.2 Source-of-truth invariant

The structured markdown is the source of truth. HTML is regenerated deterministically. The renderer never modifies markdown.

## 12. Non-goals (deliberate)

- **No release management.** Cutting release notes, deploying, rolling out — out of scope. LDD ends at code-PR merge.
- **No verify or close skills.** PR review + CI cover verification. Closing is automated on code-PR merge. These don't need skill-level handles.
- **No sprint planning / standup / retrospective automation.** Scrum ceremonies are human-coordination concerns; LDD doesn't replace them.
- **No new database, no service to run.** Ledger + git is the entire state.
- **No real-time sync.** Skills operate on-demand; CI/webhooks flip labels on PR events; no daemon.
- **No bidirectional ledger-as-truth and repo-as-truth.** Ledger is authoritative for status; repo is authoritative for content. Conflicts resolve to repo for content, ledger for state.

## 13. Open Questions / Future Work

- **PRD-PR review mechanics for PM-heavy orgs.** PMs unfamiliar with PRs may resist. Mitigation: `--override-preflight="pm-workflow-exception"` exists for teams that explicitly bypass PRD-PR review; `prd:review-skipped` label visible at retro time. Worth revisiting after first team adoption.
- **Cost ceilings as hard limits vs. warnings.** Configured as warnings initially; revisit if teams hit unexpected bills.
- **Verify-skill candidacy.** A future `/ldd:verify` skill could summarise acceptance-criteria checks, coverage deltas, and security scan outputs as a single readable verification report. Not in v1.
- **Cross-ticket dependency graph visualisation.** The frontmatter `depends_on:` + `parent:` data is queryable; a visualisation tool could render a project-wide DAG. Out of scope for v1; possible future companion.
- **Templates per ticket `kind:`** — `kind:bug` template is 3 fields (repro, expected, actual); `kind:feature` is the lean 4 (problem, AC, affected modules, out-of-scope); `kind:refactor` adds risk explicitly. Templates ship in `.ldd/templates/`; teams can customise.

## 14. Glossary

- **Ledger** — the ticket tracker (JIRA, GitHub Issues, Linear, or local files) holding ticket status.
- **Artifact** — a structured markdown file committed to `docs/tickets/<KEY>/` carrying ticket content (PRD, ticket-detail, design, plan, progress).
- **Phase** — one of eight macro states a ticket passes through (scoping → elaboration → refinement → design → plan → implement → verify → close).
- **Scoping** — the activity of setting boundaries: what's in/out of a PRD (Goals/Non-goals), out-of-scope of a ticket, or how an epic decomposes into children. High-stakes, costly to reverse. Owned by `/ldd:scope`.
- **Elaboration** — first-pass content generation within already-scoped boundaries: drafting problem framing, user stories, AC, success metrics, affected modules. Generative, low-stakes. Owned by `/ldd:elaborate`.
- **Refinement** — polishing and sharpening of elaborated content: making AC testable, metrics measurable, ambiguities resolved, edge cases surfaced. Convergent, high-precision. Owned by `/ldd:refine`.
- **Scope-locked region** — a section of an artifact (marked with `<!-- # scope-locked -->`) that `/ldd:elaborate` and `/ldd:refine` refuse to modify. To change scope, re-invoke `/ldd:scope`.
- **Slice** (in LDD) — one step inside `plan.md`; the unit of execution within a single ticket. Minutes–hours of work. TDD red-test-first.
- **Slice** (in Pocock) — note that Pocock uses this term to mean *ticket-sized* deliverables; in LDD it means *intra-ticket* execution steps. Vocabulary collision.
- **Ticket-blind research** — codebase investigation performed by a subagent with the ticket reference hidden, to prevent biased "find evidence supporting the proposed direction" patterns.
- **Tier** — a logical capability bucket (`fast`, `balanced`, `reasoning`) mapped to concrete model IDs at setup time. Skills only reference tiers.
- **Override** — one of LDD's explicit bypass flags: `--override-preflight="<reason>"`, `--override-review="<reason>"`, or `--hotfix="<incident-ref>"`. Overrides are classed by what they bypass, always logged, and unavailable for halt-only invariants.
