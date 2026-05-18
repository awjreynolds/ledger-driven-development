# GAPS

GAPS is the **Governed Autonomy Process Specification** layer incubating in this repository.

GADD is the concrete software-delivery methodology. GAPS is the emerging profile for describing how a governed process preserves accountability, authority, autonomy boundaries, evidence, escalation, approval, state, projection, verification, closure, and external control mappings when autonomous systems may participate.

## Status

GAPS remains exploratory. The current incubating validation profile is built from two reference processes.

The current surface is intentionally small:

- `examples/gadd/ga-process.yml` expresses GADD as the first reference process.
- `examples/compliance-review/ga-process.yml` expresses a second, unlike casework reference process.
- `schema/ga-process.schema.json` defines the exploratory machine-readable shape.
- `../scripts/validate-gaps.py` validates reference processes against the schema and GAPS-specific semantic checks.
- This README explains the incubation model and boundaries.

There is no GAPS command suite, generator, BPMN/CMMN/DMN/OSCAL exporter, or runtime target yet.

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

## Second reference process

The second reference process is intentionally unlike GADD.

The compliance review example stresses adaptive case flow, long-running state, statutory or policy deadlines, named human identities, multiple authority levels, budget or resource gates, and event-driven escalation.

## Validation

Run:

```bash
python3 scripts/validate-gaps.py
```

The validator checks every `gaps/examples/*/ga-process.yml` file against `gaps/schema/ga-process.schema.json` and GAPS-specific semantic rules.

Validator success means the reference processes conform to this repository's current exploratory GAPS profile. It is not regulatory compliance, certification, proof of executable correctness, legal sufficiency, or a BPMN/CMMN/DMN/OSCAL export.

## Files

- `examples/gadd/ga-process.yml` - GADD as the first GAPS reference process.
- `examples/compliance-review/ga-process.yml` - Compliance review casework as the second GAPS reference process.
- `schema/ga-process.schema.json` - Exploratory schema for the GAPS process profile.
