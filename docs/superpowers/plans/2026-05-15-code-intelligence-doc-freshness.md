# Code Intelligence And Documentation Freshness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update GADD command contracts, templates, README, and validation so GitNexus is strongly recommended for code intelligence and every implementation slice accounts for documentation impact.

**Architecture:** This is a contract/documentation change in the GADD skill package. The canonical behavior lives in `skills/gadd-*/SKILL.md`; setup templates under `skills/gadd-setup/assets/templates/` define target-repo artifact shapes; `README.md` describes the public package contract; `scripts/validate-gadd-mvp.sh` enforces key package invariants.

**Tech Stack:** Markdown skill files, YAML templates, shell validation with `grep`, git.

---

### Task 1: Add GitNexus advisory code-intelligence contract

**Files:**
- Modify: `skills/gadd-setup/SKILL.md`
- Modify: `skills/gadd-setup/assets/templates/config.yml`
- Modify: `skills/gadd-research/SKILL.md`
- Modify: `skills/gadd-design/SKILL.md`
- Modify: `skills/gadd-plan/SKILL.md`
- Modify: `skills/gadd-verify/SKILL.md`
- Modify: `README.md`

- [x] **Step 1: Update setup contract**

Add GitNexus-aware setup guidance: setup may detect availability/index state, may write advisory config, must recommend commands rather than silently install/index, and must not block setup when GitNexus is absent.

- [x] **Step 2: Update config template**

Add:

```yaml
code_intelligence:
  preferred_tool: gitnexus
  recommendation_level: strong
  required: false
  related_repositories: []
  freshness_policy:
    warn_when_stale: true
    block_when_stale: false
```

- [x] **Step 3: Update research/design/plan/verify**

Add command-local GitNexus recommendation language:

- research records whether GitNexus was used, repos considered, staleness, queries/evidence classes, and limitations.
- design is the strongest GitNexus consumer and uses it for affected repos/systems, SDD boundaries, impact, and stale-index warnings.
- plan recommends GitNexus for expected files/modules, slice boundaries, and review load.
- verify may use GitNexus optionally for blast-radius/change-impact checks, but never turns closure into a broad repo audit.

- [x] **Step 4: Update README**

Add public README language that GitNexus is strongly recommended when code reality matters, especially multi-repo impact and SDD boundary decisions, while remaining advisory.

### Task 2: Add documentation freshness contract

**Files:**
- Modify: `skills/gadd-setup/assets/templates/plan.md`
- Modify: `skills/gadd-setup/assets/templates/issue-body-child.md`
- Modify: `skills/gadd-implement/SKILL.md`
- Modify: `skills/gadd-verify/SKILL.md`
- Modify: `README.md`

- [x] **Step 1: Update plan template**

Add documentation impact to slice planning and review checklist. Each slice should identify docs updated, docs not needed with reason, or docs blocked.

- [x] **Step 2: Update child ticket template**

Add a `Documentation impact` section so implementation agents do not infer docs obligations from the parent plan.

- [x] **Step 3: Update implement contract**

Require implementation completion evidence to include `updated`, `not_needed`, or `blocked` documentation impact. Do not mark implementation completed when documentation impact is blocked.

- [x] **Step 4: Update verify contract**

Require verification to read docs evidence and block closure when docs impact is missing or blocked for user-facing behavior, command behavior, public APIs, configuration, setup flow, templates, integration contracts, or operational workflow.

- [x] **Step 5: Update README**

State that docs freshness is part of implementation evidence and verification.

### Task 3: Update validation and verify

**Files:**
- Modify: `scripts/validate-gadd-mvp.sh`

- [x] **Step 1: Add validation greps**

Add targeted checks for:

- `code_intelligence` in the config template
- `GitNexus` in README and relevant command skills
- `Documentation impact` in plan and child issue templates
- documentation impact evidence in `/gadd:implement`
- documentation impact verification in `/gadd:verify`

- [x] **Step 2: Run validation**

Run:

```sh
./scripts/validate-gadd-mvp.sh
git diff --check
```

Expected: both pass.

- [x] **Step 3: Commit and push**

Commit the package updates and push `main`.
