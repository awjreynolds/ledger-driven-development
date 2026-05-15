# Enterprise README And Workflow Visualization Design

**Date:** 2026-05-15
**Status:** approved direction for implementation planning
**Context:** improving the public README so enterprise PMs, EMs, Tech Leads, SEs, TPMs, engineering reviewers, and buyers of AI-assisted delivery workflows understand why GADD is different

## Thesis

The README should sell GADD as the enterprise operating model for AI-assisted software delivery, not as another prompt pack, task wrapper, or individual-developer productivity hack.

The sales promise is:

> GADD lets enterprise teams use AI agents without losing SDLC governance, role ownership, roadmap visibility, review discipline, or multi-repo delivery control.

GADD is different because it keeps product scope, technical design, planning, implementation, verification, and closure in explicit handoffs. Agents can accelerate the work, but they must not collapse role boundaries into one maverick chat loop where scope expands quietly, planning systems drift, and approval evidence is unclear.

The README should make that promise visible in the first screen before explaining package mechanics.

## Audience

The primary audience is enterprise teams evaluating whether GADD makes AI-assisted delivery safe enough for real product work:

- PMs who own product problem, users, outcomes, scope, and PRD readiness
- EMs and Tech Leads who own technical design decisions and engineering plan shape
- SEs who implement approved vertical slices
- Engineering reviewers, including QA signal where needed, who assess evidence and closure readiness
- TPMs and delivery stakeholders who need roadmap, dependency, sequencing, and status visibility
- Directors and platform leaders who need adoption to fit existing planning, review, audit, and compliance expectations

Agent/tool authors are secondary. Package mechanics and adapter details remain in the README, but they should no longer be the opening story.

## Sales Positioning

The README should be written as a sales pitch for enterprise teams, with a clear problem, promise, differentiators, and proof points.

Lead with enterprise pain:

- AI agents are effective, but chat-first delivery does not naturally respect PM, EM, SE, QA, TPM, roadmap, or audit boundaries.
- One conversational task can quietly become product scope, design, implementation, test strategy, documentation policy, and closure decision.
- External planning systems can become stale when the canonical work happens in an agent chat.
- Multi-repo work becomes risky when one agent treats several codebases as one unbounded implementation surface.
- Reviewers end up asking "what happened?" instead of the intended handoff question.

Then state the GADD promise:

- role-safe SDLC handoffs
- canonical repo-local workflow state
- reviewable artifacts at each phase
- vertical-slice implementation with evidence
- explicit verification and closure
- business planning and review projections without making the planning system (GitHub Issues, Jira, Asana, Linear, Trello, or a custom internal tracker) the hidden source of truth
- multi-repo awareness with repo-scoped SDDs

The README should use confident product language, but every claim must stay within validated support. It can say "designed for planning systems such as GitHub Issues, Jira, Asana, Linear, Trello, and internal trackers" or "future/adaptive projection targets"; it must not say those integrations work today.

The AI-native pitch should be explicit:

> Point GADD at the planning system your organization already uses (GitHub Issues, Jira, Asana, Linear, Trello, or an internal tracker). GADD is designed to learn the available API surface, propose the safest projection model, and keep the repo-local ledger canonical.

That claim must be framed as product direction unless and until API-surface discovery, mapping approval, and external mutation controls are implemented and verified.

## README Narrative

Open with the contrast:

- **Maverick chat/task loop:** scope, design, planning, implementation, and review happen in one conversation; responsibilities blur; scope creep is easy; trackers drift; review asks the wrong question.
- **GADD:** each SDLC phase has clear inputs, owning role, `/gadd:*` skill, output artifact, approval gate, and next command.

Then explain the mechanism:

- the repo-local `ledger.yml` is canonical workflow state
- external tools are projections for planning, review, and visibility, not the source of truth
- `/gadd:next` is shared read-only navigation for every participant
- visible progress checklists are recommended agent UX only; they do not replace ledger state, approval, verification, or closure evidence

The first README screen should answer three sales questions:

1. What enterprise risk does GADD remove?
2. Why is GADD different from letting an agent run a task list?
3. How does GADD fit existing business planning and engineering review?

Detailed commands and installation should come after those answers.

## Role Visualization

The README should include a visual or table organized as vertical role lanes.

The lanes should be:

1. **PM**
   - Inputs: customer pain, business goal, roadmap context, current workflow, constraints
   - Skills: `/gadd:research`, `/gadd:scope`, `/gadd:elaborate`, `/gadd:refine`, `/gadd:approve`
   - Outputs: `research.md`, approved `prd.md`
2. **EM / Tech Lead**
   - Inputs: approved PRD, repository context, ADRs, technical constraints, related repositories
   - Skills: `/gadd:design`, `/gadd:plan`, `/gadd:approve`, `/gadd:decompose`
   - Outputs: repo-scoped `sdd.md`, `plan.md`, `plan.html`, child vertical-slice tickets
3. **SEs**
   - Inputs: ready child ticket, approved plan, codebase, tests, documentation obligation
   - Skills: `/gadd:implement <ticket>`, `/gadd:implement ALL`
   - Outputs: bounded code diff or PR, implementation evidence, documentation impact evidence
4. **Engineering Review**
   - Inputs: implementation evidence, required checks, approved artifacts, PR state, drift metadata
   - Skills: `/gadd:verify`, `/gadd:close`, `/gadd:archive`
   - Outputs: `verification.md`, closed ledger state, optional external tracker projection

TPMs should not be shown as owning a distinct GADD artifact or gate. They should be named as important planning, dependency, sequencing, roadmap, and status stakeholders.

## Utility Skills

The README should include a small utility section:

- `/gadd:next`: read-only workflow navigation used by PMs, TPMs, EMs, SEs, and reviewers
- `/gadd:setup`: repository bootstrap
- visible session progress: recommended UX for agents that support it

Utility skills do not own SDLC artifacts.

## Multi-Repo Boundary

The README must state the distinction clearly:

- GADD is multi-repo aware.
- SDDs are repo-scoped.

A Product Requirement can reveal coordinated work across several repositories. GADD may use repository inspection and GitNexus-style code intelligence across related repositories to discover impact and sequencing. The design output must still preserve repository ownership: each affected repository needs its own SDD and plan boundary for implementation, review, verification, and closure.

The README should avoid implying one vague cross-repo SDD owns all code changes.

## External Planning And Review Surfaces

The README should make external systems important without overclaiming support.

Use an integration maturity model:

- **Local ledger:** canonical and always supported
- **GitHub:** first dogfooding path currently documented in the repo
- **Linear:** important planning surface, not validated support yet
- **Jira:** important enterprise planning surface, not validated support yet
- **Asana:** potential roadmap/cross-functional planning surface, not part of the current validated contract
- **Trello and internal trackers:** examples of adaptive projection targets, not validated support yet

Avoid language such as "supports Jira", "supports Trello", or "integrates with Asana" until those paths are implemented and verified. Prefer "planning-system target", "adaptive projection target", "not yet validated", or "future integration candidate" depending on maturity.

## README Structure

Recommended structure:

1. Sales headline and one-paragraph enterprise promise
2. "Why AI delivery breaks in enterprise teams" pain section
3. "What GADD changes" differentiator section
4. Role-lane workflow visualization
5. Shared state and utility skills
6. Multi-repo awareness and repo-scoped SDDs
7. External planning/review surface maturity
8. Commands
9. Install
10. Package model and source-of-truth details
11. Validation

The existing install and package details should remain, but move lower so readers understand the workflow before adapter mechanics.

## GitHub Pages Or Wiki

Do not start with GitHub Wiki.

Do not require GitHub Pages for this change. The README should be the canonical public front door because package consumers and GitHub visitors land there first. GitHub Pages can be follow-on if the project needs richer diagrams, walkthroughs, or a documentation site. Wiki would create another mutable documentation surface and risks drifting from the repo.

## Non-Goals

- Do not claim validated Jira, Linear, or Asana support.
- Do not claim validated Trello or custom internal tracker support.
- Do not define a TPM-owned GADD artifact or gate.
- Do not make visible agent progress canonical workflow state.
- Do not move canonical workflow truth out of `ledger.yml`.
- Do not replace existing command contracts in this README-only change.
- Do not create a full documentation site unless the README proves insufficient.
- Do not dilute the pitch into neutral package documentation before explaining the enterprise value.

## Acceptance Criteria

- A new reader can identify why GADD is different from a chat/task loop within the first README section.
- A skeptical enterprise reader can identify the business value: safer AI adoption, clearer role ownership, less scope creep, reviewable evidence, planning-system visibility, and multi-repo control.
- PM, EM/Tech Lead, SE, Engineering Review, and TPM participation are explained without blurring ownership.
- `/gadd:next`, `/gadd:setup`, and visible progress are described as utility/support surfaces.
- `/gadd:implement <ticket>` and `/gadd:implement ALL` are described without inventing behavior for bare `/gadd:implement`.
- Multi-repo awareness and repo-scoped SDDs are stated explicitly.
- External tool maturity is labeled accurately, with GitHub as the first dogfooding path and Jira/Linear/Asana/Trello/internal trackers not claimed as validated.
- Existing install and package instructions remain available.
- The repository validation command still passes.
