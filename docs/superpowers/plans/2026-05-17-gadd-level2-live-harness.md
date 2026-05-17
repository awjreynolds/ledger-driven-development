# GADD Level 2 Live Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an automated Level 2 harness that seeds disposable target repositories from Level 1 fixtures and validates live-style GADD skill scenarios through a pluggable runner.

**Architecture:** Keep Level 1 as the deterministic routing oracle. Level 2 owns target-repo setup, scenario selection, runner invocation, transcript/diff capture, and assertions. The first committed runner is `fixture-next`, a deterministic adapter for `/gadd:next` smoke tests; real Codex/Claude/Gemini adapters can later reuse the same scenario format.

**Tech Stack:** Python 3 standard library, repo-local YAML subset parser style, shell validation scripts, existing `tests/level1` fixture corpus.

---

### Task 1: Level 2 Scenario Format And Runner Skeleton

**Files:**
- Create: `tests/level2/README.md`
- Create: `tests/level2/scenarios/next-smoke.yml`
- Create: `scripts/run-gadd-level2.py`
- Modify: `scripts/validate-gadd-mvp.sh`

- [x] **Step 1: Add a failing scenario-level check**

Create `tests/level2/scenarios/next-smoke.yml` with a read-only smoke case that maps to the existing Level 1 `full-prd-workflow` fixture and expects `/gadd:research GADD-L1-PRD`.

- [x] **Step 2: Run the missing runner and verify RED**

Run: `python3 scripts/run-gadd-level2.py --runner fixture-next`

Expected: FAIL because `scripts/run-gadd-level2.py` does not exist yet.

- [x] **Step 3: Implement minimal Level 2 runner**

Create `scripts/run-gadd-level2.py` with:
- YAML subset parsing for Level 2 scenario files.
- Temp repo creation under `/tmp` by default.
- Fixture copy from `tests/level1/fixtures/<source_scenario>/<fixture>`.
- Repo package copy for `skills/`, `commands/`, `agent-skills.json`, `GEMINI.md`, `README.md`, `CONTEXT.md`, and `docs/skills.md`.
- `fixture-next` runner that imports the Level 1 validator logic via `importlib`, derives the next command from seeded ledger state, writes a transcript file, and asserts `output_contains`, `changed_files`, and `no_external_mutation`.

- [x] **Step 4: Run Level 2 and verify GREEN**

Run: `python3 scripts/run-gadd-level2.py --runner fixture-next`

Expected: PASS with one scenario step validated.

- [x] **Step 5: Wire validation**

Modify `scripts/validate-gadd-mvp.sh` to run `python3 scripts/run-gadd-level2.py --runner fixture-next` after Level 1 validation.

- [x] **Step 6: Document Level 2**

Create `tests/level2/README.md` explaining the level boundary, runner model, scenario fields, and how to add read-only versus mutating live cases.

- [x] **Step 7: Run full validation**

Run: `./scripts/validate-gadd-mvp.sh`

Expected: PASS, including Level 1 and Level 2.
