# Add /gadd:approve command surface

## Parent

GADD-0003 - Make GADD ready for external trackers and guided next actions

## What to build

Add `/gadd:approve` as a standalone command-shaped skill for PRD and SDD approval. The command must be installable and discoverable through the same surfaces as the other `/gadd:*` commands.

Expected touch points:

- `skills/gadd-approve/SKILL.md`
- `skills/gadd-approve/agents/openai.yaml`
- `commands/gadd/approve.md`
- `commands/gadd/approve.toml`
- `agent-skills.json`
- `.claude-plugin/plugin.json`
- `gemini-extension.json`
- `README.md`
- `GEMINI.md`
- `scripts/validate-gadd-mvp.sh`

## Acceptance criteria

- `/gadd:approve <work-item-id>` is listed wherever the package lists supported GADD commands.
- Codex/OpenAI, Claude Code, and Gemini adapter files exist and point to the canonical `skills/gadd-approve/SKILL.md`.
- `/gadd:approve` approves PRD or SDD only when exactly one gate is active in ledger state.
- `/gadd:approve` explicitly refuses plan, decomposition, closure, and external mutation approval.
- Approval updates artifact frontmatter/status, ledger artifact status, `approved_artifacts`, `execution_context`, and events.
- `bash scripts/validate-gadd-mvp.sh` and `git diff --check` pass.

## Blocked by

None.

## User stories covered

5, 6, 7

## GADD Traceability

- Parent PRD: `gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/prd.md`
- Parent SDD: `gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/sdd.md`
- Plan: `gadd/work-items/_archive/GADD-0003-tracker-readiness-guided-next/plan.md`
- Plan slice: `Slice 1: /gadd:approve command surface`
- Ledger: `gadd/work-items/_archive/GADD-0003-001-approve-command-surface/ledger.yml`

