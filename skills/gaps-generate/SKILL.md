---
name: gaps-generate
description: Use when the user says /gaps:generate, wants to generate skills from a GAPS process spec, or asks for a GAPS ga-process.yml to produce skill package skeletons.
---

# /gaps:generate

Generate a reviewable skill-package skeleton from one GAPS process specification.

This command is a standalone, agent-agnostic GAPS command. Follow this file directly; do not require any other installed skill.

## Inputs

Run against one GAPS process file:

```text
/gaps:generate <path-to-ga-process.yml>
```

If no process file is supplied, ask for one. Do not infer the target from unrelated repo files.

## Reads

- `gaps/README.md`
- `gaps/schema/ga-process.schema.json`
- requested `ga-process.yml`
- `scripts/validate-gaps.py`
- `scripts/generate-gaps-skill-package.py`

## Writes

By default, only preview files under:

```text
gaps/generated/<process-id-slug>/
```

Adopted package output under `skills/` and `commands/` is allowed only when the user explicitly requests write/adopt mode. Review artifacts remain under `gaps/generated/<process-id-slug>/`.

If `implementation.yml` exists beside the requested process file, generation uses it to produce command-level skills and full preview manifests. Use `--no-implementation-map` only when the user explicitly wants lane-level scaffold output.

## Input Quality Gate

Before generating, run:

```bash
python3 scripts/validate-gaps.py <path-to-ga-process.yml>
```

If validation fails, do not generate. Report the validator findings.

## Rules

- Dry-run preview is the default.
- Adjacent implementation maps are used by default for command-level skill generation.
- Adopted output requires explicit user instruction and generator flags `--write --adopt-output`.
- Adopted output refuses to replace existing files unless the user explicitly requests `--overwrite`.
- Generated skills are skeletons for human review, not production-ready process controls.
- Do not claim regulatory compliance, certification, legal sufficiency, runtime execution, BPMN export, CMMN export, DMN export, or OSCAL export.
- Do not overwrite existing package files unless the user explicitly requests overwrite mode.
- Preserve known gaps and non-claims in generated artifacts.

## Workflow

1. Resolve the requested `ga-process.yml`.
2. Run `python3 scripts/validate-gaps.py <path-to-ga-process.yml>`.
3. For normal preview generation, run:

   ```bash
   python3 scripts/generate-gaps-skill-package.py <path-to-ga-process.yml>
   ```

   If the process has an adjacent `implementation.yml`, validate the generated preview map:

   ```bash
   python3 scripts/validate-gaps-implementation.py gaps/generated/<process-id-slug>/implementation.yml
   ```

   For GADD specifically, run generated-package behavior validation:

   ```bash
   python3 scripts/validate-generated-gadd-package.py
   ```

4. For explicit adopted output only, run:

   ```bash
   python3 scripts/generate-gaps-skill-package.py <path-to-ga-process.yml> --write --adopt-output
   ```

5. Report the output directory and generated artifacts. If existing files block adoption, ask whether the user wants `--overwrite`.
6. Tell the user that `/gaps:validate` is required after adopting generated files.

## Stop Conditions

Stop without generating when:

- the requested process file is missing
- GAPS validation fails
- the user asks for direct runtime execution or standards export
- the user asks for adopted output but does not explicitly authorize writing package roots
