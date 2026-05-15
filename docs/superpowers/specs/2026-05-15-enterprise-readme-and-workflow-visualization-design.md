# Enterprise README And Workflow Visualization Design

**Date:** 2026-05-15
**Status:** approved direction for implementation planning
**Context:** improving the public README so PMs, EMs, Tech Leads, SEs, TPMs, and engineering reviewers understand why LDD is different

## Thesis

The README should present Ledger-Driven Development as an enterprise SDLC workflow for AI-assisted delivery, not as another chat/task wrapper.

LDD is different because it keeps product scope, technical design, planning, implementation, verification, and closure in explicit handoffs. Agents can accelerate the work, but they must not collapse role boundaries into one maverick chat loop where scope expands quietly and approval evidence is unclear.

The README should make that difference visible in the first screen.

## Audience

The primary audience is SDLC participants:

- PMs who own product problem, users, outcomes, scope, and PRD readiness
- EMs and Tech Leads who own technical design decisions and engineering plan shape
- SEs who implement approved vertical slices
- Engineering reviewers, including QA signal where needed, who assess evidence and closure readiness
- TPMs and delivery stakeholders who need roadmap, dependency, sequencing, and status visibility

Agent/tool authors are secondary. Package mechanics and adapter details remain in the README, but they should no longer be the opening story.

## README Narrative

Open with the contrast:

- **Maverick chat/task loop:** scope, design, planning, implementation, and review happen in one conversation; responsibilities blur; scope creep is easy; trackers drift; review asks the wrong question.
- **LDD:** each SDLC phase has clear inputs, owning role, `/ldd:*` skill, output artifact, approval gate, and next command.

Then explain the mechanism:

- the repo-local `ledger.yml` is canonical workflow state
- external tools are projections for planning, review, and visibility, not the source of truth
- `/ldd:next` is shared read-only navigation for every participant
- visible progress checklists are recommended agent UX only; they do not replace ledger state, approval, verification, or closure evidence

## Role Visualization

The README should include a visual or table organized as vertical role lanes.

The lanes should be:

1. **PM**
   - Inputs: customer pain, business goal, roadmap context, current workflow, constraints
   - Skills: `/ldd:research`, `/ldd:scope`, `/ldd:elaborate`, `/ldd:refine`, `/ldd:approve`
   - Outputs: `research.md`, approved `prd.md`
2. **EM / Tech Lead**
   - Inputs: approved PRD, repository context, ADRs, technical constraints, related repositories
   - Skills: `/ldd:design`, `/ldd:plan`, `/ldd:approve`, `/ldd:decompose`
   - Outputs: repo-scoped `sdd.md`, `plan.md`, `plan.html`, child vertical-slice tickets
3. **SEs**
   - Inputs: ready child ticket, approved plan, codebase, tests, documentation obligation
   - Skills: `/ldd:implement <ticket>`, `/ldd:implement ALL`
   - Outputs: bounded code diff or PR, implementation evidence, documentation impact evidence
4. **Engineering Review**
   - Inputs: implementation evidence, required checks, approved artifacts, PR state, drift metadata
   - Skills: `/ldd:verify`, `/ldd:close`, `/ldd:archive`
   - Outputs: `verification.md`, closed ledger state, optional external tracker projection

TPMs should not be shown as owning a distinct LDD artifact or gate. They should be named as important planning, dependency, sequencing, roadmap, and status stakeholders.

## Utility Skills

The README should include a small utility section:

- `/ldd:next`: read-only workflow navigation used by PMs, TPMs, EMs, SEs, and reviewers
- `/ldd:setup`: repository bootstrap
- visible session progress: recommended UX for agents that support it

Utility skills do not own SDLC artifacts.

## Multi-Repo Boundary

The README must state the distinction clearly:

- LDD is multi-repo aware.
- SDDs are repo-scoped.

A Product Requirement can reveal coordinated work across several repositories. LDD may use repository inspection and GitNexus-style code intelligence across related repositories to discover impact and sequencing. The design output must still preserve repository ownership: each affected repository needs its own SDD and plan boundary for implementation, review, verification, and closure.

The README should avoid implying one vague cross-repo SDD owns all code changes.

## External Planning And Review Surfaces

The README should make external systems important without overclaiming support.

Use an integration maturity model:

- **Local ledger:** canonical and always supported
- **GitHub:** first dogfooding path currently documented in the repo
- **Linear:** important planning surface, not validated support yet
- **Jira:** important enterprise planning surface, not validated support yet
- **Asana:** potential roadmap/cross-functional planning surface, not part of the current validated contract

Avoid language such as "supports Jira" or "integrates with Asana" until those paths are implemented and verified. Prefer "projection target", "planned surface", "not yet validated", or "future integration candidate" depending on maturity.

## README Structure

Recommended structure:

1. Title and one-paragraph enterprise SDLC thesis
2. "Why LDD is different" contrast against chat/task loops
3. Role-lane workflow visualization
4. Shared state and utility skills
5. Multi-repo awareness and repo-scoped SDDs
6. External planning/review surface maturity
7. Commands
8. Install
9. Package model and source-of-truth details
10. Validation

The existing install and package details should remain, but move lower so readers understand the workflow before adapter mechanics.

## GitHub Pages Or Wiki

Do not start with GitHub Wiki.

Do not require GitHub Pages for this change. The README should be the canonical public front door because package consumers and GitHub visitors land there first. GitHub Pages can be follow-on if the project needs richer diagrams, walkthroughs, or a documentation site. Wiki would create another mutable documentation surface and risks drifting from the repo.

## Non-Goals

- Do not claim validated Jira, Linear, or Asana support.
- Do not define a TPM-owned LDD artifact or gate.
- Do not make visible agent progress canonical workflow state.
- Do not move canonical workflow truth out of `ledger.yml`.
- Do not replace existing command contracts in this README-only change.
- Do not create a full documentation site unless the README proves insufficient.

## Acceptance Criteria

- A new reader can identify why LDD is different from a chat/task loop within the first README section.
- PM, EM/Tech Lead, SE, Engineering Review, and TPM participation are explained without blurring ownership.
- `/ldd:next`, `/ldd:setup`, and visible progress are described as utility/support surfaces.
- `/ldd:implement <ticket>` and `/ldd:implement ALL` are described without inventing behavior for bare `/ldd:implement`.
- Multi-repo awareness and repo-scoped SDDs are stated explicitly.
- External tool maturity is labeled accurately, with GitHub as the first dogfooding path and Jira/Linear/Asana not claimed as validated.
- Existing install and package instructions remain available.
- The repository validation command still passes.
