# GAPS Specification Layer Design

**Date:** 2026-05-18
**Status:** ready for user review before implementation planning
**Context:** introducing Governed Autonomy Process Specification as a reusable process-specification layer, incubated in the GADD repository with GADD as the first reference process

## Thesis

GADD should introduce **GAPS: Governed Autonomy Process Specification** as the reusable specification layer behind Governed Autonomy.

GADD remains the concrete SDLC methodology and executable skill suite. GAPS is the general model for describing any governed autonomous process: roles, authority, scope, input gates, evidence, escalation, approval, canonical state, projections, verification, and closure.

The first GAPS reference process should be GADD itself, expressed as `ga-process.yml`. This keeps the model grounded in a real process that already exists in this repository. If GAPS cannot describe GADD cleanly, the model is not ready to generalize.

## Problem

The repository now explains Governed Autonomy as a general business-process discipline and GADD as one SDLC case study. The missing layer is a consumable, repeatable artifact that turns the philosophy into a process specification.

Without that layer:

- Governed Autonomy remains mostly prose.
- GADD looks like a one-off skill implementation rather than a reference implementation.
- New governed processes have no standard way to describe roles, boundaries, evidence, gates, and state.
- Skill authoring risks starting from prompt text rather than from a governed process model.
- Integrations such as Archon or BAML have no canonical source to target.

The solution should avoid making any execution target canonical. GAPS should own the process semantics. Skills, workflow engines, structured-output functions, diagrams, tests, and documentation are derived views.

## Goals

- Add a clearly separated top-level `gaps/` area to this repository.
- Define GAPS as a process specification model, not only a schema file.
- Express GADD as the first reference GAPS process.
- Keep GADD and GAPS conceptually distinct:
  - GADD is Governed Autonomy for SDLC.
  - GAPS is the reusable process specification layer.
- Make the initial GAPS artifact human-readable and reviewable before adding generation.
- Establish a path for GAPS-specific skills without committing to a large command suite immediately.
- Keep future compiler targets open: GADD-style skills, Archon workflow YAML, BAML functions, docs, validation reports, state-machine diagrams, and tests.

## Non-Goals

- Do not extract GAPS into a separate repository in the first pass.
- Do not replace existing GADD skills with generated skills.
- Do not make Archon, BAML, or any other runtime the canonical model.
- Do not build a full compiler before the GADD reference process proves the model.
- Do not claim that GAPS can already model every business process.
- Do not add non-SDLC example processes in the first implementation slice.
- Do not rename GADD or dilute its current public positioning.

## Canonical Language

**GAPS**:
Governed Autonomy Process Specification. The reusable artifact and methodology for describing a business process that includes autonomous systems while preserving accountability, authority, scope, evidence, escalation, approval, and closure.

**GAPS file**:
The canonical YAML representation of one process, usually named `ga-process.yml`.

**GAPS model**:
The conceptual model behind the file format. It defines process concepts such as roles, decision rights, authority boundaries, states, transitions, evidence, approvals, escalation, closure, and projections.

**GAPS reference process**:
A complete example process expressed as a GAPS file. GADD should be the first reference process.

**GAPS compiler target**:
Any derived output produced from a GAPS file, including documentation, skills, workflow YAML, structured-output definitions, validation reports, tests, and diagrams.

**GAPS conformance**:
Validation that a process spec or generated artifact satisfies Governed Autonomy requirements and avoids known uncontrolled-AI risk patterns.

Avoid using **GASM** publicly. If needed internally, "Governed Autonomy Specification Model" can describe the metamodel, but public-facing language should use GAPS.

## Repository Shape

Create a top-level GAPS area:

```text
gaps/
  README.md
  schema/
    ga-process.schema.json
  examples/
    gadd/
      ga-process.yml
  docs/
    specification.md
    authoring-model.md
    validation-rules.md
    compiler-targets.md
```

Add GAPS skills and commands only when the implementation slice includes executable authoring support:

```text
skills/
  gaps-spec/
  gaps-validate/

commands/
  gaps/
    spec.md
    spec.toml
    validate.md
    validate.toml
```

Future skills can be added after the reference spec stabilizes:

```text
skills/
  gaps-assess/
  gaps-derive/
```

This layout makes GAPS visible to people already navigating to GADD while keeping it separate enough to extract later into a standalone repository.

## Why Incubate In This Repository

GAPS should start in the GADD repository because:

- GADD is already public and people are navigating to it.
- GADD is the first concrete Governed Autonomy implementation.
- The existing skill contracts, ledgers, templates, tests, and docs give GAPS a real process to model.
- Incubating beside the reference implementation reduces abstraction drift.
- Extraction remains straightforward once the specification stabilizes.

The `gaps/README.md` should state that GAPS is incubating here because GADD is its first reference process and may move to a standalone repository once the specification and authoring model stabilize.

## GAPS Model V0.1

The v0.1 model should describe enough of GADD to prove the abstraction:

- process identity and purpose
- scope and explicit non-scope
- roles and decision rights
- autonomous-system responsibilities
- authority boundaries
- input quality gates
- process states
- governed transitions
- required evidence per transition
- escalation conditions
- approval conditions
- closure conditions
- canonical state
- projection surfaces
- risk patterns and mitigations
- validation rules
- compiler targets

The model should prefer stable process concepts over GADD-specific nouns. GADD terms can appear in the reference process as domain vocabulary, not in the generic schema unless the concept is genuinely reusable.

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

The file should not try to generate existing skills in v0.1. It should be a faithful, reviewable specification of what already exists or is intentionally being designed.

## GAPS Skill Suite

GAPS should have its own skills, but the initial suite should stay small.

### V1 Skills

`/gaps:spec`:
Author or update a GAPS file from an existing process description, docs, or known process implementation. In this repository, its first use is creating and maintaining `gaps/examples/gadd/ga-process.yml`.

`/gaps:validate`:
Check a GAPS file for missing or weak governance boundaries: unclear role ownership, unbounded authority, missing input gates, missing evidence, approval theater, role collapse, weak closure, unclear canonical state, unmanaged projections, and unsupported compiler targets.

### Later Skills

`/gaps:assess`:
Turn an as-is process description into a Governed Autonomy assessment. This maps current roles, handoffs, decision rights, evidence, failure modes, autonomy levels, and gaps before producing a target process spec.

`/gaps:derive`:
Produce derived artifacts from a validated GAPS file: process docs, role matrix, evidence checklists, state-machine diagrams, validation scenarios, skill scaffolds, Archon workflow YAML, or BAML functions.

Do not add `/gaps:compile` in the first implementation. "Compile" implies a stronger generator contract than the model will have initially.

## Skill Authoring Relationship

GAPS should make skill authoring process-first.

The authoring path should be:

1. Describe the process in GAPS.
2. Validate role, authority, evidence, escalation, approval, state, and closure boundaries.
3. Decide which process transitions need agent skills.
4. Derive or scaffold skill contracts from the governed transition definitions.
5. Add deterministic tests and examples for the generated or manually completed skills.

This keeps skill text subordinate to process design. It prevents a skill from silently becoming the source of truth for authority, evidence, or approval rules.

## Compiler Targets

GAPS should treat all targets as derived outputs.

### Human Documentation

Generate or maintain readable process documentation:

- process overview
- role and decision-rights matrix
- state-machine summary
- evidence checklist
- escalation and approval map
- projection policy

### GADD-Style Skills

Derive command skill scaffolds:

- `SKILL.md` frontmatter
- input contract
- read/write contract
- input quality gate
- exit gate
- rules
- stop conditions
- validation behavior
- command adapter metadata

In v0.1, scaffolding may be descriptive only. Existing GADD skills remain manually authored.

### Archon Workflow YAML

Archon is a plausible execution target because it models deterministic AI coding workflows as YAML with phases, gates, artifacts, validation, worktrees, and approval. GAPS should be able to emit or inform Archon workflows later, but Archon should not define GAPS semantics.

### BAML Functions

BAML is a plausible structured-output and prompt-engineering target. GAPS can use BAML later for:

- extracting process facts from interviews or documents
- normalizing process descriptions into typed structures
- validating structured intake
- producing conformance findings with typed output

BAML should not be required for reading or authoring a GAPS file.

### Tests And Conformance

Generate validation scenarios that check:

- transition preconditions
- required evidence
- approval gates
- stop conditions
- projection drift handling
- role separation
- closure conditions

These should eventually mirror GADD's existing Level 1, Level 2, and Level 3 validation philosophy.

## Validation Rules

The first validation rules should catch the Governed Autonomy risk patterns already documented in `docs/governed-autonomy/uncontrolled-ai-risk-patterns.md`.

Required checks:

- every process has a named process owner
- every governed step has an accountable human role
- every autonomous action has explicit allowed and prohibited actions
- every state transition has required input and completion evidence
- approval transitions identify who approves and what artifact they approve
- escalation conditions are separate from approval conditions
- canonical state is defined
- projection surfaces are declared as non-canonical unless explicitly justified
- closure has a verification condition and an acceptance condition
- no role both performs and independently approves the same governed transition without a documented exception
- high-risk transitions require stronger evidence, approval, and rollback or correction notes

The validator should start as a conservative linter over a known schema. It should report gaps clearly without pretending to prove that a process is safe.

## Documentation Changes

Update public docs to introduce GAPS without distracting from GADD:

- `README.md`: add a short section after the Governed Autonomy/GADD introduction explaining that GAPS is the emerging specification layer and GADD is its first reference process.
- `docs/governed-autonomy/README.md`: link to `gaps/` as the specification path for applying Governed Autonomy repeatably.
- `docs/governed-autonomy/case-study-gadd.md`: note that GADD is being expressed as a GAPS reference process.
- `docs/skills.md`: add GAPS skills only if the implementation creates them.

Keep the main README concise. GADD should remain easy to understand as the practical SDLC solution.

## Migration And Compatibility

No existing GADD workflow behavior should change in the first implementation.

Existing users should still install and use `/gadd:*` skills exactly as before. GAPS is additive:

- new docs
- new schema
- new example spec
- optional new `/gaps:*` skills if included in the implementation slice

The GADD reference process may reveal mismatches between docs and skill behavior. Those should be captured as validation findings or future Work Items, not silently fixed during the first GAPS slice unless they block the reference spec.

## Extraction Path

If GAPS becomes useful outside GADD, extract it later into a standalone repository.

Extraction readiness signals:

- the GADD reference process is complete and validated
- at least one non-SDLC process has been modeled successfully
- the schema has versioning and compatibility rules
- GAPS docs explain authoring without assuming GADD knowledge
- generated or derived outputs are stable enough to support users

Until then, this repository should present GAPS as incubating beside GADD.

## Open Design Questions

| Question | Impact | Owner | Next action |
| --- | --- | --- | --- |
| Should v0.1 include JSON Schema in the first implementation or start with prose plus YAML example? | JSON Schema improves tooling but may freeze the model too early. | Repo owner | Decide during implementation planning. |
| Should `/gaps:spec` and `/gaps:validate` ship in the first implementation slice? | Skills make the model executable, but docs plus example may be enough for v0.1. | Repo owner | Decide during implementation planning. |
| How strict should conformance be against existing GADD skill behavior? | Strict validation may expose existing inconsistencies; loose validation may weaken GAPS. | Repo owner | Start with findings-only validation unless a mismatch invalidates the reference process. |
| Should generated skill scaffolds target only Codex-style skills first? | Narrow target is easier, but GAPS should remain tool-agnostic. | Repo owner | Keep v0.1 target descriptions tool-aware but non-binding. |

## Recommended First Implementation Slice

The first implementation should be documentation and reference-spec heavy:

1. Add `gaps/README.md`.
2. Add `gaps/docs/specification.md`.
3. Add `gaps/docs/authoring-model.md`.
4. Add `gaps/docs/validation-rules.md`.
5. Add `gaps/docs/compiler-targets.md`.
6. Add `gaps/examples/gadd/ga-process.yml`.
7. Optionally add `gaps/schema/ga-process.schema.json` if the model feels stable enough during implementation.
8. Update top-level and Governed Autonomy docs with concise GAPS links.

GAPS skills should be a second slice unless the user explicitly wants executable commands immediately.

## Verification

Manual review:

- `gaps/README.md` clearly explains GAPS, GADD, and incubation status.
- `gaps/examples/gadd/ga-process.yml` maps every current GADD lane and gate without unexplained gaps.
- GAPS docs do not claim generated skills exist before they do.
- README changes do not obscure GADD's current install and usage path.

Automated checks:

```text
python3 scripts/validate-gadd-docs.py
python3 -m json.tool agent-skills.json >/dev/null
python3 scripts/validate-gadd-level1.py
```

If JSON Schema is added:

```text
python3 -m json.tool gaps/schema/ga-process.schema.json >/dev/null
```

If GAPS skills are added:

```text
python3 scripts/validate-gadd-mvp.sh
```

## Approval Gate

This design should be reviewed before implementation planning. Approval means the next step is an implementation plan for introducing the `gaps/` area and hand-authoring GADD as the first GAPS reference process.
