# Enterprise README Sales Pitch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the public README so enterprise teams understand why GADD is valuable, how it keeps AI-assisted delivery governed, and how it relates to role boundaries, multi-repo delivery, and planning-system projections.

**Architecture:** Keep `README.md` as the canonical public front door. Reorder the README so the sales pitch comes before package mechanics, using one Mermaid diagram/table for role lanes and concise sections for state, utilities, multi-repo boundaries, and integration maturity. Do not create GitHub Pages or Wiki in this slice.

**Tech Stack:** Markdown, GitHub-flavored Mermaid, existing shell validation via `./scripts/validate-gadd-mvp.sh`.

---

## File Structure

- Modify `README.md`: replace the current package-first opening with an enterprise sales pitch, role-lane workflow, integration maturity, and then preserve install/package/validation content lower down.
- Modify `.gitignore`: add `.superpowers/` so local brainstorming companion files do not appear as repo changes.
- Do not modify command skill contracts in this slice.
- Do not add GitHub Pages or Wiki in this slice.

## Task 1: Ignore Local Brainstorming Scratch Files

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Add the local scratch directory to `.gitignore`**

Add this line to `.gitignore`:

```gitignore
.superpowers/
```

- [ ] **Step 2: Verify scratch files are ignored**

Run:

```bash
git status --short
```

Expected: no `?? .superpowers/` line remains.

- [ ] **Step 3: Commit**

Run:

```bash
git add .gitignore
git commit -m "Ignore local brainstorming scratch files"
```

Expected: commit succeeds.

## Task 2: Rewrite README Opening As Enterprise Sales Pitch

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace the current title and opening paragraph**

Replace:

```markdown
# GADD Skills

Agent-agnostic skills for the GADD MVP.

GADD uses a repo-local ledger as canonical workflow state. External trackers such as GitHub, Linear, or Jira are optional sync and review surfaces. GADD separates product scope, engineering design, implementation planning, decomposition, implementation, verification, and closure so AI-assisted work has explicit, reviewable handoffs.
```

With:

```markdown
# GADD

Enterprise teams can use AI agents for real software delivery without giving up SDLC governance, role ownership, roadmap visibility, review discipline, or multi-repo control.

Governed Autonomy is the operating philosophy: autonomous AI execution is useful only when authority, scope, evidence, and approval boundaries remain explicit.

GADD is the practical methodology for applying Governed Autonomy to software delivery. It turns agent work into explicit SDLC handoffs: product scope, technical design, implementation planning, vertical-slice implementation, verification, and closure. The repo-local `ledger.yml` remains canonical; planning and review systems are projection surfaces.
```

- [ ] **Step 2: Add a "Why GADD exists" section immediately after the opening**

Insert this section after the new opening:

```markdown
## Why GADD Exists

AI agents are powerful, but chat-first delivery is a poor enterprise control plane.

In a maverick chat/task loop, one prompt can quietly become product scope, technical design, implementation plan, test strategy, documentation policy, and closure decision. PM, EM, Tech Lead, SE, QA, and TPM responsibilities blur. Scope grows in the conversation. Planning systems drift. Reviewers end up asking "what happened?" instead of reviewing the intended handoff.

GADD keeps the useful part of AI acceleration while putting the work back into recognizable SDLC boundaries:

- product scope stays separate from engineering design
- technical decisions are reviewed before implementation planning
- implementation happens as bounded vertical slices
- verification and closure are separate gates
- business planning systems stay visible without becoming the hidden source of truth
- multi-repo impact can be discovered without turning design into one unbounded cross-repo blob
```

- [ ] **Step 3: Add a "What GADD Changes" section**

Insert this section after `## Why GADD Exists`:

```markdown
## What GADD Changes

| Enterprise risk | GADD response |
| --- | --- |
| Agent chat becomes the source of truth | Repo-local `ledger.yml` records phase, gate, approved inputs, next action, external links, and evidence. |
| Scope creep hides inside implementation | PRD, SDD, plan, decomposition, implementation, verification, and closure are separate handoffs. |
| Existing planning tools go stale | External systems are managed projections for roadmap, review, and status visibility. |
| Multi-repo work becomes unbounded | GADD is multi-repo aware, but SDDs and plans stay repo-scoped. |
| Reviewers lack evidence | Implementation, documentation impact, verification, and closure evidence are recorded explicitly. |
```

- [ ] **Step 4: Verify the README opening reads as a sales pitch**

Run:

```bash
sed -n '1,90p' README.md
```

Expected: the first screen leads with enterprise AI delivery value before package details.

## Task 3: Add Role-Lane Workflow And Utility Skills

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add the role-lane workflow section after "What GADD Changes"**

Insert:

```markdown
## Workflow By Role

GADD is designed for teams where different people own different SDLC decisions. The agent can assist each phase, but it should not collapse ownership into one task loop.

| Role | Inputs | GADD skills | Outputs |
| --- | --- | --- | --- |
| PM | Customer pain, business goal, roadmap context, current workflow, constraints | `/gadd:research`, `/gadd:scope`, `/gadd:elaborate`, `/gadd:refine`, `/gadd:approve` | `research.md`, approved `prd.md` |
| EM / Tech Lead | Approved PRD, repo context, ADRs, technical constraints, related repositories | `/gadd:design`, `/gadd:plan`, `/gadd:approve`, `/gadd:decompose` | repo-scoped `sdd.md`, `plan.md`, `plan.html`, child vertical-slice tickets |
| SEs | Ready child ticket, approved plan, codebase, tests, documentation obligation | `/gadd:implement <ticket>`, `/gadd:implement ALL` | bounded code diff or PR, implementation evidence, documentation impact evidence |
| Engineering Review | Implementation evidence, required checks, approved artifacts, PR state, drift metadata | `/gadd:verify`, `/gadd:close`, `/gadd:archive` | `verification.md`, closed ledger state, optional external tracker projection |

TPMs and delivery stakeholders are first-class consumers of the workflow. They need dependency, sequencing, roadmap, review-load, and status visibility, but the current GADD command model does not define a TPM-owned artifact or approval gate.
```

- [ ] **Step 2: Add the utility skills section**

Insert after `## Workflow By Role`:

```markdown
## Shared Utilities

Some GADD skills support every participant rather than owning one SDLC artifact:

- `/gadd:next` is read-only workflow navigation. It reports the next command, next human action, reason, and blocker from repo-local ledger state.
- `/gadd:setup` bootstraps a target repository with ledger config, templates, draft/archive directories, and optional external projection settings.
- Visible session progress is recommended agent UX when the host agent supports it. It helps humans see what the agent is doing, but it never replaces `ledger.yml`, approval evidence, verification, or closure state.
```

- [ ] **Step 3: Verify commands are not duplicated incorrectly**

Run:

```bash
rg -n "/gadd:implement|/gadd:next|Workflow By Role|Shared Utilities" README.md
```

Expected: `/gadd:implement <ticket>`, `/gadd:implement ALL`, and `/gadd:next` appear in the new explanatory sections; bare `/gadd:implement` is not redefined.

## Task 4: Add Multi-Repo And Adaptive Planning-System Positioning

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a multi-repo boundary section**

Insert after `## Shared Utilities`:

```markdown
## Multi-Repo Aware, Repo-Scoped Design

GADD can reason about product work that affects more than one repository. Research and design may inspect related repositories and code-intelligence evidence when available.

The boundary is deliberate: Product Requirements can be multi-repo aware, but SDDs are repo-scoped. Each affected repository needs its own design and plan boundary so ownership, implementation, review, verification, and closure remain concrete.

That distinction keeps multi-repo work coordinated without turning one agent task into an unbounded cross-repo implementation.
```

- [ ] **Step 2: Add an adaptive planning-system section**

Insert after `## Multi-Repo Aware, Repo-Scoped Design`:

```markdown
## Planning-System Projections

Enterprise delivery already lives in planning and review systems. GADD should meet teams there without making those systems canonical workflow state.

The long-term model is adaptive projection: point GADD at the planning system your organization already uses (GitHub Issues, Jira, Asana, Linear, Trello, or an internal tracker). GADD is designed to learn the available API surface, propose the safest projection model, and keep the repo-local ledger canonical.

Current maturity:

| Surface | Status |
| --- | --- |
| Local ledger | Canonical and always supported |
| GitHub | First dogfooding path for issues, sub-issues, and PR review projections |
| Linear | Important planning surface, not validated support yet |
| Jira | Important enterprise planning surface, not validated support yet |
| Asana | Candidate roadmap/cross-functional planning surface, not validated support yet |
| Trello and internal trackers | Adaptive projection examples, not validated support yet |

Do not treat external trackers as GADD's source of truth. External mutations require explicit human confirmation and drift checks.
```

- [ ] **Step 3: Verify support claims stay accurate**

Run:

```bash
rg -n "supports Jira|supports Trello|integrates with Asana|not validated|First dogfooding path|adaptive projection" README.md
```

Expected: no support claims appear for Jira, Trello, or Asana; the README uses `not validated` and `adaptive projection` language.

## Task 5: Preserve Install, Package, Source-Of-Truth, And Validation Sections

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Move the existing "Package Model" section below the new sales/workflow sections**

Keep the existing package model content, but place it after:

```markdown
## Commands
```

Do not remove the Agent Skills layout, adapter manifest table, standalone skill contract, or install instructions.

- [ ] **Step 2: Keep the command list intact**

Ensure this command list remains present:

```text
/gadd:setup
/gadd:next
/gadd:research
/gadd:scope
/gadd:elaborate
/gadd:refine
/gadd:approve
/gadd:design
/gadd:plan
/gadd:decompose
/gadd:implement
/gadd:verify
/gadd:close
/gadd:archive
```

- [ ] **Step 3: Keep source-of-truth wording intact but lower in the README**

Preserve these claims:

```markdown
- Workflow state: repo-local `ledger.yml` files in the target project.
- Skill package: `agent-skills.json`.
- Command behavior: `skills/gadd-*/SKILL.md`.
```

- [ ] **Step 4: Verify required sections exist**

Run:

```bash
rg -n "^## (Why GADD Exists|What GADD Changes|Workflow By Role|Shared Utilities|Multi-Repo Aware, Repo-Scoped Design|Planning-System Projections|Commands|Install|Package Model|Source Of Truth|Validate This Repo)" README.md
```

Expected: all listed sections are present exactly once.

## Task 6: Validate, Commit, And Publish

**Files:**
- Modify: `README.md`
- Modify: `.gitignore`

- [ ] **Step 1: Run whitespace check**

Run:

```bash
git diff --check
```

Expected: no output and exit code 0.

- [ ] **Step 2: Run repository validation**

Run:

```bash
./scripts/validate-gadd-mvp.sh
```

Expected: validation passes.

- [ ] **Step 3: Review README excerpt**

Run:

```bash
sed -n '1,220p' README.md
```

Expected: the opening sells GADD to enterprise teams before package/install mechanics.

- [ ] **Step 4: Commit the README implementation**

Run:

```bash
git add .gitignore README.md
git commit -m "Rewrite README for enterprise GADD pitch"
```

Expected: commit succeeds.

- [ ] **Step 5: Push to GitHub**

Run:

```bash
git push
```

Expected: current branch pushes successfully to its configured upstream.

If `git push` reports no upstream branch, run:

```bash
git branch --show-current
```

Then push the current branch with:

```bash
git push -u origin <branch-name>
```

Replace `<branch-name>` with the actual output from `git branch --show-current`.

## Self-Review

- Spec coverage: the plan covers enterprise sales positioning, role lanes, utility skills, multi-repo awareness with repo-scoped SDDs, adaptive planning-system examples, maturity labels, no Pages/Wiki, install/package preservation, validation, commit, and push.
- Placeholder scan: no `TBD`, `TODO`, or "fill in later" placeholders are present.
- Support-claim check: the plan says GitHub is the first dogfooding path and labels Jira, Linear, Asana, Trello, and internal trackers as not validated or adaptive projection examples.
