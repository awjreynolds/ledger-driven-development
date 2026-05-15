# Ledger-Driven Development

Enterprise teams can use Artificial Intelligence (AI) agents for real software delivery without giving up Software Development Life Cycle (SDLC) governance, role ownership, roadmap visibility, review discipline, or multi-repo control.

Ledger-Driven Development (LDD) is an AI-native workflow for product and engineering teams. It turns agent work into explicit SDLC handoffs: requirements analysis, technical design, implementation planning, vertical-slice development, verification, and closure. The repo-local `ledger.yml` remains canonical; planning and review systems are projection surfaces.

## Why LDD Exists

AI agents are powerful, but chat-first delivery is a poor enterprise control plane.

In a maverick chat/task loop, one prompt can quietly become product scope, technical design, implementation plan, test strategy, documentation policy, and closure decision. Product Manager (PM), Engineering Manager (EM), Tech Lead, Software Engineer (SE), Quality Assurance (QA), and Technical Program Manager (TPM) responsibilities blur. Scope grows in the conversation. Planning systems drift. Reviewers end up asking "what happened?" instead of reviewing the intended handoff.

LDD keeps the useful part of AI acceleration while putting the work back into recognizable SDLC boundaries:

- requirements analysis produces an approved Product Requirements Document (PRD)
- technical design produces a repo-scoped Software Design Document (SDD) and plan
- Software Engineers implement bounded vertical slices using built-in Test-Driven Development (TDD)
- engineering review verifies evidence before closure
- business planning systems stay visible without becoming the hidden source of truth
- multi-repo impact can be discovered without turning design into one unbounded cross-repo task

## What LDD Changes

| Enterprise risk | LDD response |
| --- | --- |
| Agent chat becomes the source of truth | Repo-local `ledger.yml` records phase, gate, approved inputs, next action, external links, and evidence. |
| Scope creep hides inside implementation | PRD, SDD, plan, decomposition, implementation, verification, and closure are separate handoffs. |
| AI jumps straight to code | `/ldd:implement` uses a built-in TDD loop: write a focused failing test, make it pass, refactor, then rerun broader checks. |
| Existing planning tools go stale | External systems are managed projections for roadmap, review, and status visibility. |
| Multi-repo work becomes unbounded | LDD is multi-repo aware, but SDDs and plans stay repo-scoped. |
| Reviewers lack evidence | Implementation, documentation impact, verification, and closure evidence are recorded explicitly. |

![LDD workflow across requirements analysis, design, development, and verification](docs/assets/ldd-sdlc-workflow.png)

LDD governs the SDLC slice from Requirements Analysis through Testing / Verification. It does not claim to own enterprise planning, deployment operations, or long-term maintenance; it keeps AI-assisted delivery inside clear handoffs from approved requirements to verified implementation.

## Workflow By Role

LDD is designed for teams where different people own different SDLC decisions. The agent can assist each phase, but it should not collapse ownership into one task loop.

| Lane | SDLC focus | Inputs | LDD skills | Outputs |
| --- | --- | --- | --- | --- |
| Product + Repo Context | Requirements Analysis | Customer pain, business goal, roadmap context, current workflow, constraints, existing product behavior, repository context | `/ldd:research`, `/ldd:scope`, `/ldd:elaborate`, `/ldd:refine`, `/ldd:approve` | approved `prd.md` with acceptance criteria, non-goals, constraints, and repo-informed risks |
| Technical Design | Design | Approved PRD, repo context, Architecture Decision Records (ADRs), technical constraints, related repositories | `/ldd:design`, `/ldd:plan`, `/ldd:approve`, `/ldd:decompose` | repo-scoped `sdd.md`, `plan.md`, `plan.html`, child vertical-slice tickets |
| Software Engineering | Development | Ready child ticket, approved plan, codebase, tests, documentation obligation | `/ldd:implement <ticket>`, `/ldd:implement ALL` with built-in TDD | bounded code diff or Pull Request (PR), tests, refactoring, implementation evidence, documentation impact evidence |
| Engineering Review | Testing / Verification | Implementation evidence, required checks, approved artifacts, PR state, drift metadata | `/ldd:verify`, `/ldd:close`, `/ldd:archive` | `verification.md`, closure readiness, closed ledger state, optional external tracker projection |

EMs, TPMs, PMs, and delivery stakeholders use the same workflow for dependency, sequencing, roadmap, capacity, review-load, and status visibility. They do not own a separate LDD artifact or approval gate.

## Shared Utilities

Some LDD skills support every participant rather than owning one SDLC artifact:

- `/ldd:next` is read-only workflow navigation. It reports the next command, next human action, reason, and blocker from repo-local ledger state.
- `/ldd:setup` bootstraps a target repository with ledger config, templates, draft/archive directories, and optional external projection settings.
- Visible session progress is recommended agent User Experience (UX) when the host agent supports it. It helps humans see what the agent is doing, but it never replaces `ledger.yml`, approval evidence, verification, or closure state.

## Multi-Repo Aware, Repo-Scoped Design

LDD can reason about product work that affects more than one repository. Requirements Analysis and Design may inspect related repositories and code-intelligence evidence when available.

The boundary is deliberate: Product Requirements can be multi-repo aware, but SDDs are repo-scoped. Each affected repository needs its own design and plan boundary so ownership, implementation, review, verification, and closure remain concrete.

## Planning-System Projections

Enterprise delivery already lives in planning and review systems. LDD should meet teams there without making those systems canonical workflow state.

The long-term model is adaptive projection: LDD should be able to target the planning system your organization already uses (GitHub Issues, Jira, Asana, Linear, Trello, or an internal tracker), learn the available Application Programming Interface (API) surface, and propose the safest projection model. Today, the documented dogfooding path is GitHub-first, and the repo-local ledger remains canonical.

Do not treat external trackers as LDD's source of truth. External mutations require explicit human confirmation and drift checks.

## Commands

```text
/ldd:setup
/ldd:next
/ldd:research
/ldd:scope
/ldd:elaborate
/ldd:refine
/ldd:approve
/ldd:design
/ldd:plan
/ldd:decompose
/ldd:implement
/ldd:verify
/ldd:close
/ldd:archive
```

## Install

The canonical package manifest is `agent-skills.json`.

Codex users can ask `$skill-installer` to install all skills from this repository using `agent-skills.json`. Claude Code users can install the plugin marketplace entry. Gemini Command-Line Interface (CLI) users can install this repository as an extension.

Detailed installation and package mechanics live in [docs/package-model.md](docs/package-model.md).

## More Detail

- [docs/workflow.md](docs/workflow.md) covers workflow state, external projections, the MVP workflow, and handoff artifact contracts.
- [docs/package-model.md](docs/package-model.md) covers package layout, adapter manifests, and install commands.

## Validate This Repo

```sh
./scripts/validate-ldd-mvp.sh
```
