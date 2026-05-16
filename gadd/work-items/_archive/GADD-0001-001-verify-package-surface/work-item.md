# Add /gadd:verify package surface

## Parent

GADD-0001 - Add GADD execution context and verification gate

## What to build

Add the installable `/gadd:verify` command surface across the agent-skill package without changing existing command behavior yet. The command must be discoverable and installable through the same package paths as the other `/gadd:*` commands.

Expected touch points:

- `agent-skills.json`
- `README.md`
- `GEMINI.md`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `gemini-extension.json`
- `commands/gadd/verify.md`
- `commands/gadd/verify.toml`
- `skills/gadd-verify/SKILL.md`
- `skills/gadd-verify/agents/openai.yaml`
- `scripts/validate-gadd-mvp.sh`

## Acceptance criteria

- `/gadd:verify` is listed wherever the package lists supported GADD commands.
- Codex/OpenAI, Claude Code, and Gemini adapter files exist and point to the canonical `skills/gadd-verify/SKILL.md`.
- The new verify skill states that repo-local ledger state is canonical and external mutations require human confirmation.
- The validation script requires the new verify package files and still rejects external skill dependencies.
- `./scripts/validate-gadd-mvp.sh` and `git diff --check` pass.

## Blocked by

None.

## User stories covered

1, 2, 3, 5

## GADD Traceability

- Parent PRD: `gadd/work-items/_archive/GADD-0001-verify-context-header/prd.md`
- Parent SDD: `gadd/work-items/_archive/GADD-0001-verify-context-header/sdd.md`
- Plan: `gadd/work-items/_archive/GADD-0001-verify-context-header/plan.md`
- Plan slice: `1. Add /gadd:verify package surface`
- Ledger: `gadd/work-items/_archive/GADD-0001-001-verify-package-surface/ledger.yml`
