# GitNexus Code Intelligence Design

**Date:** 2026-05-15
**Status:** proposed design
**Context:** extending GADD code-understanding guidance for multi-repo Product Requirements

## Thesis

GADD should strongly recommend GitNexus as the preferred code-understanding surface whenever code reality matters, especially when a Product Requirement may span multiple repositories or architecture boundaries.

GitNexus must remain advisory rather than mandatory. GADD is ledger-first and agent-agnostic; it should not become unusable when GitNexus is unavailable, stale, unindexed, or outside the user's current toolchain. Commands should continue with normal repository inspection when GitNexus cannot be used, and record the limitation in the relevant artifact.

## Current GADD Constraint

The current MVP keeps each Product Requirement deliberately narrow and repo-local:

- one Product Requirement moves through PRD, SDD, plan, decomposition, implementation, verification, and closure
- the repo-local `ledger.yml` remains canonical workflow state
- external systems are projections or evidence sources, not canonical state
- `/gadd:research` may inspect code read-only and write sanitized conclusions
- `/gadd:design` grounds the SDD in code and ADR reality
- `/gadd:setup` bootstraps one target repository

That model works for single-repo work but does not yet give agents a disciplined way to reason about product work that may require coordinated changes across multiple repositories.

## GitNexus Fit

GitNexus indexes repositories into graph-backed code intelligence: dependencies, call chains, functional clusters, execution flows, symbol context, impact analysis, and change detection. Its MCP server can serve multiple indexed repositories from a local registry.

Important boundary: GitNexus multi-repo support uses independent per-repo graphs. Cross-repo investigation is performed by querying specific repos and combining results in the agent or workflow layer. GADD should therefore treat GitNexus as structured evidence, not as a complete cross-repo truth source.

Sources reviewed:

- GitNexus overview: `https://gitnexus.homes/`
- GitNexus multi-repo architecture docs: `https://abhigyanpatwari-gitnexus.mintlify.app/mcp/multi-repo`

## Product Workflow Implication

A single Product Requirement may require work across multiple repositories. That does not automatically mean multiple PRDs. The Product Requirement should remain the product-scope unit: user outcome, business reason, acceptance criteria, constraints, and non-goals.

The PRD is the parent product contract that ties all SDD workstreams together. It ties them through shared product intent, acceptance criteria, constraints, non-goals, and closure conditions. It does not tie them through technical design, repo-specific architecture, implementation sequencing, API shape, schema details, or rollout mechanics.

The design layer should decide whether the approved PRD needs:

- one SDD for one cohesive code boundary
- multiple SDD workstreams for distinct repo, service, package, or architecture boundaries
- a shared contract, migration, or rollout SDD in addition to repo-local SDDs

GitNexus helps the agent make that decision by improving codebase discovery and impact analysis before SDD boundaries are chosen.

## Recommended Command Behavior

### `/gadd:setup`

`/gadd:setup` should become GitNexus-aware, not GitNexus-owning.

It should:

- detect whether GitNexus is available when practical
- detect whether the current repo appears indexed when practical
- optionally add advisory code-intelligence configuration to `.gadd/config.yml`
- recommend exact indexing commands for the current repo and configured related repos
- never silently install GitNexus
- never silently run indexing
- never silently mutate sibling repositories
- never block setup when GitNexus is missing

Recommended config shape:

```yaml
code_intelligence:
  preferred_tool: gitnexus
  recommendation_level: strong
  required: false
  related_repositories:
    - name: frontend
      path: ../frontend
    - name: backend
      path: ../backend
  freshness_policy:
    warn_when_stale: true
    block_when_stale: false
```

This keeps setup repo-local while allowing later commands to know which related repos should be considered.

### `/gadd:research`

Research should strongly recommend GitNexus when the product trigger needs codebase investigation, comparable behavior, architectural context, or possible multi-repo impact discovery.

Research output should record:

- whether GitNexus was used
- indexed repo names considered
- relevant indexed commits or staleness notes when available
- queries or evidence classes used
- sanitized codebase facts and constraints
- known limitations when GitNexus was unavailable or stale

Research should not use GitNexus findings to write product scope directly. It should turn them into codebase facts, explicit uncertainties, risks, constraints, or open questions. Any uncertainty that would affect scope or design must be stated directly and reviewed by a human before it can shape the next artifact.

### `/gadd:design`

Design should be the strongest GitNexus consumer.

Before writing or updating an SDD, `/gadd:design` should recommend GitNexus-backed discovery for:

- affected repos and systems
- relevant entry points, call chains, and functional clusters
- upstream and downstream impact
- possible SDD boundaries
- cross-repo sequencing and contract risks
- stale or missing index warnings

If GitNexus is unavailable, design continues with normal code inspection and records the limitation in the SDD.

If GitNexus is stale, design should warn clearly and either:

- continue with the stale-evidence limitation recorded, or
- ask the human whether to refresh the index before proceeding

It should not hard-block unless a future approved Product Requirement or team policy explicitly requires fresh GitNexus evidence.

### `/gadd:plan`

Planning should recommend GitNexus for expected file/module impact, slice boundaries, and review-load estimates.

The plan should record GitNexus-derived impact evidence only when it materially affects slice order, dependencies, risk, or expected files/modules.

### `/gadd:verify`

Verification may use GitNexus for optional blast-radius or change-impact checks, but it should not make child closure depend on GitNexus unless the approved plan explicitly required that evidence.

Verification remains a child-ticket closure-readiness gate, not a general repository healthcheck.

## Multi-Repo SDD Model

The eventual model should allow one PRD to own multiple SDD workstreams. The PRD remains the single parent Product Requirement for every workstream. Each SDD must trace back to the parent PRD and explain which part of the PRD's product contract it satisfies.

```text
Product Requirement / PRD
  -> parent product contract
  -> Design routing decision
      -> SDD workstream: repo A or service A
          -> plan
          -> child vertical slices
      -> SDD workstream: repo B or service B
          -> plan
          -> child vertical slices
      -> SDD workstream: shared contract, migration, or rollout
          -> plan
          -> child vertical slices
```

This is not part of the immediate setup change, but GitNexus-aware setup and design guidance should prepare for it.

## Ledger And Artifact Evidence

GADD should record GitNexus evidence as artifact context, not canonical state.

Appropriate places:

- `research.md`: sanitized codebase facts, indexed repos considered, freshness limitations
- `sdd.md`: repo impact map, SDD boundary reasoning, cross-repo risks
- `plan.md`: impact-informed slice order and expected files/modules
- `ledger.yml`: optional compact metadata about code-intelligence evidence, only if needed for workflow navigation or reproducibility

Avoid turning the ledger into a second GitNexus registry. GitNexus owns its index registry; GADD records which evidence informed a decision.

## Human Control And Safety

GitNexus-related operations may touch local files outside the current repo or write `.gitnexus/` indexes. GADD commands should therefore ask before running setup, install, analyze, clean, or cross-repo indexing commands.

Safe defaults:

- recommending commands is allowed
- reading configured GADD state is allowed
- reading GitNexus registry/context is allowed when available
- indexing or mutating another repo requires explicit human approval
- deleting indexes or cleaning registries is never automatic

## Open Follow-On Work

- Define the exact `.gadd/config.yml` schema for `code_intelligence`.
- Update `/gadd:setup` to add advisory config and guidance.
- Update `/gadd:research`, `/gadd:design`, `/gadd:plan`, and `/gadd:verify` with GitNexus recommendation language.
- Decide whether multi-SDD workstreams require new ledger schema fields or can first be represented as design output.
- Decide whether to add a later `/gadd:context` or `/gadd:index` command for workspace-level code intelligence.

## Non-Goals

- Do not make GitNexus mandatory for GADD.
- Do not replace repo-local ledgers with GitNexus state.
- Do not add a full cross-repo orchestration engine.
- Do not silently install tooling or mutate sibling repositories.
- Do not treat stale GitNexus indexes as fresh evidence.
- Do not require native cross-repo graph edges from GitNexus before GADD can support multi-repo design reasoning.
