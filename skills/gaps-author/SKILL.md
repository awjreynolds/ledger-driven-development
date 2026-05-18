---
name: gaps-author
description: Use when the user says /gaps:author, wants to write or revise a GAPS process specification, or asks to express an existing governed process as a GAPS ga-process.yml file.
---

# /gaps:author

Author or revise one GAPS process specification.

This command is a standalone, agent-agnostic GAPS command. Follow this file directly; do not require any other installed skill.

## Inputs

Run against a named process, existing process notes, or an existing GAPS example:

```text
/gaps:author <process-id or source>
```

If no process or source is provided, ask for the governed process to model. Do not invent an organization-specific process from generic assumptions.

## Reads

- `gaps/README.md`
- `gaps/schema/ga-process.schema.json`
- existing `gaps/examples/*/ga-process.yml`
- supplied process notes, docs, policy text, workflows, or implementation artifacts
- `gaps/examples/gadd/implementation.yml` when revising GADD's implemented profile

## Writes

- `gaps/examples/<process-id>/ga-process.yml`
- known gaps inside that process file

Do not write implementation maps, skills, command adapters, runtime code, external trackers, or regulatory submissions from this command.

## Input Quality Gate

Required input standard before writing:

- a process name or id
- process scope, including includes and excludes
- at least one accountable human role
- at least one state or lane
- at least one authority boundary, approval gate, escalation condition, or evidence requirement
- explicit uncertainty list when source material is incomplete

If source material is not enough to model the process responsibly, write nothing and ask the smallest clarifying question.

## Rules

- GAPS describes governed processes. It does not replace BPMN, CMMN, DMN, OSCAL, or local policy.
- Preserve the standards posture and explicit non-adoption rationale.
- Keep `schemaVersion: "0.1"` until the schema changes.
- Include `formatWarning` and `knownGaps`.
- Use `standards_alignment`, not `standardsAlignment`.
- Prefer sparse but honest fields over invented completeness.
- Do not claim regulatory compliance, certification, legal sufficiency, executable correctness, BPMN export, CMMN export, DMN export, OSCAL export, runtime support, or validator proof beyond what exists.
- Separate process specification from implementation binding. A `ga-process.yml` describes the process type; an `implementation.yml` binds that process to concrete files.
- Map existing standards where they own the concept: BPMN for structured flow, CMMN for adaptive casework, DMN for decisions, OSCAL-style fields for controls and evidence references.

## Workflow

1. Identify the process id and source material.
2. Read `gaps/README.md`, the process schema, and the closest existing example.
3. Extract scope, roles, lanes, states, authority, evidence, gates, projections, risk patterns, control mappings, freshness, and known gaps.
4. Decide whether the process is structured, adaptive, decision-heavy, or control-heavy, and reflect that in `standards_alignment`.
5. Write or update `gaps/examples/<process-id>/ga-process.yml`.
6. Run `python3 scripts/validate-gaps.py gaps/examples/<process-id>/ga-process.yml`.
7. Report validation status, known gaps, and whether an implementation map is still needed.

## Stop Conditions

Stop without writing when:

- the user asks for legal, regulatory, or certification conclusions
- the source process has no accountable human owner
- the requested output is a runtime workflow rather than a GAPS process spec
- authoring would require inventing facts that should be owned by a human process owner
