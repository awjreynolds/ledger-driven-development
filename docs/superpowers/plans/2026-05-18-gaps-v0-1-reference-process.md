# GAPS v0.1 Reference Process Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Introduce GAPS v0.1 as an incubating Governed Autonomy profile layer with GADD as the first reference process.

**Architecture:** Add a top-level `gaps/` area with one README and one hand-authored GADD reference process file. Keep GAPS as a profile/crosswalk layer over existing standards rather than a competing process notation. Add only a one-line top-level README pointer so GADD remains the public entry point.

**Tech Stack:** Markdown, YAML, existing Python validation scripts.

---

## File structure

- Create: `gaps/README.md`
  Explains GAPS, incubation status, relationship to GADD, prior-art stance, v0.1 limits, and next gates.
- Create: `gaps/examples/gadd/ga-process.yml`
  Describes GADD as the first GAPS reference process with schema version, standards alignment, lanes, authority planes, gates, evidence, state/projection policy, drift/freshness, and known gaps.
- Modify: `README.md`
  Adds one concise pointer to `gaps/` under "More Detail".

No schema, validator, GAPS commands, GAPS skills, generator, or runtime emission target should be added in this implementation slice.

---

### Task 1: Add the GAPS README

**Files:**
- Create: `gaps/README.md`

- [ ] **Step 1: Create the directory**

Run:

```bash
mkdir -p gaps/examples/gadd
```

Expected: command exits with status 0 and creates the directory tree.

- [ ] **Step 2: Write `gaps/README.md`**

Create `gaps/README.md` with this content:

```markdown
# GAPS

GAPS is the **Governed Autonomy Process Specification** layer incubating in this repository.

GADD is the concrete software-delivery methodology. GAPS is the emerging profile for describing how a governed process preserves accountability, authority, autonomy boundaries, evidence, escalation, approval, state, projection, verification, closure, and external control mappings when autonomous systems may participate.

## Status

GAPS v0.1 is exploratory.

The current v0.1 surface is intentionally small:

- `examples/gadd/ga-process.yml` expresses GADD as the first reference process.
- This README explains the incubation model and boundaries.

There is no GAPS schema, validator, command suite, generator, or runtime target yet.

## Relationship to existing standards

GAPS is not intended to become a competing process notation.

Where existing standards already own a concept, GAPS should align with them rather than re-derive them:

- BPMN for structured process flow.
- CMMN for adaptive case-style work.
- DMN for decision and policy logic.
- OSCAL-style structures for control mappings, implementation status, and evidence.
- NIST AI RMF, ISO/IEC 42001, and the EU AI Act as governance and regulatory anchors where applicable.

The intended GAPS contribution is the Governed Autonomy profile layered over that substrate:

- autonomy tier
- authority plane
- gate type
- human accountability
- evidence contract
- escalation and approval separation
- canonical state and projection rule
- drift and freshness rule
- Governed Autonomy risk-pattern coverage
- external control mapping stubs

## Why GADD is the first reference process

GADD already implements Governed Autonomy for the software-delivery process: intake, triage, product scope, technical design, planning, implementation, verification, closure, and archive cleanup.

Using GADD first keeps GAPS grounded in a real process with existing skills, templates, ledgers, tests, and docs. If GAPS cannot describe GADD faithfully, the GAPS model is not ready to generalize.

## V0.1 completion rule

The GADD reference process should be faithful and explicit, not exhaustive.

The reference process is acceptable when:

- every current GADD lane and approval boundary is represented
- core fields are present where they apply
- missing or weak concepts are recorded as known gaps
- optional fields are used only when they describe real GADD behavior
- no regulatory, safety, validator, generation, or runtime execution support is claimed

Sparse but honest is better than a large file that invents structure GADD does not yet have.

## Second reference process gate

Before adding a schema, validator, GAPS skills, generation, or runtime emission, GAPS needs a second reference process that is intentionally unlike GADD.

Good candidates include:

- compliance review
- service-request case handling
- procurement approval
- incident response
- public-sector casework

The second process should stress adaptive flow, long-running state, statutory deadlines, named human identities, multiple authority levels, budget or resource gates, and event-driven escalation.

## Files

- `examples/gadd/ga-process.yml` - GADD as the first GAPS reference process.
```

- [ ] **Step 3: Review the README for overclaiming**

Run:

```bash
rg -n "schema|validator|generator|runtime|compliance|certification|supports" gaps/README.md
```

Expected: each hit is either a negative boundary, an incubation statement, or a future-gate statement. No sentence claims current schema, validation, compliance, certification, generation, or runtime support.

- [ ] **Step 4: Commit the GAPS README**

Run:

```bash
git add gaps/README.md
git commit -m "Add GAPS incubation README"
```

Expected: commit succeeds and includes only `gaps/README.md`.

---

### Task 2: Add the GADD reference process

**Files:**
- Create: `gaps/examples/gadd/ga-process.yml`

- [ ] **Step 1: Write `gaps/examples/gadd/ga-process.yml`**

Create `gaps/examples/gadd/ga-process.yml` with this content:

```yaml
schemaVersion: "0.1"
status: exploratory
formatWarning: "GAPS v0.1 is not stable. This file is a reference process, not a formal schema or compliance artifact."

process:
  id: gadd
  name: Governed Autonomy for Software Delivery
  purpose: >
    Govern SDLC work from intake through triage, product scope, technical design,
    planning, implementation, verification, closure, and optional archive cleanup.
  scope:
    includes:
      - unclassified software-delivery intake
      - product requirement discovery and approval
      - repo-scoped software design
      - implementation planning and decomposition
      - bounded implementation
      - verification and closure
      - optional local archive cleanup
    excludes:
      - enterprise portfolio planning
      - deployment operations
      - long-term maintenance operations
      - non-software business processes
  standardsAlignment:
    posture: "GAPS is a Governed Autonomy profile, not a replacement for BPMN, CMMN, DMN, or OSCAL."
    compatibleConcepts:
      - standard: bpmn
        appliesTo:
          - process states
          - governed transitions
          - phase gates
        status: candidate
      - standard: dmn
        appliesTo:
          - route decisions
          - approval conditions
          - triage state selection
        status: candidate
      - standard: oscal
        appliesTo:
          - control mappings
          - evidence references
          - implementation status
        status: candidate
    gapsExtensions:
      - autonomy_tier
      - authority_plane
      - drift_freshness
      - governed_autonomy_risk_patterns

canonicalState:
  source: repo-local-ledger
  pathPattern: "gadd/work-items/**/ledger.yml"
  relationshipToGaps:
    gaProcessYml: "Describes the process type: roles, transitions, gates, evidence requirements, projections, and known gaps."
    ledgerYml: "Records one Work Item's current execution state inside the GADD process."
  projectionRule: "External systems are collaboration surfaces, not canonical workflow state."

freshness:
  reviewedAt: "2026-05-18"
  implementedBy:
    skillFiles:
      - skills/gadd-setup/SKILL.md
      - skills/gadd-next/SKILL.md
      - skills/gadd-triage/SKILL.md
      - skills/gadd-research/SKILL.md
      - skills/gadd-scope/SKILL.md
      - skills/gadd-elaborate/SKILL.md
      - skills/gadd-refine/SKILL.md
      - skills/gadd-approve/SKILL.md
      - skills/gadd-design/SKILL.md
      - skills/gadd-plan/SKILL.md
      - skills/gadd-decompose/SKILL.md
      - skills/gadd-implement/SKILL.md
      - skills/gadd-verify/SKILL.md
      - skills/gadd-close/SKILL.md
      - skills/gadd-archive/SKILL.md
    ledgerTemplates:
      - skills/gadd-setup/assets/templates/work-item-ledger.yml
  driftPolicy: >
    If GADD skill behavior changes before this reference process is updated,
    record a known gap in this file or create a follow-up Work Item. Do not
    silently treat either artifact as authoritative when they disagree.

roles:
  process_owner:
    label: Team or organization adopting GADD
    decisionRights:
      - adopt GADD for the repository
      - set tracker and projection policy
      - decide when GAPS should be extracted or generalized
  product_authority:
    label: Product Manager or equivalent product owner
    decisionRights:
      - approve product scope
      - resolve product acceptance criteria
      - approve Product Requirement boundaries
  technical_authority:
    label: EM, Tech Lead, Architect, or senior engineer
    decisionRights:
      - approve technical design readiness
      - decide whether plan and decomposition are required
      - resolve architectural trade-offs
  operator:
    label: Software Engineer or autonomous coding agent inside approved boundary
    decisionRights:
      - implement approved Work Items
      - run tests and collect implementation evidence
      - stop when approved boundaries are insufficient
  reviewer:
    label: Engineering reviewer or verifier
    decisionRights:
      - verify implementation evidence
      - decide closure readiness
      - identify verification gaps
  approver:
    label: Human approver
    decisionRights:
      - approve PRD, SDD, and plan gates
      - approve external projection mutations
      - approve closure
  autonomous_system:
    label: Agent executing bounded GADD skills
    decisionRights:
      - recommend routes
      - draft artifacts
      - execute bounded implementation only after approved boundary exists
      - record evidence
      - escalate when gates, scope, or evidence are insufficient

autonomyVocabulary:
  tiers:
    - assist
    - recommend
    - draft
    - execute_with_approval
    - execute_within_limits
    - autonomous_with_monitoring
  riskTiers:
    - low
    - medium
    - high
    - human_only
  gateTypes:
    - advisory
    - validating
    - blocking
    - escalating
  authorityPlanes:
    - data_plane
    - control_plane

lanes:
  intake:
    purpose: Normalize unclassified incoming work and route it safely.
    skills:
      - /gadd:triage
      - /gadd:next
    states:
      - needs_info
      - ready_for_implementation
      - needs_sdd
      - needs_prd
      - blocked_on_human_decision
      - duplicate
      - out_of_scope
      - not_gadd_work
    autonomousResponsibilities:
      - inspect source intake
      - gather repository and GitNexus evidence where code reality matters
      - recommend Work Item type and route
      - draft triage outcome
    authority:
      plane: data_plane
      autonomyTier: draft
      riskTier: medium
      allowed:
        - create or update local triage state
        - draft external projection content
      prohibited:
        - mutate external issues without human approval
        - route code-impacting work without GitNexus evidence or approved fallback
    evidence:
      input:
        - source intake
        - external issue state when provided
        - repo evidence when relevant
        - GitNexus evidence or approved fallback for code-impacting routes
      completion:
        - Work Item ledger
        - triage approved outcome when route boundary is approved
        - next command and next human action
    gates:
      - id: triage_route
        gateType: validating
        approvalRole: approver
        approvalCondition: "Route boundary is approved when downstream work depends on triage outcome."
        escalationCondition: "Information, evidence, or authority is insufficient for responsible routing."

  product_requirement:
    purpose: Establish product scope before technical design.
    skills:
      - /gadd:research
      - /gadd:scope
      - /gadd:elaborate
      - /gadd:refine
      - /gadd:approve
    autonomousResponsibilities:
      - gather sanitized product and repository evidence
      - draft and refine PRD sections
      - preserve product non-goals and unresolved questions
    authority:
      plane: data_plane
      autonomyTier: draft
      riskTier: medium
      allowed:
        - draft research and PRD artifacts
        - recommend readiness for approval
      prohibited:
        - approve product scope
        - silently add product scope during design or implementation
    evidence:
      input:
        - product trigger
        - research where required
        - repository context
      completion:
        - approved PRD
        - ledger approval event
    gates:
      - id: prd_approval
        gateType: blocking
        approvalRole: product_authority
        approvalCondition: "PRD is review-ready and explicitly approved through /gadd:approve."
        escalationCondition: "Product goals, users, acceptance criteria, non-goals, or constraints remain unresolved."

  technical_design:
    purpose: Convert approved product or engineering boundary into repo-scoped design and implementation plan.
    skills:
      - /gadd:design
      - /gadd:plan
      - /gadd:decompose
      - /gadd:approve
    autonomousResponsibilities:
      - inspect code and ADR context
      - draft SDD
      - draft implementation plan
      - decompose approved plan into child Work Items
    authority:
      plane: data_plane
      autonomyTier: draft
      riskTier: high
      allowed:
        - draft design and plan artifacts
        - recommend implementation route
      prohibited:
        - approve SDD or plan
        - change product boundary
        - make external tracker mutations without human confirmation
    evidence:
      input:
        - approved PRD or approved triage outcome
        - code and ADR context
        - GitNexus context when available and relevant
      completion:
        - approved SDD
        - approved plan when required
        - child Work Item ledgers when decomposed
    gates:
      - id: sdd_approval
        gateType: blocking
        approvalRole: technical_authority
        approvalCondition: "SDD is approved through /gadd:approve."
        escalationCondition: "Architecture, contract, data, security, privacy, or cross-repo questions remain unresolved."
      - id: plan_approval
        gateType: blocking
        approvalRole: technical_authority
        approvalCondition: "Plan is approved through /gadd:approve."
        escalationCondition: "Sequencing, review load, or slice boundaries remain unclear."

  implementation:
    purpose: Execute approved Work Item boundaries with code, tests, docs impact, and evidence.
    skills:
      - /gadd:implement
    autonomousResponsibilities:
      - implement within approved boundary
      - run tests and checks
      - record implementation evidence
      - stop when scope or authority boundary is insufficient
    authority:
      plane: data_plane
      autonomyTier: execute_with_approval
      riskTier: medium
      allowed:
        - edit repository files inside approved boundary
        - run tests and local verification commands
      prohibited:
        - bypass PRD, SDD, or plan gates
        - approve its own work for closure
        - mutate external state without explicit confirmation
    evidence:
      input:
        - ready Work Item
        - approved triage, PRD, SDD, or plan boundary
      completion:
        - code diff or pull request
        - tests and checks
        - documentation impact evidence
        - implementation ledger status
    gates:
      - id: implementation_boundary
        gateType: blocking
        approvalRole: approver
        approvalCondition: "Implementation starts only after the owning approved boundary exists."
        escalationCondition: "The implementation requires scope, design, or authority outside the approved boundary."

  review_and_closure:
    purpose: Verify implementation and apply human-approved closure.
    skills:
      - /gadd:verify
      - /gadd:close
      - /gadd:archive
    autonomousResponsibilities:
      - inspect implementation evidence
      - draft verification report
      - recommend closure readiness
      - archive already closed local packages when requested
    authority:
      plane: data_plane
      autonomyTier: draft
      riskTier: high
      allowed:
        - draft verification findings
        - update local verification artifact
        - archive closed Work Items when closure already exists
      prohibited:
        - close unverified work
        - approve its own implementation
        - claim closure without human approval
    evidence:
      input:
        - implemented Work Item
        - implementation evidence
        - approved boundaries
      completion:
        - verification.md
        - closure ledger event
        - optional archive state
    gates:
      - id: verification
        gateType: validating
        approvalRole: reviewer
        approvalCondition: "Verification evidence supports closure readiness."
        escalationCondition: "Checks, evidence, docs impact, or approved boundary are insufficient."
      - id: closure
        gateType: blocking
        approvalRole: approver
        approvalCondition: "Human approves closure after verification readiness."
        escalationCondition: "Closure would hide unresolved verification or external drift."

controlPlaneActions:
  - command: /gadd:setup
    authorityPlane: control_plane
    autonomyTier: execute_with_approval
    riskTier: high
    reason: "Bootstraps configuration, templates, Work Item directories, and projection settings."
  - command: /gadd:approve
    authorityPlane: control_plane
    autonomyTier: execute_with_approval
    riskTier: high
    reason: "Promotes governed gates and updates canonical ledger state."
  - command: /gadd:close
    authorityPlane: control_plane
    autonomyTier: execute_with_approval
    riskTier: high
    reason: "Applies workflow closure."

projections:
  externalTrackers:
    canonical: false
    examples:
      - GitHub Issues
      - GitHub Pull Requests
      - Linear
      - Jira
    rule: "Projection mutations require human confirmation and drift checks."

governedAutonomyRiskPatterns:
  chat_as_control_plane:
    mitigation: "Repo-local ledger remains canonical."
  unbounded_delegation:
    mitigation: "Each skill has input gates, rules, stop conditions, and approved boundaries."
  role_collapse:
    mitigation: "Product, design, implementation, verification, and closure are separate lanes."
  evidence_drift:
    mitigation: "PRD, SDD, plan, implementation evidence, verification report, and ledger events record evidence."
  approval_theater:
    mitigation: "/gadd:approve approves specific PRD, SDD, and plan gates."
  tool_sprawl:
    mitigation: "External trackers are projections, not canonical state."
  accountability_gaps:
    mitigation: "Human roles own product, technical, review, and closure decisions."
  scope_creep_at_machine_speed:
    mitigation: "Approved boundaries and stop conditions force boundary resets."
  post_hoc_governance:
    mitigation: "GADD introduces gates before implementation and closure."

controlMappings:
  - source: NIST AI RMF
    controlId: GOVERN
    mappingStatus: candidate
    implementationStatus: partial
    evidenceReferences:
      - docs/governed-autonomy/operating-model.md
      - skills/gadd-approve/SKILL.md
      - skills/gadd-verify/SKILL.md
  - source: ISO/IEC 42001
    controlId: Annex A
    mappingStatus: unmapped
    implementationStatus: unreviewed
    evidenceReferences: []
  - source: EU AI Act
    controlId: Article 26
    mappingStatus: unmapped
    implementationStatus: not_applicable
    evidenceReferences: []

knownGaps:
  - id: second-reference-process-missing
    summary: "GAPS has only one reference process. Schema, validator, skills, and generation are blocked until an unlike process is modeled."
  - id: formal-standards-export-not-designed
    summary: "BPMN, DMN, and OSCAL compatibility is a posture, not an implemented export contract."
  - id: field-origin-not-enforced
    summary: "Standards origin is described in standardsAlignment, not enforced field-by-field in v0.1."
  - id: regulatory-mapping-unreviewed
    summary: "Control mappings are stubs and do not claim compliance, certification, or legal sufficiency."
```

- [ ] **Step 2: Parse the YAML**

Run:

```bash
python3 - <<'PY'
import pathlib

path = pathlib.Path("gaps/examples/gadd/ga-process.yml")
text = path.read_text()
assert 'schemaVersion: "0.1"' in text
assert "id: gadd" in text
assert "knownGaps:" in text
print("GAPS reference process parsed")
PY
```

Expected: `GAPS reference process parsed`.

- [ ] **Step 3: Check v0.1 boundaries**

Run:

```bash
rg -n "certification|compliance artifact|generator|runtime target|validator|schema/" gaps/examples/gadd/ga-process.yml
```

Expected: hits, if any, only appear as negative boundaries or known gaps. No sentence claims certification, compliance, generator, runtime target, validator, or schema support.

- [ ] **Step 4: Commit the reference process**

Run:

```bash
git add gaps/examples/gadd/ga-process.yml
git commit -m "Add GADD GAPS reference process"
```

Expected: commit succeeds and includes only `gaps/examples/gadd/ga-process.yml`.

---

### Task 3: Add the top-level README pointer

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add one bullet under "More Detail"**

Modify the `## More Detail` list in `README.md` so it contains this new bullet after the Governed Autonomy docs bullet:

```markdown
- [gaps/](gaps/README.md) incubates GAPS, the Governed Autonomy Process Specification layer, with GADD as the first reference process.
```

The resulting `## More Detail` section should be:

```markdown
## More Detail

- [docs/governed-autonomy/](docs/governed-autonomy/README.md) explains the broader Governed Autonomy philosophy, operating model, uncontrolled AI risk patterns, and the GADD case study.
- [gaps/](gaps/README.md) incubates GAPS, the Governed Autonomy Process Specification layer, with GADD as the first reference process.
- [docs/workflow.md](docs/workflow.md) covers workflow state, external projections, the MVP workflow, and handoff artifact contracts.
- [docs/skills.md](docs/skills.md) catalogs the `/gadd:*` skills by lane, purpose, input, output, and usual handoff.
- [docs/package-model.md](docs/package-model.md) covers package layout and compatibility surfaces.
```

- [ ] **Step 2: Verify the README pointer is minimal**

Run:

```bash
rg -n "gaps|GAPS|Governed Autonomy Process Specification" README.md
```

Expected: one hit in the `## More Detail` section only.

- [ ] **Step 3: Commit the README pointer**

Run:

```bash
git add README.md
git commit -m "Link GAPS from README"
```

Expected: commit succeeds and includes only `README.md`.

---

### Task 4: Final verification

**Files:**
- Verify: `README.md`
- Verify: `gaps/README.md`
- Verify: `gaps/examples/gadd/ga-process.yml`
- Verify: existing validation scripts

- [ ] **Step 1: Run whitespace check**

Run:

```bash
git diff --check HEAD~3..HEAD
```

Expected: no output.

- [ ] **Step 2: Run documentation freshness validation**

Run:

```bash
python3 scripts/validate-gadd-docs.py
```

Expected:

```text
GADD documentation freshness validated
```

- [ ] **Step 3: Parse package manifest**

Run:

```bash
python3 -m json.tool agent-skills.json >/dev/null
```

Expected: no output and exit status 0.

- [ ] **Step 4: Run Level 1 workflow validation**

Run:

```bash
python3 scripts/validate-gadd-level1.py
```

Expected:

```text
GADD Level 1 workflow scenarios validated (5 scenarios)
```

- [ ] **Step 5: Re-parse the GAPS YAML**

Run:

```bash
python3 - <<'PY'
import pathlib

text = pathlib.Path("gaps/examples/gadd/ga-process.yml").read_text()
required = [
    "schemaVersion:",
    "process:",
    "canonicalState:",
    "freshness:",
    "roles:",
    "lanes:",
    "governedAutonomyRiskPatterns:",
    "controlMappings:",
    "knownGaps:",
]
missing = [key for key in required if key not in text]
assert not missing, missing
assert 'schemaVersion: "0.1"' in text
assert "GAPS is a Governed Autonomy profile" in text
print("GAPS YAML shape validated")
PY
```

Expected:

```text
GAPS YAML shape validated
```

- [ ] **Step 6: Check final status**

Run:

```bash
git status --short
```

Expected: no output.
