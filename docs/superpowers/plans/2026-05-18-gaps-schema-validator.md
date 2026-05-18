# GAPS Schema Validator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote GAPS from an exploratory two-file reference to a validated incubation profile with a second reference process, JSON Schema, validator, tests, and MVP validation wiring.

**Architecture:** Keep `ga-process.yml` as the canonical authored artifact and validate it with a permissive JSON Schema plus GAPS-specific semantic checks. The validator loads YAML through the system Ruby YAML parser, then performs schema and semantic validation in Python without adding package dependencies. The schema stays intentionally profile-shaped and permits additional fields so the second reference process can still teach the model before a frozen standard exists.

**Tech Stack:** YAML reference files, JSON Schema document, Python stdlib validator and `unittest`, Ruby stdlib YAML-to-JSON bridge for YAML parsing.

---

## File Structure

- Create `gaps/examples/compliance-review/ga-process.yml`: unlike-GADD reference process stressing adaptive casework, time limits, identity, budget gates, multiple authority levels, and event-driven escalation.
- Create `gaps/schema/ga-process.schema.json`: permissive v0.1 JSON Schema for required GAPS profile fields, enums, and repeated lane/gate/control-mapping shapes.
- Create `scripts/validate-gaps.py`: dependency-light validator that loads every `gaps/examples/*/ga-process.yml`, validates against the schema, and runs semantic checks not expressible in the small schema subset.
- Create `tests/gaps/test_validate_gaps.py`: stdlib tests for valid examples and invalid examples.
- Modify `scripts/validate-gadd-mvp.sh`: add GAPS file requirements and run the GAPS validator as part of the repo MVP validation.
- Modify `gaps/README.md`: update status, explain schema/validator commands, second reference process, and remaining incubation boundaries.

---

### Task 1: Second Reference Process

**Files:**
- Create: `gaps/examples/compliance-review/ga-process.yml`
- Modify: `gaps/README.md`

- [ ] **Step 1: Create the compliance-review reference**

Add a full process file with this shape:

```yaml
schemaVersion: "0.1"
status: exploratory
formatWarning: "GAPS v0.1 is not stable. This file is a reference process, not a formal schema or compliance artifact."
standards_alignment:
  posture: "GAPS is a Governed Autonomy profile layered over existing process and control standards."
  compatible_concepts:
    - standard: cmmn
      applies_to:
        - adaptive case state
        - event-driven escalation
      status: candidate
  standard_aliases:
    - concept: case milestone
      aliases:
        - standard: cmmn
          term: milestone
        - standard: gaps
          term: gate
      status: candidate
  gaps_extensions:
    - autonomy_tier
    - authority_plane
    - drift_freshness
    - governed_autonomy_risk_patterns
```

The file must include process metadata, canonical state, freshness, roles, autonomy vocabulary, at least four lanes, control-plane actions, projections, risk patterns, control mappings, and known gaps.

- [ ] **Step 2: Validate YAML loads**

Run:

```bash
ruby -ryaml -rjson -e 'puts JSON.generate(YAML.load_file(ARGV[0]))' gaps/examples/compliance-review/ga-process.yml >/tmp/gaps-compliance-review.json
```

Expected: command exits 0 and writes JSON to `/tmp/gaps-compliance-review.json`.

- [ ] **Step 3: Commit**

```bash
git add gaps/examples/compliance-review/ga-process.yml gaps/README.md
git commit -m "Add GAPS compliance review reference process"
```

---

### Task 2: Schema And Validator Tests

**Files:**
- Create: `gaps/schema/ga-process.schema.json`
- Create: `tests/gaps/test_validate_gaps.py`

- [ ] **Step 1: Add schema file**

Create a JSON Schema with these required top-level fields:

```json
[
  "schemaVersion",
  "status",
  "formatWarning",
  "standards_alignment",
  "process",
  "canonicalState",
  "freshness",
  "roles",
  "autonomyVocabulary",
  "lanes",
  "governedAutonomyRiskPatterns",
  "controlMappings",
  "knownGaps"
]
```

The schema must require `gateType`, `approvalRole`, `approvalCondition`, and `escalationCondition` for each gate, and must require `source`, `controlId`, `mappingStatus`, `implementationStatus`, and `evidenceReferences` for each control mapping.

- [ ] **Step 2: Add failing validator tests**

Create `tests/gaps/test_validate_gaps.py` with these tests:

```python
def test_valid_examples_pass():
    result = run_validator()
    assert result.returncode == 0, result.stderr + result.stdout

def test_missing_known_gaps_fails(tmp_path):
    spec = write_invalid_spec(tmp_path, lambda data: data.pop("knownGaps"))
    result = run_validator(spec)
    assert result.returncode == 1
    assert "knownGaps" in result.stderr

def test_invalid_gate_type_fails(tmp_path):
    def mutate(data):
        first_lane = next(iter(data["lanes"].values()))
        first_lane["gates"][0]["gateType"] = "rubber_stamp"
    spec = write_invalid_spec(tmp_path, mutate)
    result = run_validator(spec)
    assert result.returncode == 1
    assert "gateType" in result.stderr

def test_stale_standards_alignment_name_fails(tmp_path):
    def mutate(data):
        data["standardsAlignment"] = data.pop("standards_alignment")
    spec = write_invalid_spec(tmp_path, mutate)
    result = run_validator(spec)
    assert result.returncode == 1
    assert "standards_alignment" in result.stderr
```

- [ ] **Step 3: Run tests to verify failure**

Run:

```bash
python3 -m unittest discover tests/gaps
```

Expected: FAIL because `scripts/validate-gaps.py` does not exist yet.

---

### Task 3: Validator Implementation

**Files:**
- Create: `scripts/validate-gaps.py`
- Modify: `tests/gaps/test_validate_gaps.py` if test helper paths need adjustment

- [ ] **Step 1: Implement YAML loading**

Implement `load_yaml(path)` by invoking:

```python
subprocess.run(
    ["ruby", "-ryaml", "-rjson", "-e", "puts JSON.generate(YAML.load_file(ARGV[0]))", str(path)],
    text=True,
    capture_output=True,
    check=False,
)
```

Return `json.loads(stdout)` on success and raise `ValidationError` with stderr on failure.

- [ ] **Step 2: Implement schema subset validation**

Implement recursive validation for `type`, `required`, `enum`, `properties`, `items`, and `additionalProperties`. Report paths such as `lanes.intake.gates.0.gateType`.

- [ ] **Step 3: Implement GAPS semantic checks**

Add checks that:

```python
if "standardsAlignment" in spec:
    error("standardsAlignment is stale; use standards_alignment")
if "standard_aliases" not in spec["standards_alignment"]:
    error("standards_alignment.standard_aliases is required")
if not spec["lanes"]:
    error("lanes must contain at least one lane")
```

Each lane must include `purpose`, `authority.plane`, `authority.autonomyTier`, `authority.riskTier`, `evidence.input`, `evidence.completion`, and at least one gate. Each control mapping must have a valid `mappingStatus`. `knownGaps` must be non-empty.

- [ ] **Step 4: Run validator tests**

Run:

```bash
python3 -m unittest discover tests/gaps
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add gaps/schema/ga-process.schema.json scripts/validate-gaps.py tests/gaps/test_validate_gaps.py
git commit -m "Add GAPS schema validator"
```

---

### Task 4: Validation Wiring And Documentation

**Files:**
- Modify: `scripts/validate-gadd-mvp.sh`
- Modify: `gaps/README.md`

- [ ] **Step 1: Wire files into MVP validation**

Add these required files to the `required_files` block:

```sh
gaps/README.md
gaps/schema/ga-process.schema.json
gaps/examples/gadd/ga-process.yml
gaps/examples/compliance-review/ga-process.yml
scripts/validate-gaps.py
```

Add this command near the other Python validators:

```sh
python3 scripts/validate-gaps.py
```

- [ ] **Step 2: Update README**

Document:

```markdown
## Validation

Run:

```bash
python3 scripts/validate-gaps.py
```

The validator checks every `gaps/examples/*/ga-process.yml` file against `gaps/schema/ga-process.schema.json` and GAPS-specific semantic rules.
```

Also state that validator success is not regulatory compliance, certification, proof of executable correctness, or a BPMN/CMMN/DMN/OSCAL export.

- [ ] **Step 3: Run full verification**

Run:

```bash
python3 scripts/validate-gaps.py
python3 -m unittest discover tests/gaps
python3 scripts/validate-gadd-docs.py
./scripts/validate-gadd-mvp.sh
git diff --check
```

Expected: every command exits 0.

- [ ] **Step 4: Commit**

```bash
git add scripts/validate-gadd-mvp.sh gaps/README.md
git commit -m "Validate GAPS in MVP checks"
```

---

## Self-Review

- Spec coverage: this plan covers the approved v0.2 path by adding a second unlike reference process, schema, validator, tests, docs, and MVP validation wiring.
- Scope discipline: it does not add GAPS skills, runtime emission, BAML extraction, Archon execution, BPMN/CMMN/DMN export, OSCAL export, or legal compliance claims.
- Type consistency: field names use existing `ga-process.yml` casing: `schemaVersion`, `standards_alignment`, `canonicalState`, `autonomyVocabulary`, `governedAutonomyRiskPatterns`, `controlMappings`, and `knownGaps`.
