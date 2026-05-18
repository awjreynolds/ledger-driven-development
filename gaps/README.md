# GAPS

GAPS is the **Governed Autonomy Process Specification** layer incubating in this repository.

GADD is the concrete software-delivery methodology. GAPS is the emerging profile for describing how a governed process preserves accountability, authority, autonomy boundaries, evidence, escalation, approval, state, projection, verification, closure, and external control mappings when autonomous systems may participate.

## Status

GAPS remains exploratory. The current incubating validation profile is built from two reference processes.

The current surface is intentionally small:

- `examples/gadd/ga-process.yml` expresses GADD as the first reference process.
- `examples/gadd/implementation.yml` binds that GADD process spec to the concrete GADD skill package.
- `examples/compliance-review/ga-process.yml` expresses a second, unlike casework reference process.
- `schema/ga-process.schema.json` defines the exploratory machine-readable shape.
- `schema/implementation.schema.json` defines the exploratory implementation-map shape.
- `../scripts/validate-gaps.py` validates reference processes against the schema and GAPS-specific semantic checks.
- `../scripts/validate-gaps-implementation.py` validates implementation maps against process specs and repo files.
- `/gaps:author`, `/gaps:validate`, and `/gaps:generate` provide the first GAPS authoring, validation, and skill-package generation skills.
- This README explains the incubation model and boundaries.

There is no BPMN/CMMN/DMN/OSCAL exporter or runtime target yet.

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

## GADD implementation binding

GADD is now implemented as this repository's first GAPS-described agent skill package.

The binding is explicit:

- `examples/gadd/ga-process.yml` describes the governed software-delivery process.
- `examples/gadd/implementation.yml` maps each GAPS lane, gate, command, and control-plane action to concrete GADD skills, command adapters, manifests, and validators.
- `../scripts/validate-gaps-implementation.py` checks that the implementation map still matches the process spec and package files.

This is an implementation-conformance check for the repo package. It is not a regulatory, legal, standards-export, or runtime-execution claim.

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
python3 scripts/validate-gaps-implementation.py
```

The validator checks every `gaps/examples/*/ga-process.yml` file against `gaps/schema/ga-process.schema.json` and GAPS-specific semantic rules.

The implementation validator checks `gaps/examples/gadd/implementation.yml` against `gaps/examples/gadd/ga-process.yml` and the actual GADD package files.

Validator success means the reference processes and implementation maps conform to this repository's current exploratory GAPS profile. It is not regulatory compliance, certification, proof of executable correctness, legal sufficiency, or a BPMN/CMMN/DMN/OSCAL export.

## Generation

Run:

```bash
python3 scripts/generate-gaps-skill-package.py <path-to-ga-process.yml>
```

Generation is dry-run-first. By default it writes a reviewable package skeleton under `gaps/generated/<process-id-slug>/` with skills, command adapters, manifest patch suggestions, an implementation map, and a validation checklist.

When `implementation.yml` exists beside the input `ga-process.yml`, the generator uses it to produce command-level skill skeletons that match the implementation map. For GADD, that means generated skills such as `gadd-refine`, `gadd-implement`, and `gadd-verify`, not only broad lane skills. Use `--no-implementation-map` to force the older lane-level preview mode, or `--implementation-map <path>` to supply a map explicitly.

Adopting generated files into package roots requires explicit write mode:

```bash
python3 scripts/generate-gaps-skill-package.py <path-to-ga-process.yml> --write --adopt-output
```

Adopted mode writes package files under `skills/` and `commands/`, while review artifacts stay under `gaps/generated/<process-id-slug>/`. Existing files are not replaced unless `--overwrite` is also supplied.

Generated output is a starting point for human process-owner review. It is not production-ready by default and does not claim regulatory compliance, certification, legal sufficiency, runtime execution, or standards export.

To validate the generated GADD package against the available deterministic behavior harnesses, run:

```bash
python3 scripts/validate-generated-gadd-package.py
```

This command generates a temporary GADD package, validates its generated implementation map, and runs Level 1 plus Level 2/3 scripted harnesses with `GADD_PACKAGE_ROOT` pointing at the generated package.

## Files

- `examples/gadd/ga-process.yml` - GADD as the first GAPS reference process.
- `examples/gadd/implementation.yml` - GADD implementation map for the skill package.
- `examples/compliance-review/ga-process.yml` - Compliance review casework as the second GAPS reference process.
- `schema/ga-process.schema.json` - Exploratory schema for the GAPS process profile.
- `schema/implementation.schema.json` - Exploratory schema for implementation maps.
