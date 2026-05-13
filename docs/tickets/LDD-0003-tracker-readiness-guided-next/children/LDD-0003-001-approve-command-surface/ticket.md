# Add /ldd:approve command surface

## Parent

LDD-0003 - Make LDD ready for external trackers and guided next actions

## What to build

Add `/ldd:approve` as a standalone command-shaped skill for PRD and SDD approval. The command must be installable and discoverable through the same surfaces as the other `/ldd:*` commands.

Expected touch points:

- `skills/ldd-approve/SKILL.md`
- `skills/ldd-approve/agents/openai.yaml`
- `commands/ldd/approve.md`
- `commands/ldd/approve.toml`
- `agent-skills.json`
- `.claude-plugin/plugin.json`
- `gemini-extension.json`
- `README.md`
- `GEMINI.md`
- `scripts/validate-ldd-mvp.sh`

## Acceptance criteria

- `/ldd:approve <ticket-id>` is listed wherever the package lists supported LDD commands.
- Codex/OpenAI, Claude Code, and Gemini adapter files exist and point to the canonical `skills/ldd-approve/SKILL.md`.
- `/ldd:approve` approves PRD or SDD only when exactly one gate is active in ledger state.
- `/ldd:approve` explicitly refuses plan, decomposition, closure, and external mutation approval.
- Approval updates artifact frontmatter/status, ledger artifact status, `approved_artifacts`, `execution_context`, and events.
- `bash scripts/validate-ldd-mvp.sh` and `git diff --check` pass.

## Blocked by

None.

## User stories covered

5, 6, 7

## LDD Traceability

- Parent PRD: `docs/tickets/LDD-0003-tracker-readiness-guided-next/prd.md`
- Parent SDD: `docs/tickets/LDD-0003-tracker-readiness-guided-next/sdd.md`
- Plan: `docs/tickets/LDD-0003-tracker-readiness-guided-next/plan.md`
- Plan slice: `Slice 1: /ldd:approve command surface`
- Ledger: `docs/tickets/LDD-0003-tracker-readiness-guided-next/children/LDD-0003-001-approve-command-surface/ledger.yml`

