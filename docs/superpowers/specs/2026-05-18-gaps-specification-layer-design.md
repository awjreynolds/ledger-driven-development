# GAPS Specification Layer Design

**Date:** 2026-05-18
**Status:** ready for user review before implementation planning
**Context:** introducing Governed Autonomy Process Specification as a reusable process-specification layer, incubated in the GADD repository with GADD as the first reference process

## Thesis

GADD should introduce **GAPS: Governed Autonomy Process Specification** as the reusable specification layer behind Governed Autonomy.

GADD remains the concrete SDLC methodology and executable skill suite. GAPS is the emerging process-specification layer: a way to describe roles, authority, autonomy level, gates, evidence, escalation, approval, canonical state, projections, verification, closure, and external governance mappings for a process that includes autonomous systems.

GAPS must not present itself as if business-process modeling starts here. BPMN, CMMN, DMN, OSCAL, NIST AI RMF, ISO/IEC 42001, the EU AI Act, workflow runtimes, and structured-output tooling all occupy nearby territory. The v0.1 design should therefore be deliberately small: express GADD as one GAPS reference process, then learn from the mismatch.

## Problem

The repository now explains Governed Autonomy as a general business-process discipline and GADD as one SDLC case study. The missing layer is a repeatable artifact that turns the philosophy into a process specification.

Without that layer:

- Governed Autonomy remains mostly prose.
- GADD looks like a one-off skill implementation rather than a reference implementation.
- New governed processes have no standard way to describe roles, authority, evidence, gates, autonomy tiers, and state.
- Skill authoring risks starting from prompt text rather than from a governed process model.
- Integrations such as Archon or BAML have no canonical source to consume or assist.

The earlier draft overreached by proposing a new YAML metamodel plus schema, docs, skills, validation, and multiple targets before the model had described more than one process. This revision narrows v0.1 to two artifacts and makes prior art and regulatory anchoring explicit.

## Goals

- Add a clearly separated top-level `gaps/` area to this repository.
- Define GAPS as an incubating specification layer, not a finished standard.
- Express GADD as the first reference GAPS process.
- Require the GADD reference process to declare schema version, drift/freshness expectations, gate taxonomy, autonomy tier, authority plane, canonical state, and regulatory mapping placeholders.
- Keep GADD and GAPS conceptually distinct:
  - GADD is Governed Autonomy for SDLC.
  - GAPS is the emerging process specification layer.
- Defer schema, validator, skill suite, and generation until at least a second unlike process has been attempted.

## Non-Goals

- Do not extract GAPS into a separate repository in the first pass.
- Do not replace existing GADD skills with generated skills.
- Do not make BPMN, CMMN, DMN, Archon, BAML, or any runtime/tool the canonical GAPS model.
- Do not claim that GAPS can already model every business process.
- Do not add a formal JSON Schema in v0.1.
- Do not add `/gaps:*` skills in v0.1.
- Do not add compiler or generator behavior in v0.1.
- Do not add non-SDLC example processes in the first implementation slice, but do require one before schema and validator work.
- Do not rename GADD or dilute its current public positioning.

## Canonical Language

**GAPS**:
Governed Autonomy Process Specification. The reusable artifact and methodology for describing a business process that includes autonomous systems while preserving accountability, authority, scope, evidence, escalation, approval, and closure.

**GAPS file**:
The canonical YAML representation of one process, usually named `ga-process.yml`.

**GAPS model**:
The conceptual model behind the file format. In v0.1 this model is exploratory and expressed through the GADD reference process, not frozen as a formal schema.

**GAPS reference process**:
A complete example process expressed as a GAPS file. GADD should be the first reference process. A second unlike reference process is required before schema, validation, or generation is promoted.

**GAPS conformance**:
In v0.1, conformance means "the process spec explicitly covers the Governed Autonomy control questions and declares any gaps." It does not mean legal compliance, safety certification, or complete process correctness. Later conformance should split into:

- schema conformance
- Governed Autonomy risk-pattern coverage
- external framework mapping coverage
- implementation drift/freshness coverage

Avoid using **GASM** publicly. If needed internally, "Governed Autonomy Specification Model" can describe the metamodel, but public-facing language should use GAPS.

## Prior Art And Explicit Non-Adoption

GAPS should acknowledge the existing landscape instead of silently re-deriving it.

| Prior art | GAPS relationship | Rationale |
| --- | --- | --- |
| BPMN | Influenced by; not adopted as the v0.1 authoring format. | BPMN is the mature notation for modeled business processes and is actively being extended for agentic orchestration. GAPS should learn from its temporal and gate semantics, but BPMN-first authoring would add notation/tooling weight before the GA-specific control model is proven. |
| CMMN | Influenced by; not adopted in v0.1. | CMMN is relevant for adaptive, event-driven, case-style work that BPMN models awkwardly. GADD is mostly phase/gate workflow, so CMMN should inform the second unlike reference process rather than shape the first file prematurely. |
| DMN | Influenced by; not adopted in v0.1. | DMN already models decision/rule layers. GAPS should not invent a rules language; it should leave room to map gate conditions and policy decisions to DMN later. |
| OSCAL | Influenced by; not adopted in v0.1. | OSCAL is the strongest model for machine-readable control catalogs and assessment artifacts. It does not currently provide a ready-made AI RMF / ISO 42001 / EU AI Act process-spec layer, but GAPS should be designed so later control mappings can be exported or crosswalked. |
| NIST AI RMF | Regulatory/governance anchor. | GAPS validation findings should eventually map to NIST AI RMF functions and subcategories, especially Govern, Map, Measure, and Manage. |
| ISO/IEC 42001 | Regulatory/governance anchor. | ISO/IEC 42001 provides an AI management-system frame and Annex A controls. GAPS should support mapping process controls toward an AIMS Statement of Applicability, but v0.1 should not claim certification support. |
| EU AI Act | Regulatory anchor where applicable. | GAPS should be able to identify deployer/operator obligations and human-oversight/logging evidence needs for high-risk use cases, but v0.1 GADD is not an EU AI Act compliance artifact. |
| LangGraph | Influenced by as an execution/runtime graph pattern, not adopted. | Useful for agent flow implementation, but it is not the governance source of truth. |
| Archon | Candidate execution target. | Archon can execute deterministic workflow projections. It belongs in the runtime-emission layer, not the authoring/extraction layer. |
| BAML | Candidate authoring and extraction tool. | BAML can help extract structured candidate specs from interviews, docs, or prompts. It is not parallel to Archon and should not be treated as a runtime target. |

Useful source anchors for the implementation notes include OMG BPMN/CMMN/DMN material, Camunda agentic BPMN writing, Flowable BPMN/CMMN/DMN AI writing, NIST AI RMF and its ISO/IEC 42001 crosswalk, ISO/IEC 42001, the EU AI Act Article 26 deployer obligations, Oracle runtime governance layers, Microsoft agent governance guidance, Archon, and BAML.

## Layered Architecture

GAPS should separate process meaning from runtime enforcement and audit evidence.

V0.1 should use these conceptual layers in the reference process:

| Layer | Purpose | GAPS examples |
| --- | --- | --- |
| Rules | Policy, risk appetite, role ownership, authority limits, autonomy tiers, gate definitions. | allowed actions, prohibited actions, control-plane vs data-plane authority, high-risk transition policy |
| Gating | Preconditions and transition controls. | advisory, validating, blocking, escalating gates |
| Behavior | What autonomous systems and human roles may do at runtime. | skill responsibilities, tool access, stop conditions, escalation behavior |
| Evidence | Durable trace, audit, and verification material. | ledger entries, PRD/SDD/plan/verification files, approval records, external projection hashes |

This avoids putting validation rules, projection policy, evidence requirements, and authority boundaries into one flat bucket.

## GAPS Model V0.1

The v0.1 model should be expressed through `gaps/examples/gadd/ga-process.yml`, not a JSON Schema.

The file should include:

- `schemaVersion: "0.1"`
- a breakage warning that v0.1 is exploratory and not stable
- process identity and purpose
- scope and explicit non-scope
- roles, named role classes, and decision rights
- RACI-style gate ownership where a gate has accountable, responsible, consulted, and informed roles
- autonomous-system responsibilities
- authority boundaries split by:
  - `authority_plane: data_plane | control_plane`
  - allowed actions
  - prohibited actions
  - escalation triggers
  - revocation or trust-decay triggers where known
- autonomy tier using the existing Governed Autonomy ladder:
  - `assist`
  - `recommend`
  - `draft`
  - `execute_with_approval`
  - `execute_within_limits`
  - `autonomous_with_monitoring`
- risk tier per transition:
  - `low`
  - `medium`
  - `high`
  - `human_only`
- gate taxonomy:
  - `advisory`
  - `validating`
  - `blocking`
  - `escalating`
- process states and governed transitions
- temporal semantics:
  - must-precede
  - must-follow
  - must-happen-within where applicable
  - deadlock or bypass notes where known
- required input evidence and completion evidence per transition
- approval record requirements:
  - identity
  - timestamp
  - approved artifact
  - prior gate outcomes
  - budget/resource state where applicable
- escalation conditions separate from approval conditions
- dry-run or simulation expectations where a transition can be exercised without business side effects
- closure conditions
- canonical state
- projection surfaces and drift rules
- implementation freshness checks
- risk patterns and mitigations
- regulatory/control mapping placeholders:
  - NIST AI RMF
  - ISO/IEC 42001
  - EU AI Act where applicable

The model should prefer stable process concepts over GADD-specific nouns. GADD terms can appear in the reference process as domain vocabulary, not as generic schema assumptions.

## GADD Reference Process

The first `gaps/examples/gadd/ga-process.yml` should describe GADD end to end:

- intake and triage
- Product Requirement lane
- Technical Design lane
- Software Engineering lane
- Engineering Review lane
- closure and optional archive
- repo-local ledger as canonical state
- external trackers as projection surfaces
- Work Items as the canonical unit of governed SDLC work
- PRD, SDD, plan, child Work Item, implementation evidence, verification, and closure gates
- `/gadd:approve` as explicit approval for PRD, SDD, and plan transitions
- `/gadd:verify` and `/gadd:close` as review and closure boundaries
- `/gadd:setup` and other configuration-changing commands as control-plane authority
- `/gadd:implement` as data-plane authority inside an approved boundary

The file should not try to generate existing skills in v0.1. It should be a faithful, reviewable specification of what already exists or is intentionally being designed.

## GAPS Vs GADD State

`ga-process.yml` and `ledger.yml` must not become competing state stores.

- `ga-process.yml` describes the process type: roles, allowed transitions, gates, evidence requirements, and projections.
- `ledger.yml` records one Work Item's current execution state inside that process.

The GADD reference process should declare this relationship explicitly and include a freshness signal:

- which GADD skill files implement the process
- which ledger templates instantiate process state
- last reviewed date
- known mismatches or unmodeled behavior
- drift policy when the skill implementation changes before the GAPS process file

If the GAPS reference process and GADD skill behavior disagree, the implementation plan should record a finding rather than silently treating either artifact as correct.

## Regulatory And Control Mapping

GAPS should be designed for audit usefulness, but v0.1 should not overclaim.

The GADD reference process should include placeholder mappings that show where controls would attach:

- NIST AI RMF function and subcategory references where known.
- ISO/IEC 42001 clause or Annex A references where known.
- EU AI Act deployer/operator obligations where applicable.
- `mapping_status: unmapped | candidate | reviewed`.

The first implementation should not attempt complete mappings. It should prove that GAPS has a place to store them and that validation findings can later become audit-useful rather than only internally meaningful.

## Future Skill Suite

GAPS should eventually have its own skills, but not in v0.1.

Candidate future skills:

`/gaps:assess`:
Turn an as-is process description into a Governed Autonomy assessment. This maps current roles, handoffs, decision rights, evidence, failure modes, autonomy levels, and gaps before producing a target process spec.

`/gaps:spec`:
Author or update a GAPS file from an existing process description, docs, or known process implementation. BAML could assist this step by extracting structured candidate spec fields from interviews or documents.

`/gaps:validate`:
Check a GAPS file for missing or weak governance boundaries, risk-pattern exposure, missing external mappings, drift/freshness gaps, temporal issues, and weak gate ownership. The validator should start as findings-only.

`/gaps:derive`:
Produce derived artifacts from a validated GAPS file: process docs, role matrix, evidence checklists, state-machine diagrams, validation scenarios, skill scaffolds, Archon workflow YAML, or BAML extraction functions.

Do not add `/gaps:compile` until generation semantics are real enough to support.

## Future Tool Roles

GAPS should treat tools as different layers, not one list of equal compiler targets.

### Authoring And Extraction

BAML can assist `/gaps:spec` by extracting structured candidate fields from:

- process interviews
- existing documentation
- skill contracts
- tracker workflows
- approval policies

BAML should not be required for reading or authoring a GAPS file.

### Runtime Emission

Archon can be a candidate runtime-emission target once a process has enough formal transition semantics. GAPS would describe the process; Archon would execute a deterministic projection of selected transitions.

### Documentation And Assurance

Future derived outputs may include:

- process overview
- role and decision-rights matrix
- state-machine summary
- evidence checklist
- escalation and approval map
- projection policy
- NIST / ISO / EU AI Act mapping report

### Skill Scaffolding

Future derived skill scaffolds may include:

- `SKILL.md` frontmatter
- input contract
- read/write contract
- input quality gate
- exit gate
- rules
- stop conditions
- validation behavior
- command adapter metadata

Existing GADD skills remain manually authored until generation earns trust.

## Future Validation Rules

The first validator should not ship in v0.1, but the reference process should be structured so these checks become possible:

- every process has a named process owner
- every governed step has an accountable human role
- every autonomous action declares data-plane or control-plane authority
- every autonomous action has explicit allowed and prohibited actions
- every transition declares autonomy tier and risk tier
- every gate declares `gate_type`
- every gate has RACI ownership
- blocking and escalating gates cannot be satisfied by the same actor that performed the governed action unless an exception is declared
- every state transition has required input and completion evidence
- approval transitions identify who approves, what artifact they approve, and what record must be kept
- escalation conditions are separate from approval conditions
- temporal preconditions prevent bypassing approval or verification
- dry-run expectations are defined for transitions that can be simulated
- canonical state is defined
- projection surfaces are declared as non-canonical unless explicitly justified
- drift/freshness policy is declared for generated or manually implemented artifacts
- closure has a verification condition and an acceptance condition
- high-risk transitions require stronger evidence, approval, and rollback or correction notes
- findings can map to NIST AI RMF, ISO/IEC 42001, or EU AI Act references where applicable

The validator should report findings clearly without pretending to prove that a process is safe or compliant.

## Repository Shape

V0.1 should add only:

```text
gaps/
  README.md
  examples/
    gadd/
      ga-process.yml
```

Do not add these until after the GADD reference process and at least one unlike second process have been attempted:

```text
gaps/schema/
gaps/docs/
skills/gaps-*/
commands/gaps/
```

This layout makes GAPS visible to people already navigating to GADD while avoiding a premature product surface.

## Why Incubate In This Repository

GAPS should start in the GADD repository because:

- GADD is already public and people are navigating to it.
- GADD is the first concrete Governed Autonomy implementation.
- The existing skill contracts, ledgers, templates, tests, and docs give GAPS a real process to model.
- Incubating beside the reference implementation reduces abstraction drift.
- Extraction remains straightforward once the specification stabilizes.

The `gaps/README.md` should state that GAPS is incubating here because GADD is its first reference process and may move to a standalone repository once the specification and authoring model stabilize.

## Second Reference Process Requirement

Before adding schema, validation, generation, or GAPS skills, model one unlike process informally.

Good candidates:

- compliance review
- service-request case handling
- procurement approval
- incident response
- public-sector casework

The second process should stress what GADD does not:

- adaptive case flow
- long-running state
- external statutory deadlines
- named human identities
- multiple authority levels
- budget/resource gates
- event-driven escalation

This is the rule-of-three discipline applied early. GADD can justify v0.1. It cannot justify a general schema alone.

## Documentation Changes

In v0.1, do not update the top-level README beyond a minimal link unless the implementation owner explicitly wants public positioning changed.

The first implementation should keep public GADD positioning stable:

- `gaps/README.md` explains GAPS and incubation status.
- `gaps/examples/gadd/ga-process.yml` is the reference artifact.
- Main GADD docs can link to GAPS in a later pass after review.

## Migration And Compatibility

No existing GADD workflow behavior should change in the first implementation.

Existing users should still install and use `/gadd:*` skills exactly as before. GAPS is additive:

- one new GAPS README
- one new GADD reference process spec

The GADD reference process may reveal mismatches between docs and skill behavior. Those should be captured as findings or future Work Items, not silently fixed during the first GAPS slice unless they block the reference spec.

## Extraction Path

If GAPS becomes useful outside GADD, extract it later into a standalone repository.

Extraction readiness signals:

- the GADD reference process is complete and reviewed
- at least one non-SDLC process has been modeled successfully
- schema versioning and compatibility rules are stable
- GAPS docs explain authoring without assuming GADD knowledge
- validator findings have a clear output format and control-mapping strategy
- generated or derived outputs are stable enough to support users

Until then, this repository should present GAPS as incubating beside GADD.

## Open Design Questions

| Question | Impact | Owner | Next action |
| --- | --- | --- | --- |
| Which second unlike process should stress-test GAPS after GADD? | Determines whether CMMN/case semantics or regulatory mapping becomes the next pressure point. | Repo owner | Pick after the GADD reference file exists. |
| How formal should temporal semantics become before validation? | Determines whether GAPS can detect bypasses, deadlocks, and missing preconditions. | Repo owner | Keep v0.1 descriptive; revisit after second process. |
| Which external mapping should come first: NIST AI RMF, ISO/IEC 42001, or EU AI Act? | Determines whether GAPS optimizes for governance, management-system assurance, or legal deployer obligations. | Repo owner | Add placeholders now; choose first mapping later. |
| Should GAPS eventually export OSCAL-like control artifacts? | Could make GAPS more audit-useful, but risks pulling the project into compliance tooling too early. | Repo owner | Revisit after control mappings are reviewed. |
| What should the validator output format be? | Determines whether findings integrate with GADD verification, CI, or standalone review. | Repo owner | Defer until validator design. |

## Recommended First Implementation Slice

The first implementation should add exactly two artifacts:

1. `gaps/README.md`
2. `gaps/examples/gadd/ga-process.yml`

The reference process should include `schemaVersion: "0.1"` and an explicit warning that the format is exploratory and expected to break.

Do not add:

- JSON Schema
- GAPS docs directory
- GAPS skills
- GAPS commands
- validator
- generator
- runtime emission target

## Verification

Manual review:

- `gaps/README.md` clearly explains GAPS, GADD, incubation status, prior art posture, and v0.1 limits.
- `gaps/examples/gadd/ga-process.yml` maps every current GADD lane and gate without unexplained gaps.
- The reference process declares gate type, autonomy tier, authority plane, canonical state, drift policy, and mapping placeholders.
- The reference process does not claim regulatory compliance or generated skill support.
- README changes do not obscure GADD's current install and usage path. In v0.1, avoid top-level README changes unless explicitly approved.

Automated checks:

```text
python3 scripts/validate-gadd-docs.py
python3 -m json.tool agent-skills.json >/dev/null
python3 scripts/validate-gadd-level1.py
```

## Approval Gate

This design should be reviewed before implementation planning. Approval means the next step is an implementation plan for introducing only the `gaps/README.md` and hand-authored GADD reference process file.
