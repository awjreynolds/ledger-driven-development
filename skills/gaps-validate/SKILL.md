---
name: gaps-validate
description: Use when the user says /gaps:validate, wants to validate GAPS process specs, validate GAPS implementation maps, or check that GADD is implemented through GAPS.
---

# /gaps:validate

Validate GAPS process specifications and implementation maps.

This command is a standalone, agent-agnostic GAPS command. Follow this file directly; do not require any other installed skill.

## Inputs

Run with no arguments for the repository default:

```text
/gaps:validate
```

Optional arguments may name a specific `ga-process.yml` or `implementation.yml` file.

## Reads

- `gaps/README.md`
- `gaps/schema/ga-process.schema.json`
- `gaps/schema/implementation.schema.json`
- `gaps/examples/*/ga-process.yml`
- `gaps/examples/*/implementation.yml`
- `agent-skills.json`
- adapter manifests
- mapped skill and command files

## Writes

None. This command is read-only.

## Input Quality Gate

Required input standard:

- repository contains `scripts/validate-gaps.py`
- repository contains `scripts/validate-gaps-implementation.py`
- requested paths, when provided, exist

If a requested path is missing, write nothing and report the missing path.

## Rules

- Run validation commands; do not validate by inspection alone.
- GAPS validation is a conformance check for this repository's exploratory profile.
- Implementation validation checks that a GAPS process is bound to concrete repo files.
- Do not claim regulatory compliance, certification, legal sufficiency, executable correctness, BPMN export, CMMN export, DMN export, OSCAL export, or runtime support.
- Keep process-spec validation separate from implementation-map validation.

## Workflow

1. If no arguments are supplied, run:

   ```bash
   python3 scripts/validate-gaps.py
   python3 scripts/validate-gaps-implementation.py
   ```

2. If a `ga-process.yml` path is supplied, run:

   ```bash
   python3 scripts/validate-gaps.py <path>
   ```

3. If an `implementation.yml` path is supplied, run:

   ```bash
   python3 scripts/validate-gaps-implementation.py <path>
   ```

4. Report pass or fail with the exact failing command and the validator's findings.
5. When both commands pass for GADD, state that GADD is implemented as this repository's GAPS-described agent skill package.

## Stop Conditions

Stop and report the blocker when:

- either validator script is missing
- Ruby is unavailable for YAML parsing
- a requested path does not exist
- validation fails
