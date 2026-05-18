# GAPS Command-Level Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate GADD-comparable command-level skill package skeletons from a GAPS process spec plus its implementation map.

**Architecture:** Preserve the current lane-level fallback for specs without an implementation map. When an implementation map is available, derive command-skill pairs, gates, required sections, required phrases, control-plane actions, and generated manifests from that map so generated output can be validated independently.

**Tech Stack:** Python stdlib generator, Ruby YAML bridge already used by the repo, unittest, existing GAPS validators.

---

### Task 1: Add Command-Level Regression Tests

**Files:**
- Modify: `tests/gaps/test_generate_gaps_skill_package.py`

- [ ] **Step 1: Add tests proving GADD generation emits published-skill-shaped names**

Add tests that run:

```bash
python3 scripts/generate-gaps-skill-package.py gaps/examples/gadd/ga-process.yml --output-root <tmp>
```

and assert generated files include `skills/gadd-refine/SKILL.md`, `skills/gadd-implement/SKILL.md`, `skills/gadd-verify/SKILL.md`, `commands/gadd/refine.md`, `commands/gadd/implement.md`, and `commands/gadd/verify.md`.

- [ ] **Step 2: Add validation test for generated implementation map**

Run the generated `implementation.yml` through:

```bash
python3 scripts/validate-gaps-implementation.py <tmp>/gaps/generated/gadd/implementation.yml
```

Expected first run before implementation: FAIL because generated preview roots/manifests do not yet describe command-level output.

### Task 2: Implement Implementation-Map Mode

**Files:**
- Modify: `scripts/generate-gaps-skill-package.py`

- [ ] **Step 1: Load an implementation map automatically**

If no flag is provided, discover `implementation.yml` beside the input `ga-process.yml`. Add `--implementation-map <path>` and `--no-implementation-map` flags for explicit control.

- [ ] **Step 2: Build command-level generation specs**

For each lane implementation, pair `commands[]` with `skills[]`. Merge repeated skills, especially `gadd-approve`, across lanes and control-plane actions. Carry lane evidence, gates, authority phrases, evidence phrases, required sections, global phrases, and control-plane required phrases into the generated skill spec.

- [ ] **Step 3: Render command-level skills**

Render one `SKILL.md` and `agents/openai.yaml` per generated skill. Include `## Input Quality Gate`, every required section from the implementation map, `## Rules`, and `## Stop Conditions`. Include authority/evidence phrases verbatim so the implementation validator can check them.

- [ ] **Step 4: Render full preview manifests**

Generate preview-local `agent-skills.json`, `.claude-plugin/plugin.json`, and `gemini-extension.json`, not only `agent-skills.patch.json`, so the generated implementation map is independently valid.

- [ ] **Step 5: Render preview-valid implementation map**

When generating preview output, write absolute `skillsRoot`, `commandsRoot`, package manifest, and adapter manifest paths into `implementation.yml`. When adopting output, keep repo-root-relative paths.

### Task 3: Docs And Validation Wiring

**Files:**
- Modify: `gaps/README.md`
- Modify: `skills/gaps-generate/SKILL.md`
- Modify: `scripts/validate-gadd-mvp.sh`

- [ ] **Step 1: Document implementation-map mode**

Explain that specs with adjacent implementation maps generate command-level skeletons; specs without maps still generate lane-level skeletons.

- [ ] **Step 2: Extend MVP smoke**

Keep the tiny fixture smoke for fallback mode and add a GADD smoke that validates the generated preview implementation map.

- [ ] **Step 3: Run full verification**

Run:

```bash
python3 scripts/validate-gaps.py
python3 scripts/validate-gaps-implementation.py
python3 -m unittest discover tests/gaps
./scripts/validate-gadd-mvp.sh
git diff --check
```
