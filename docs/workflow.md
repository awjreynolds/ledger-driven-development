# LDD Workflow Details

This document expands the workflow model summarized in the README. The README is the public front door; this file holds the deeper mechanics.

## Source Of Truth

- Workflow state: repo-local `ledger.yml` files in the target project.
- Skill package: `agent-skills.json`.
- Command behavior: `skills/ldd-*/SKILL.md`.
- Claude adapters: `commands/ldd/*.md`.
- Gemini adapters: `commands/ldd/*.toml` plus `GEMINI.md`.

External trackers are optional review and sync surfaces. They are not canonical LDD state.

GitNexus is the strongly recommended code-intelligence surface when code reality matters. LDD treats GitNexus as advisory evidence, not canonical workflow state. If GitNexus is unavailable, stale, unindexed, or outside the configured related repositories, commands continue with normal repository inspection and record the limitation.

## Workflow Roles

| Lane | SDLC focus | Inputs | LDD skills | Outputs |
| --- | --- | --- | --- | --- |
| Product + Repo Context | Requirements Analysis | Customer pain, business goal, roadmap context, current workflow, constraints, existing product behavior, repository context | `/ldd:research`, `/ldd:scope`, `/ldd:elaborate`, `/ldd:refine`, `/ldd:approve` | approved `prd.md` with acceptance criteria, non-goals, constraints, and repo-informed risks |
| Technical Design | Design | Approved PRD, repo context, Architecture Decision Records (ADRs), technical constraints, related repositories | `/ldd:design`, `/ldd:plan`, `/ldd:approve`, `/ldd:decompose` | repo-scoped `sdd.md`, `plan.md`, `plan.html`, child vertical-slice tickets |
| Software Engineering | Development | Ready child ticket, approved plan, codebase, tests, documentation obligation | `/ldd:implement <ticket>`, `/ldd:implement ALL` with built-in Test-Driven Development (TDD) | bounded code diff or Pull Request (PR), tests, refactoring, implementation evidence, documentation impact evidence |
| Engineering Review | Testing / Verification | Implementation evidence, required checks, approved artifacts, PR state, drift metadata | `/ldd:verify`, `/ldd:close`, `/ldd:archive` | `verification.md`, closure readiness, closed ledger state, optional external tracker projection |

Engineering Managers, Technical Program Managers, Product Managers, and delivery stakeholders use the workflow for dependency, sequencing, roadmap, capacity, review-load, and status visibility. They do not own a separate LDD artifact or approval gate.

## MVP Workflow

```text
draft PRD ledger
  -> optional research
  -> promoted Product Requirement ticket
  -> PRD approval with /ldd:approve
  -> SDD/Plan
  -> SDD and plan approval with /ldd:approve
  -> child vertical-slice tickets
  -> implementation
  -> verification
  -> human-approved closure
  -> optional local archive cleanup
```

The repo-local `ledger.yml` is canonical. `/ldd:refine` commits the final PRD and routes PRD approval to `/ldd:approve <ticket-id>`. In local tracker mode, a promoted stable ticket directory such as `docs/tickets/LDD-0001-short-slug/` is the real ticket. In GitHub tracker mode, PRD approval creates or binds the GitHub Product Requirement issue first, then uses the GitHub issue number as the promoted ticket identifier (ID) and directory name. External trackers are synchronized only when configured and approved by the human.

New Product Requirements can be scoped while other promoted tickets are still in progress. `/ldd:scope` creates or updates the local draft ticket directory; incomplete promoted tickets do not block new draft PRDs. Local mode keeps one active draft, so starting another draft first requires continuing, renaming, promoting, or discarding the existing draft.

`/ldd:research` gathers Product Manager-grade inputs before scoping when the trigger is weak, sensitive, or requires codebase investigation. Research has full read-only visibility into repository files, docs, existing LDD artifacts, GitNexus code-intelligence context when available, and human-supplied private/local context, but it writes only sanitized conclusions, codebase facts, explicit uncertainties, risks, sensitivity handling, open questions, and one readiness decision.

`/ldd:design` is the strongest GitNexus consumer. It strongly recommends GitNexus-backed discovery before deciding affected repositories, SDD boundaries, cross-repo sequencing, and contract risks. GitNexus is advisory: stale or unavailable indexes are recorded as limitations rather than blocking LDD unless a team policy or approved plan explicitly requires fresh GitNexus evidence.

Product commands use a bounded shared-understanding gate before a PRD can move forward. That gate keeps the useful part of grill-style questioning: the agent must prove it understands the user's intended boundary, blocker, and handoff criteria. It is bounded so the conversation does not absorb every related idea into the current PRD; weak inputs route to `/ldd:research`, new scope routes back to `/ldd:scope`, a later phase, or a separate PRD.

Every LDD phase has an input quality gate. A command must validate its source inputs before writing or mutating artifacts; when inputs fail the standard, it names the blocking gap and the earliest LDD command that can repair it.

## Handoff Artifacts

`/ldd:setup` installs templates into a target repository:

```text
.ldd/config.yml
.ldd/templates/ledger.yml
.ldd/templates/research.md
.ldd/templates/prd.md
.ldd/templates/sdd.md
.ldd/templates/plan.md
.ldd/templates/plan.html
.ldd/templates/issue-body-prd.md
.ldd/templates/issue-body-sdd.md
.ldd/templates/issue-body-child.md
.ldd/templates/pr-body-prd.md
.ldd/templates/pr-body-sdd-plan.md
.ldd/templates/pr-body-implementation.md
.ldd/templates/verification.md
docs/tickets/_drafts/
docs/tickets/_archive/
```

The templates are quality contracts, not blank forms:

- PRDs keep product scope separate from technical design.
- Research artifacts gather standard Product Manager inputs, codebase facts, and sensitivity handling before scope without becoming product scope or engineering design.
- GitNexus is strongly recommended code intelligence for research, design, planning, and optional verification evidence; it never replaces the repo-local ledger.
- `/ldd:approve` records explicit human approval for PRD, SDD, and plan gates. It does not approve decomposition, closure, or external mutations.
- SDDs translate approved PRDs into designs grounded in code and ADRs.
- Plans trace acceptance criteria to implementation slices and verification.
- Plans and child tickets must record documentation impact for each slice: updated, not needed with reason, or blocked.
- Decomposition turns approved plan slices into child vertical-slice tickets.
- Implementation completes child work but does not close it. Implementation evidence must include documentation impact, changed documentation paths, or a direct docs-not-needed rationale.
- Verification checks child-ticket closure readiness before workflow close, including documentation impact for the implemented child work.
- Close applies verified closure, keeps local ticket paths stable, and can close a parent only when every child is verified and closeable. In GitHub mode, issue closure is an explicit external mutation recorded as evidence.
- Archive is optional storage cleanup for already-closed local ticket packages.
- Child tickets follow LDD's standalone independently-grabbable shape: parent, what to build, acceptance criteria, blockers, user stories covered, and LDD traceability.
- PR bodies focus reviewers on the correct handoff question.

## Planning-System Projections

GitHub is the first external-tracker dogfooding path:

- GitHub issues project PRD, SDD, and child work visibility.
- SDD issues are children of PRD issues; implementation child work issues created by decomposition are native GitHub sub-issues of the SDD issue when GitHub supports sub-issues, so a PRD issue may have implementation issue grandchildren.
- GitHub Pull Requests project implementation review.
- LDD updates managed GitHub bodies only after explicit human confirmation and drift checks.
- Linear and Jira remain follow-on optional collaboration surfaces until the GitHub model is proven.

Current maturity:

| Surface | Status |
| --- | --- |
| Local ledger | Canonical and always supported |
| GitHub | First dogfooding path for issues, sub-issues, and Pull Request review projections |
| Linear | Important planning surface, not validated support yet |
| Jira | Important enterprise planning surface, not validated support yet |
| Asana | Candidate roadmap/cross-functional planning surface, not validated support yet |
| Trello and internal trackers | Adaptive projection examples, not validated support yet |

External issue bodies are rich projections of the ledger and artifacts, readable without opening the repo.
