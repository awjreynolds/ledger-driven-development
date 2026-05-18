# GAPS Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a dry-run-first GAPS skill-package generator that turns a validated `ga-process.yml` into proposed skill skeletons, command adapters, manifest patches, implementation map, and validation checklist.

**Architecture:** The generator is a Python stdlib CLI that loads a GAPS process spec through the same Ruby YAML bridge used by validators. By default it writes generated files to a preview directory under `gaps/generated/<process-id>/` so users can review before adopting. `--write --output-root <dir>` writes into an explicit target. Generated files include strong non-claim language and human-review gates; validation remains separate through `/gaps:validate`.

**Tech Stack:** Python stdlib, Ruby stdlib YAML-to-JSON bridge, YAML text rendering, existing GAPS schemas and skill/command adapter patterns.

---

## File Structure

- Create `scripts/generate-gaps-skill-package.py`: dry-run generator CLI.
- Create `tests/gaps/fixtures/tiny-process/ga-process.yml`: small process fixture for stable generator tests.
- Create `tests/gaps/test_generate_gaps_skill_package.py`: stdlib tests for dry-run output and write guardrails.
- Create `skills/gaps-generate/SKILL.md` and `skills/gaps-generate/agents/openai.yaml`: user-facing generator skill.
- Create `commands/gaps/generate.md` and `commands/gaps/generate.toml`: command adapters.
- Modify `agent-skills.json`, `.claude-plugin/plugin.json`, `gemini-extension.json`, `gaps/README.md`, `README.md`, and `scripts/validate-gadd-mvp.sh`.

---

### Task 1: Generator CLI And Tests

**Files:**
- Create: `scripts/generate-gaps-skill-package.py`
- Create: `tests/gaps/fixtures/tiny-process/ga-process.yml`
- Create: `tests/gaps/test_generate_gaps_skill_package.py`

- [ ] **Step 1: Add fixture process**

Create a tiny process with two lanes, one control-plane action, required GAPS fields, and no compliance claims.

- [ ] **Step 2: Add failing tests**

Tests must verify:

```python
def test_dry_run_generates_preview_files(tmp_path):
    result = run_generator("--output-root", tmp_path)
    assert result.returncode == 0
    assert (tmp_path / "gaps" / "generated" / "tiny_process" / "skills" / "tiny-process-intake" / "SKILL.md").is_file()

def test_default_mode_does_not_modify_package_roots(tmp_path):
    result = run_generator("--output-root", tmp_path)
    assert result.returncode == 0
    assert not (tmp_path / "skills").exists()
    assert not (tmp_path / "commands").exists()

def test_write_requires_explicit_flag(tmp_path):
    result = run_generator("--adopt-output", "--output-root", tmp_path)
    assert result.returncode == 2
    assert "--write" in result.stderr
```

- [ ] **Step 3: Implement generator**

CLI:

```bash
python3 scripts/generate-gaps-skill-package.py <ga-process.yml> [--output-root DIR] [--write] [--adopt-output]
```

Behavior:

- default output root is repository root
- default mode writes under `gaps/generated/<process-id>/`
- `--write --adopt-output` writes package files under `skills/`, `commands/`, plus generated manifest patch and `implementation.yml`
- `--adopt-output` without `--write` exits 2
- generated artifacts include `README.generated.md`, skill skeletons, command adapters, `agent-skills.patch.json`, `implementation.yml`, and `validation-checklist.md`

- [ ] **Step 4: Run tests**

```bash
python3 -m unittest tests.gaps.test_generate_gaps_skill_package
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/generate-gaps-skill-package.py tests/gaps/fixtures/tiny-process/ga-process.yml tests/gaps/test_generate_gaps_skill_package.py
git commit -m "Add GAPS skill package generator"
```

---

### Task 2: Generator Skill And Manifest Wiring

**Files:**
- Create: `skills/gaps-generate/SKILL.md`
- Create: `skills/gaps-generate/agents/openai.yaml`
- Create: `commands/gaps/generate.md`
- Create: `commands/gaps/generate.toml`
- Modify: `agent-skills.json`
- Modify: `.claude-plugin/plugin.json`
- Modify: `gemini-extension.json`

- [ ] **Step 1: Add `/gaps:generate` skill**

The skill must run validation first:

```bash
python3 scripts/validate-gaps.py <ga-process.yml>
```

Then run the generator in dry-run mode by default:

```bash
python3 scripts/generate-gaps-skill-package.py <ga-process.yml>
```

It must not adopt generated files into package roots unless the user explicitly requests write/adopt mode.

- [ ] **Step 2: Add adapters and manifests**

Add `/gaps:generate` to the Agent Skills manifest, Claude plugin, and Gemini extension.

- [ ] **Step 3: Commit**

```bash
git add skills/gaps-generate commands/gaps/generate.md commands/gaps/generate.toml agent-skills.json .claude-plugin/plugin.json gemini-extension.json
git commit -m "Add GAPS generator skill"
```

---

### Task 3: MVP Wiring And Docs

**Files:**
- Modify: `scripts/validate-gadd-mvp.sh`
- Modify: `gaps/README.md`
- Modify: `README.md`

- [ ] **Step 1: Wire files into MVP checks**

Add required file checks for the generator script, generator tests, fixture, skill, adapters, and metadata. Add:

```sh
python3 -m unittest tests.gaps.test_generate_gaps_skill_package
python3 scripts/generate-gaps-skill-package.py tests/gaps/fixtures/tiny-process/ga-process.yml --output-root /tmp/gaps-generator-check
```

- [ ] **Step 2: Update docs**

Document `/gaps:generate`, dry-run-first behavior, generated output paths, and non-claims.

- [ ] **Step 3: Run full verification**

```bash
python3 scripts/validate-gaps.py
python3 scripts/validate-gaps-implementation.py
python3 -m unittest discover tests/gaps
./scripts/validate-gadd-mvp.sh
git diff --check
```

Expected: all commands exit 0.

- [ ] **Step 4: Commit**

```bash
git add scripts/validate-gadd-mvp.sh gaps/README.md README.md
git commit -m "Wire GAPS generator into validation"
```

---

## Self-Review

- Scope: generate skill-package skeletons and review artifacts only; no runtime engine, standards export, or compliance claims.
- Safety: dry-run preview is the default; adoption requires explicit `--write --adopt-output`.
- Reuse: generator follows existing skill and command adapter patterns rather than inventing a new package layout.
