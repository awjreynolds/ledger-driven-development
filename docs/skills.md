# LDD Skill Catalog

This is the human-readable catalog for the `/ldd:*` skills. The canonical executable contract for each command remains its `skills/ldd-*/SKILL.md` file.

Use this document to understand where a skill sits in the workflow, what it consumes, what it produces, and what handoff usually follows.

## Documentation Standard

Each LDD skill is documented in the Agent Skills layout:

```text
skills/ldd-<command>/
  SKILL.md
  agents/openai.yaml
  assets/
  references/
  scripts/
```

- `SKILL.md` is required and canonical. It contains frontmatter, trigger description, workflow rules, input quality gates, writes, outputs, and validation behavior.
- `agents/openai.yaml` is recommended UI metadata for agent skill lists and chips.
- `assets/`, `references/`, and `scripts/` are optional. Use them only when the skill needs templates, deeper reference material, or deterministic helper scripts.
- Do not add per-skill `README.md` files. Human summaries belong here; executable command contracts belong in `SKILL.md`.

## Workflow Skills

| Skill | Lane | Purpose | Primary inputs | Primary outputs | Usual next handoff |
| --- | --- | --- | --- | --- | --- |
| `/ldd:research` | Product + Repo Context | Gather sanitized product and repo evidence before scoping when inputs are weak, sensitive, or need investigation. | Product trigger, repository files/docs, existing LDD artifacts, optional GitNexus context | `research.md`, readiness decision, explicit uncertainties | `/ldd:scope` |
| `/ldd:scope` | Product + Repo Context | Define Product Requirement scope boundaries without moving into design or implementation. | Product change, goals, non-goals, constraints, draft context | draft `prd.md` scope sections, dependencies, open questions | `/ldd:elaborate` |
| `/ldd:elaborate` | Product + Repo Context | Fill product detail inside approved scope. | scoped draft PRD, user/persona context, workflow detail, acceptance signals | richer `prd.md` with users, stories, draft acceptance criteria, draft metrics | `/ldd:refine` |
| `/ldd:refine` | Product + Repo Context | Sharpen the PRD for engineering handoff and route it to approval. | draft PRD, resolved product decisions, repo-informed constraints | review-ready `prd.md`, ledger gate for PRD approval | `/ldd:approve <ticket-id>` |
| `/ldd:approve` | Product + Repo Context / Technical Design | Approve exactly one PRD, SDD, or plan gate from repo-local ledger state. | target ledger, candidate PRD/SDD/plan, external drift metadata when configured | approved artifact state, next command, approval evidence | `/ldd:design`, `/ldd:plan`, or `/ldd:decompose` depending on the approved gate |
| `/ldd:design` | Technical Design | Create or update the repo-scoped Software Design Document (SDD), including the required `## Structure` header-file summary. | approved PRD, code/docs, Architecture Decision Records, related repo context, optional GitNexus context | draft `sdd.md`, synchronized structure summary, ADR updates only when the ADR threshold is met | `/ldd:approve <ticket-id>` |
| `/ldd:plan` | Technical Design | Create an implementation plan from an approved PRD and approved SDD. | approved PRD, approved SDD, relevant ADRs, code-intelligence context | draft `plan.md`, generated `plan.html`, planned vertical slices | `/ldd:approve <ticket-id>` |
| `/ldd:decompose` | Technical Design | Turn an approved plan into independently grabbable child vertical-slice tickets. | approved PRD, approved SDD, approved plan, tracker state when configured | child ticket ledgers, child work items, parent ledger child entries | `/ldd:implement <ticket>` or `/ldd:implement ALL` |
| `/ldd:implement` | Software Engineering | Execute one ready child vertical-slice ticket or all ready child tickets within the approved boundary. | ready child ticket, approved parent PRD/SDD/plan, codebase, tests, docs obligation | code diff or Pull Request, tests, implementation evidence, documentation impact evidence | `/ldd:verify <child-ticket-id>` |
| `/ldd:verify` | Engineering Review | Verify one implemented child ticket is ready for human-approved closure. | child ledger, parent ledger, approved artifacts, implementation evidence, checks, docs impact, PR state | `verification.md`, closure readiness, verifier evidence | `/ldd:close <child-ticket-id>` |
| `/ldd:close` | Engineering Review | Apply human-approved workflow closure to a verified child or parent roll-up. | verification evidence, child/parent ledgers, external drift metadata when configured | closed ledger state, optional external issue closure after confirmation | `/ldd:archive <ticket-id>` when local cleanup is wanted |
| `/ldd:archive` | Engineering Review | Move already-closed local ticket packages into the configured archive directory. | closed ticket ledger, parent ledger when needed, archive config | archived local ticket package, updated archive state | none |

## Utility Skills

| Skill | Used by | Purpose | Writes |
| --- | --- | --- | --- |
| `/ldd:setup` | Repository owners and project starters | Bootstrap a target repository with `.ldd/config.yml`, templates, ticket directories, and optional projection settings. | Local LDD config, templates, `docs/tickets/` structure |
| `/ldd:next` | Everyone | Read repo-local ledger state and report the next command, next human action, reason, and blocker. | Nothing. It is read-only. |

## Ownership Boundaries

- Product + Repo Context owns requirements analysis and the approved PRD. It can inspect repo context, but it does not decide architecture or implementation.
- Technical Design owns the repo-scoped SDD, plan, and decomposition. Senior Engineers, Tech Leads, and Architects are expected participants.
- Software Engineering owns implementation quality inside the approved boundary: Test-Driven Development, code, refactoring, local design choices, documentation impact, and implementation evidence.
- Engineering Review owns verification and closure readiness. Quality Assurance contributes here where the team uses a QA role.
- Engineering Managers, Technical Program Managers, Product Managers, and delivery stakeholders use LDD state for sequencing, capacity, dependency, roadmap, review-load, and status visibility. They do not own a separate LDD command gate.

## Maintaining This Catalog

When a `skills/ldd-*/SKILL.md` contract changes, update this catalog only if the public purpose, lane, input, output, or handoff changed. Do not mirror every rule from the skill file.
