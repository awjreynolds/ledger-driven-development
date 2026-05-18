# GAPS specification layer design

**Date:** 2026-05-18
**Status:** ready for user review before implementation planning
**Context:** introducing Governed Autonomy Process Specification as a reusable process-specification layer, incubated in the GADD repository with GADD as the first reference process

## Thesis

GADD should introduce **GAPS: Governed Autonomy Process Specification** as the reusable specification layer behind Governed Autonomy.

GADD remains the concrete SDLC methodology and executable skill suite. GAPS is the emerging process-specification layer: a way to describe roles, authority, autonomy level, gates, evidence, escalation, approval, canonical state, projections, verification, closure, and external governance mappings for a governed process where autonomous systems may participate.

GAPS must not present itself as if business-process modeling starts here. BPMN, CMMN, DMN, OSCAL, NIST AI RMF, ISO/IEC 42001, the EU AI Act, workflow runtimes, and structured-output tooling all occupy nearby territory. The v0.1 design should therefore be deliberately small: express GADD as one GAPS reference process, then learn from the mismatch.

Where existing standards already model a concept, GAPS should use their terminology rather than re-derive it. The contribution of GAPS is the agent-governance overlay (autonomy tier, authority plane, trust decay, drift signal, Governed Autonomy risk-pattern coverage) layered on top of process and control plumbing that BPMN, CMMN, DMN, and OSCAL already supply. Authors should use a source-standard term when they know one and mark unknown cases for later review; exact value-shape parity and lossless export are v1+ directions, not v0.1 gates.

## Problem

The repository now explains Governed Autonomy as a general business-process discipline and GADD as one SDLC case study. The missing layer is a repeatable artifact that turns the philosophy into a process specification.

Without that layer:

- Governed Autonomy remains mostly prose.
- GADD looks like a one-off skill implementation rather than a reference implementation.
- New governed processes have no standard way to describe roles, authority, evidence, gates, autonomy tiers, and state.
- Skill authoring risks starting from prompt text rather than from a governed process model.
- Integrations such as Archon or BAML have no canonical source to consume or assist.

The earlier draft overreached by proposing a new YAML metamodel plus schema, docs, skills, validation, and multiple targets before the model had described more than one process. This revision narrows v0.1 to two GAPS artifacts plus a one-line README pointer, and makes prior art and regulatory anchoring explicit.

## Goals

- Add a clearly separated top-level `gaps/` area to this repository.
- Define GAPS as an incubating specification layer, not a finished standard.
- Express GADD as the first reference GAPS process.
- Require the GADD reference process to declare schema version, drift/freshness expectations, gate taxonomy, autonomy tier, authority plane, canonical state, and regulatory mapping placeholders.
- Keep GADD and GAPS conceptually distinct:
  - GADD is Governed Autonomy for SDLC.
  - GAPS is the emerging process specification layer.
- Defer schema, validator, skill suite, and generation until at least a second unlike process has been attempted.

## Non-goals

- Do not extract GAPS into a separate repository in the first pass.
- Do not replace existing GADD skills with generated skills.
- Do not make BPMN, CMMN, DMN, Archon, BAML, or any runtime/tool the canonical GAPS model.
- Do not re-derive concepts that BPMN, CMMN, DMN, or OSCAL already model. Where a GAPS field corresponds to one of those standards, use the term a reader of that standard would already recognize; if you don't know one, mark the field for later review rather than coining a fresh name. Exact value-shape parity and lossless export are deferred to v1+.
- Do not claim that GAPS can already model every business process.
- Do not add a formal JSON Schema in v0.1.
- Do not add `/gaps:*` skills in v0.1.
- Do not add compiler or generator behavior in v0.1.
- Do not add non-SDLC example processes in the first implementation slice, but do require one before schema and validator work.
- Do not rename GADD or dilute its current public positioning.

## Canonical language

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

## Prior art and explicit non-adoption

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

## Standards compatibility

GAPS uses the *concepts* of BPMN, CMMN, DMN, and OSCAL where they overlap with the v0.1 model. It does not adopt their artifact formats. BPMN's XML and graphical authoring, CMMN's case-flow modeler, DMN's decision tables, and OSCAL's JSON catalog assume tooling and audiences that GADD users do not have. GAPS keeps a git-native YAML authoring form and adds an agent-governance overlay (autonomy tier, authority plane, trust decay, drift signal, GA risk-pattern coverage) that those standards do not cover.

The genuine contribution of GAPS is the overlay. Re-derived process and control plumbing is not worth defending if a standard already does the job. To keep that distinction honest without turning v0.1 into a standards-compliance exercise:

- **Use the source-standard term when you know one.** Where a GAPS field clearly corresponds to a concept in BPMN, DMN, or OSCAL, use the term a reader of that standard would already recognize (`gateway`, `task`, `sequence flow`, `control-id`, `implementation-status`, and so on). If you don't know one and have to coin a name, mark the field in `standards_alignment` as `name_review_pending` so a later mapper pass can rename rather than re-derive. Exact value-shape parity and lossless export are v1+ concerns, not v0.1 gates. The reference process should record the alignment it knows in a top-of-file `standards_alignment` section, not require it on every field.
- **Mark the overlay at section level.** The agent-governance overlay (autonomy tier, authority plane, trust decay, drift/freshness signal, GA risk-pattern coverage) should be grouped or annotated so the GAPS-specific contribution stays distinguishable from re-derived plumbing. Section-level annotation is enough; per-field origin tags are not required in v0.1.
- **Lossless export is a v1 direction, not a v0.1 obligation.** Process structure should aim to be exportable to BPMN/DMN, and control mappings should aim to be shape-compatible with OSCAL, but v0.1 field shapes are not held to that bar yet. The goal is to avoid choices that would obviously preclude later export, not to prove export-readiness now.
- **CMMN compatibility is deferred.** CMMN matters when adaptive case flow becomes load-bearing. GADD is mostly phase/gate workflow, so CMMN alignment should be revisited when the second reference process is selected, not designed against GADD.
- **Conflict policy.** When BPMN, CMMN, DMN, OSCAL, or other standards name the same concept differently, record the alternate names in a structured `standard_aliases` block inside `standards_alignment`, not in YAML comments (which tools and exporters lose). Recurring conflicts belong in Open Design Questions.

This positioning is also why the spec rejects making BPMN, CMMN, DMN, or OSCAL the GAPS authoring format: alignment with them is the direction, adopting them as the source format is not.

## Layered architecture

GAPS should separate process meaning from runtime enforcement and audit evidence.

V0.1 should use these conceptual layers in the reference process:

| Layer | Purpose | GAPS examples |
| --- | --- | --- |
| Rules | Policy, risk appetite, role ownership, authority limits, autonomy tiers, gate definitions. | allowed actions, prohibited actions, control-plane vs data-plane authority, high-risk transition policy |
| Gating | Preconditions and transition controls. | advisory, validating, blocking, escalating gates |
| Behavior | What autonomous systems and human roles may do at runtime. | skill responsibilities, tool access, stop conditions, escalation behavior |
| Evidence | Durable trace, audit, and verification material. | ledger entries, PRD/SDD/plan/verification files, approval records, external projection hashes |

This avoids putting validation rules, projection policy, evidence requirements, and authority boundaries into one flat bucket.

## GAPS model v0.1

The v0.1 model should be expressed through `gaps/examples/gadd/ga-process.yml`, not a JSON Schema.

The reference process should have a tight required core. It is complete when it faithfully describes GADD and names any gaps, not when it populates every possible future field.

Required for v0.1:

- `schemaVersion: "0.1"`
- a breakage warning that v0.1 is exploratory and not stable
- process identity and purpose
- scope and explicit non-scope
- roles and decision rights
- autonomous-system responsibilities where GADD delegates work to agents
- authority plane for autonomous actions: `data_plane` or `control_plane`
- autonomy tier using the existing Governed Autonomy ladder
- risk tier per governed transition
- gate type: `advisory`, `validating`, `blocking`, or `escalating`
- process states and governed transitions
- required input evidence and completion evidence for governed transitions
- approval and escalation conditions as separate concepts
- canonical state and projection surfaces
- drift/freshness relationship to the GADD skills and ledger templates
- regulatory/control mapping placeholders with mapping status
- a top-of-file `standards_alignment` section recording known alignment to BPMN, DMN, or OSCAL (CMMN deferred to the second reference process), with a `standard_aliases` block for naming conflicts
- known gaps or unmodeled behavior

Fill where natural, but do not force coverage:

- full RACI ownership for every gate
- allowed/prohibited action lists
- revocation or trust-decay triggers
- detailed temporal semantics beyond approval/verification bypass prevention
- dry-run or simulation expectations
- budget or resource state
- OSCAL-shaped control metadata

The optional concepts should appear only when they describe GADD honestly. If a field does not fit GADD yet, the reference process should omit it or record a clear `not_applicable` or `unmodeled` note rather than inventing detail.

The expected vocabulary is:

- autonomy tier: `assist`, `recommend`, `draft`, `execute_with_approval`, `execute_within_limits`, `autonomous_with_monitoring`
- risk tier: `low`, `medium`, `high`, `human_only`
- gate type: `advisory`, `validating`, `blocking`, `escalating`
- mapping status: `unmapped`, `candidate`, `reviewed`

The model should prefer stable process concepts over GADD-specific nouns. GADD terms can appear in the reference process as domain vocabulary, not as generic schema assumptions.

## GADD reference process

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

## V0.1 completion criteria

V0.1 is complete when the reference process is faithful to GADD and explicit about uncertainty.

The GADD reference file should be accepted if:

- every current GADD lane and approval boundary is represented
- the core fields above are present where they apply
- missing or weak concepts are recorded as known gaps rather than hidden
- no regulatory, safety, validator, or generation support is claimed
- optional fields are used only where they describe real GADD behavior

V0.1 should not be rejected merely because optional fields are sparse. Sparse but honest is better than a heroic YAML file full of invented structure.

## GAPS vs GADD state

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

## Regulatory and control mapping

GAPS should be designed for audit usefulness, but v0.1 should not overclaim.

The GADD reference process should include placeholder mappings that show where controls would attach:

- NIST AI RMF function and subcategory references where known.
- ISO/IEC 42001 clause or Annex A references where known.
- EU AI Act deployer/operator obligations where applicable.
- `mapping_status: unmapped | candidate | reviewed`.

Mapping fields should leave room for later OSCAL-style export or crosswalks. Where a mapping is present, prefer a shape that can eventually carry control source, control identifier, parameter values, implementation status, evidence references, and mapping status.

The first implementation should not attempt complete mappings. It should prove that GAPS has a place to store them and that validation findings can later become audit-useful rather than only internally meaningful.

## Later work (non-normative)

Later work may add a GAPS skill suite, authoring/extraction tools, runtime emission, validation, assurance reports, and skill scaffolding. Candidate skills are `/gaps:assess`, `/gaps:spec`, `/gaps:validate`, and `/gaps:derive`, but their contracts are deliberately deferred until after the second reference process exists.

BAML belongs in the authoring and extraction layer: it could help turn process interviews, documents, tracker workflows, or skill contracts into candidate structured specs. Archon belongs in the runtime-emission layer: it could execute deterministic projections of selected transitions once GAPS has stronger formal semantics. Neither tool should shape v0.1 beyond leaving the reference process readable and explicit.

Future validation should start as findings-only and should check role ownership, authority plane, autonomy tier, risk tier, gate type, evidence, approval/escalation separation, temporal bypasses, state ownership, projection drift, closure, and external control mappings. The exact rule list, output format, and severity model are deferred.

## Repository shape

V0.1 should add two GAPS artifacts and one discoverability pointer:

```text
README.md                         # one-line pointer to GAPS
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

This layout makes GAPS visible to people already navigating to GADD while avoiding a premature product surface. The top-level README change should be limited to one sentence or one bullet; broader public positioning belongs in a later pass.

## Why incubate in this repository

GAPS should start in the GADD repository because:

- GADD is already public and people are navigating to it.
- GADD is the first concrete Governed Autonomy implementation.
- The existing skill contracts, ledgers, templates, tests, and docs give GAPS a real process to model.
- Incubating beside the reference implementation reduces abstraction drift.
- Extraction remains straightforward once the specification stabilizes.

The `gaps/README.md` should state that GAPS is incubating here because GADD is its first reference process and may move to a standalone repository once the specification and authoring model stabilize.

## Second reference process gate

Before adding schema, validation, generation, or GAPS skills, model one unlike process informally.

The repo owner should select the second reference process after the GADD reference file is reviewed. Selection criteria:

- unlike GADD in flow shape
- has real approval or escalation stakes
- includes long-running or event-driven state
- exercises named human identities or authority levels
- can expose whether CMMN/case semantics, regulatory mapping, budget/resource gates, or temporal constraints need to become first-class

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

## Documentation changes

V0.1 should keep public GADD positioning stable while making GAPS discoverable:

- `README.md` gets one concise pointer to `gaps/`.
- `gaps/README.md` explains GAPS and incubation status.
- `gaps/examples/gadd/ga-process.yml` is the reference artifact.
- Broader GADD docs can link to GAPS in a later pass after review.

## Migration and compatibility

No existing GADD workflow behavior should change in the first implementation.

Existing users should still install and use `/gadd:*` skills exactly as before. GAPS is additive:

- one top-level README pointer
- one new GAPS README
- one new GADD reference process spec

The GADD reference process may reveal mismatches between docs and skill behavior. Those should be captured as findings or future Work Items, not silently fixed during the first GAPS slice unless they block the reference spec.

## Extraction path

If GAPS becomes useful outside GADD, extract it later into a standalone repository.

Extraction readiness signals:

- the GADD reference process is complete and reviewed
- at least one non-SDLC process has been modeled successfully
- schema versioning and compatibility rules are stable
- GAPS docs explain authoring without assuming GADD knowledge
- validator findings have a clear output format and control-mapping strategy
- generated or derived outputs are stable enough to support users

Until then, this repository should present GAPS as incubating beside GADD.

## Open design questions

| Question | Impact | Owner | Next action |
| --- | --- | --- | --- |
| Which second unlike process should stress-test GAPS after GADD, and against what evidence? | This unlocks schema, validator, skills, and generation. Picking poorly would freeze a GADD-shaped model. | Repo owner | Decide after reviewing the GADD reference file, using the second-reference selection criteria above. |
| How formal should temporal semantics become before validation? | Determines whether GAPS can detect bypasses, deadlocks, and missing preconditions. | Repo owner | Keep v0.1 descriptive; revisit after second process. |
| Which external mapping should come first: NIST AI RMF, ISO/IEC 42001, or EU AI Act? | Determines whether GAPS optimizes for governance, management-system assurance, or legal deployer obligations. | Repo owner | Add placeholders now; choose first mapping later. |
| Should GAPS eventually export OSCAL-like control artifacts? | Could make GAPS more audit-useful, but risks pulling the project into compliance tooling too early. | Repo owner | Shape placeholders for possible OSCAL crosswalk; defer export design. |
| What should the validator output format be? | Determines whether findings integrate with GADD verification, CI, or standalone review. | Repo owner | Defer until validator design. |
| When BPMN, CMMN, DMN, and OSCAL name the same concept differently, how is alignment recorded? | Drives later mapper and export design without forcing v0.1 to pick one source as canonical. | Repo owner | Record alternate names in the `standard_aliases` block of `standards_alignment`; revisit when the second reference process or a real exporter exists. |

## Recommended first implementation slice

The first implementation should add two GAPS artifacts and one README pointer:

1. `gaps/README.md`
2. `gaps/examples/gadd/ga-process.yml`
3. one concise top-level `README.md` pointer to `gaps/`

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
- The reference process covers the v0.1 required core where applicable and records known gaps where it does not.
- A `standards_alignment` section records known mappings to BPMN, DMN, or OSCAL and uses a `standard_aliases` block for naming conflicts. Per-field origin tags are not required in v0.1.
- The reference process does not claim regulatory compliance or generated skill support.
- The top-level README change is a minimal pointer and does not obscure GADD's current install and usage path.

Automated checks:

```text
python3 scripts/validate-gadd-docs.py
python3 -m json.tool agent-skills.json >/dev/null
python3 scripts/validate-gadd-level1.py
```

## Approval gate

This design should be reviewed before implementation planning. Approval means the next step is an implementation plan for introducing only the two GAPS artifacts and one README pointer.
