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
| 9 | None handle epic → ticket decomposition with carried context | Pocock's `/to-issues` is one-shot, loses parent framing | `/ldd:refine` decomposition preserves parent PRD context as inherited frontmatter |
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

Preflight refusals are bypassed with `--override="<reason>"`. The override is captured durably in artifact frontmatter and mirrored as a ticket comment. Overrides are always allowed; they are never silent.

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

## 6. Skill Inventory

Eight macro skills. Each is a single user-facing verb that orchestrates internal sub-steps and subagent dispatches.

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

Verify and close are not skills — they happen via PR review + CI + automated label flips on merge.

**Why scope, elaborate, and refine are three skills:** these are three distinct cognitive activities. **Scope** sets boundaries — a high-stakes decision that's costly to reverse. **Elaborate** produces first-draft content within boundaries — generative, low-stakes. **Refine** polishes the draft for testability and clarity — convergent, low-stakes but high-precision. Conflating them lets scope creep in via "while I'm refining I might as well also expand…"; separating them forces explicit boundary decisions that elaboration and refinement honour.

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
- If accepted: also sets `phase:refinement`, creates `docs/tickets/PROJ-NNN/` skeleton
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
- Slices the approved PRD into child tickets (`reasoning` tier — bad decomposition costs days)
- Outputs: N new ledger child tickets with `kind:feature`, `phase:scoping`, `parent: PROJ-100`, frontmatter inheriting parent context; each child's `ticket.md` has the Out-of-scope section pre-populated from the slice boundary; parent epic gets `decomposed:true` + child links
- **Opens a decomposition-PR** (`ldd/decompose/PROJ-100` branch) with the new child tickets' `ticket.md` files for reviewer sign-off before children enter their own workflows

**Pre-commit self-review** (every branch runs this before commit/PR):
- Branch A: are goals measurable? Are non-goals concrete (not "general improvements")? Are the goals + non-goals together a complete envelope (no obvious adjacent areas left ambiguous)?
- Branch B: is out-of-scope concrete (specific things, not vague categories)? Is sizing realistic?
- Branch C: does each child have a minimum-viable scope envelope? Does any child duplicate another's scope? Does the union of child scopes equal the PRD scope minus explicitly-deferred items?

Failures halt the skill and surface the issue; the engineer either fixes the input or invokes `--override="<reason>"`.

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
- For story-level work (`kind:feature|refactor|bug`): no separate PR; `design.md` commits to main and is reviewed inline as part of the upcoming plan-PR
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
- **Plan-PR description includes the accumulated artifact package**, not just the plan diff:
  - Links and short summaries of `ticket.md` (scope + elaboration + refinement) and `design.md` (research + decisions + structure)
  - The plan diff is the diff under review, but reviewers are explicitly directed to evaluate coherence of the whole package — does the plan honour the design, does the design satisfy the refined ticket, does the ticket sit cleanly inside its scope envelope
  - PR template includes a "package coherence" checklist alongside the slice-by-slice checklist
- Ticket: `plan:in-review` set when PR opens
- On plan-PR merge: `plan:approved`, `gate:plan-approved`, `phase:implement`

### 6.8 `/ldd:implement`

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
- No files were modified outside the plan's "files touched" list (any deviation → halt and request `--override` with reason)
- All ACs from the ticket have a passing test that maps to them (verified via test name matching or explicit traceability comments)
- For `risk:high` tickets: migration steps from the plan executed; revert steps documented in PR description
- `git status` clean on the implementation branch (no unstaged or untracked changes)

Failure halts and surfaces the violation. Common remediation: add a missing test, or invoke `--override` if the deviation is intentional (deviation is logged in code-PR description).

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
/ldd:triage --override="hotfix:incident:INC-42"
       │
       ▼
/ldd:implement --override="hotfix:incident:INC-42"
       │
       ▼
[Code PR, fast-track review]
       │
       ▼
(retrospectively) /ldd:scope + /ldd:elaborate + /ldd:refine + /ldd:design + /ldd:plan committed post-merge for audit
```

Overrides logged on both ticket and code-PR; the gap between hotfix and retroactive design is visible at retro time. The retrospective pass produces the full pre-design artifact set so future engineers see the same trail of decisions a non-hotfix ticket would carry.

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
created: 2026-05-11
research_mode: blind        # blind | sighted | skip
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
```

### 8.4 Plan (`plan.md`)

```yaml
---
ticket: PROJ-101
design: design.md@<sha>
created: 2026-05-11
---

# Plan — <Ticket title>

## Slice 1: <name>
- Files touched: src/auth/oauth_config.ts (new), src/auth/oauth_config.test.ts (new)
- Red test: "OAuth config rejects missing client_id"
- Acceptance: test passes; config type exported

## Slice 2: <name>
...
```

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

- **PRD-PR review mechanics for PM-heavy orgs.** PMs unfamiliar with PRs may resist. Mitigation: `--override="pm-workflow-exception"` exists; `prd:review-skipped` label visible at retro time. Worth revisiting after first team adoption.
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
- **Override** — a `--override="<reason>"` flag that bypasses a preflight check. Always allowed; always logged.
