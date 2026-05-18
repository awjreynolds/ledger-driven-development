# GAPS GADD Operationalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make GADD operationally implemented through GAPS by adding an implementation map, an implementation-conformance validator, and minimal GAPS authoring/validation skills.

**Architecture:** Keep `gaps/examples/gadd/ga-process.yml` as the process specification and add `gaps/examples/gadd/implementation.yml` as the binding from the GAPS process to the actual GADD package: skills, commands, adapters, and validation scripts. Add a Python stdlib validator that loads the process spec and implementation map through the existing Ruby YAML bridge, then checks that referenced skills, command adapters, manifests, gate/authority/evidence phrases, and package exports exist. Add `/gaps:author` and `/gaps:validate` as standalone agent skills so users can author and validate GAPS process specs repeatably.

**Tech Stack:** YAML, JSON, Python stdlib, Ruby stdlib YAML-to-JSON bridge, existing Agent Skills manifest and command adapter patterns.

---

## File Structure

- Create `gaps/examples/gadd/implementation.yml`: the concrete implementation map from the GAPS GADD process spec to repo files.
- Create `gaps/schema/implementation.schema.json`: permissive schema for implementation maps.
- Create `scripts/validate-gaps-implementation.py`: validates the GADD implementation map against the GAPS process and actual repo files.
- Create `tests/gaps/test_validate_gaps_implementation.py`: regression tests for valid implementation and invalid maps.
- Create `skills/gaps-author/SKILL.md` and `skills/gaps-validate/SKILL.md`: minimal GAPS authoring and validation workflow skills.
- Create `skills/gaps-author/agents/openai.yaml` and `skills/gaps-validate/agents/openai.yaml`: Codex skill metadata.
- Create `commands/gaps/author.md`, `commands/gaps/author.toml`, `commands/gaps/validate.md`, `commands/gaps/validate.toml`: adapter commands.
- Modify `agent-skills.json`, `.claude-plugin/plugin.json`, `gemini-extension.json`, `gaps/README.md`, `README.md`, and `scripts/validate-gadd-mvp.sh`.

---

### Task 1: GADD Implementation Map

**Files:**
- Create: `gaps/examples/gadd/implementation.yml`
- Create: `gaps/schema/implementation.schema.json`

- [ ] **Step 1: Add the implementation map**

Create `gaps/examples/gadd/implementation.yml` with:

```yaml
schemaVersion: "0.1"
processSpec: gaps/examples/gadd/ga-process.yml
processId: gadd
implementationType: agent_skill_package
packageManifest: agent-skills.json
skillsRoot: skills
commandsRoot: commands
adapterManifests:
  claude: .claude-plugin/plugin.json
  gemini: gemini-extension.json
validators:
  - scripts/validate-gaps.py
  - scripts/validate-gaps-implementation.py
  - scripts/validate-gadd-mvp.sh
```

Add one `laneImplementations` entry for each GADD process lane. Each entry must map GAPS lane ids to concrete skills, slash commands, gate ids, authority phrases, evidence phrases, and required skill sections.

- [ ] **Step 2: Add implementation schema**

Create `gaps/schema/implementation.schema.json` requiring `schemaVersion`, `processSpec`, `processId`, `implementationType`, `packageManifest`, `skillsRoot`, `commandsRoot`, `adapterManifests`, `validators`, and `laneImplementations`. Keep `additionalProperties: true` so the map can evolve.

- [ ] **Step 3: Commit**

```bash
git add gaps/examples/gadd/implementation.yml gaps/schema/implementation.schema.json
git commit -m "Map GADD implementation to GAPS"
```

---

### Task 2: Implementation Validator

**Files:**
- Create: `scripts/validate-gaps-implementation.py`
- Create: `tests/gaps/test_validate_gaps_implementation.py`

- [ ] **Step 1: Add failing tests**

Create tests that run:

```python
def test_gadd_implementation_map_passes():
    result = run_validator()
    assert result.returncode == 0, result.stderr + result.stdout

def test_missing_skill_fails(tmp_path):
    spec = write_invalid_map(tmp_path, lambda data: data["laneImplementations"]["intake"]["skills"].append("missing-skill"))
    result = run_validator(spec)
    assert result.returncode == 1
    assert "missing-skill" in result.stderr

def test_unmapped_process_lane_fails(tmp_path):
    spec = write_invalid_map(tmp_path, lambda data: data["laneImplementations"].pop("implementation"))
    result = run_validator(spec)
    assert result.returncode == 1
    assert "implementation" in result.stderr
```

- [ ] **Step 2: Implement validator**

The validator must:

```python
process = load_yaml(map_path.parent / map_data["processSpec"])
implementation = load_yaml(map_path)
manifest = load_json(root / implementation["packageManifest"])
```

Then check:

- `implementation.processId == process.process.id`
- every process lane has a matching `laneImplementations` entry
- every mapped skill directory exists with `SKILL.md`
- every mapped slash command exists in `agent-skills.json`
- every command adapter exists under `commands/gadd/*.md` and `commands/gadd/*.toml`
- Claude and Gemini manifests expose every mapped command
- each mapped gate id exists in the process lane
- each required phrase exists in the relevant `SKILL.md`
- every validator path exists

- [ ] **Step 3: Run tests**

Run:

```bash
python3 -m unittest discover tests/gaps
```

Expected: all GAPS tests pass.

- [ ] **Step 4: Commit**

```bash
git add scripts/validate-gaps-implementation.py tests/gaps/test_validate_gaps_implementation.py
git commit -m "Validate GADD implementation against GAPS"
```

---

### Task 3: GAPS Skills And Commands

**Files:**
- Create: `skills/gaps-author/SKILL.md`
- Create: `skills/gaps-author/agents/openai.yaml`
- Create: `skills/gaps-validate/SKILL.md`
- Create: `skills/gaps-validate/agents/openai.yaml`
- Create: `commands/gaps/author.md`
- Create: `commands/gaps/author.toml`
- Create: `commands/gaps/validate.md`
- Create: `commands/gaps/validate.toml`
- Modify: `agent-skills.json`
- Modify: `.claude-plugin/plugin.json`
- Modify: `gemini-extension.json`

- [ ] **Step 1: Add `/gaps:author` skill and adapters**

The author skill must read `gaps/README.md`, `gaps/schema/ga-process.schema.json`, existing examples, and any source process docs. It writes or updates `gaps/examples/<process-id>/ga-process.yml` only after preserving explicit non-goals, known gaps, standards posture, and no-compliance-claim warnings.

- [ ] **Step 2: Add `/gaps:validate` skill and adapters**

The validate skill must run:

```bash
python3 scripts/validate-gaps.py
python3 scripts/validate-gaps-implementation.py
```

It should report whether process specs and implementation maps pass, and must not claim legal/regulatory compliance.

- [ ] **Step 3: Add commands to manifests**

Add `/gaps:author` and `/gaps:validate` to `agent-skills.json`, `.claude-plugin/plugin.json`, and `gemini-extension.json`.

- [ ] **Step 4: Commit**

```bash
git add skills/gaps-author skills/gaps-validate commands/gaps agent-skills.json .claude-plugin/plugin.json gemini-extension.json
git commit -m "Add GAPS authoring and validation skills"
```

---

### Task 4: MVP Wiring And Docs

**Files:**
- Modify: `scripts/validate-gadd-mvp.sh`
- Modify: `gaps/README.md`
- Modify: `README.md`

- [ ] **Step 1: Wire implementation validation into MVP checks**

Add required files for the GAPS implementation map, implementation schema, implementation validator, GAPS commands, and GAPS skills. Add:

```sh
python3 scripts/validate-gaps-implementation.py
```

near the existing GAPS validator call.

- [ ] **Step 2: Update docs**

Update `gaps/README.md` to state that GADD is now bound to GAPS through `examples/gadd/implementation.yml`, and that `/gaps:validate` checks both process specs and implementation maps.

Update the top-level README command list with:

```markdown
- `/gaps:author` - Author or revise a GAPS process specification from an existing governed process.
- `/gaps:validate` - Validate GAPS process specs and implementation maps.
```

- [ ] **Step 3: Run full verification**

Run:

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
git commit -m "Wire GAPS implementation validation into MVP"
```

---

## Self-Review

- Spec coverage: this plan implements GADD through GAPS by binding the GAPS process spec to the actual skill package and validating that binding.
- Scope discipline: it does not add BAML extraction, Archon runtime emission, BPMN/CMMN/DMN export, OSCAL export, or legal/regulatory conformance claims.
- Type consistency: process spec fields remain in `ga-process.yml`; implementation binding fields live in `implementation.yml` and use `laneImplementations`, `skillContracts`, and `adapterManifests`.
