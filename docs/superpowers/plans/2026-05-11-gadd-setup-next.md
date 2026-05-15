# GADD Command-Shaped Skills Implementation Plan

> Superseded for workflow semantics by `docs/superpowers/specs/2026-05-12-local-ledger-mvp-design.md`. This plan remains historical implementation context for the first command-shaped skill package.

> Supersedes the earlier `gadd-core` packaging plan. The MVP now exposes installable skills that match the user-facing `/gadd:*` command surface.

**Goal:** Build the first installable GADD MVP skill set: one skill per command, with the shared GADD contract duplicated in each command skill instead of hidden in a separate core skill.

**Architecture:** `skills/gadd-<command>/SKILL.md` is the canonical source for each command. Shared rules stay short and local to each skill: repo-local ledgers are canonical, external tracker mutations require human confirmation, and GADD must not create duplicate progress/audit state. The setup skill owns the bundled templates copied into target repositories. `agent-skills.json` is the package manifest for the installable skill set.

**Tech Stack:** Codex/OpenAI installable skills, YAML skill UI metadata, Markdown templates, POSIX shell validation, `git`, `gh`.

## File Structure

- `skills/gadd-setup/SKILL.md`
  - Bootstraps a target repository with `.gadd/config.yml`, `.gadd/templates/`, and `docs/tickets/`.
  - Does not mutate GitHub, create labels, install Actions, or create ADR folders.
- `skills/gadd-next/SKILL.md`
  - Read-only workflow diagnosis for a single GitHub issue.
  - Reads GitHub-native issue and PR state and reports the next GADD command.
- `skills/gadd-scope/SKILL.md`
  - Product Manager PRD scoping.
- `skills/gadd-elaborate/SKILL.md`
  - Product Manager PRD elaboration.
- `skills/gadd-refine/SKILL.md`
  - Product Manager PRD handoff refinement and PRD PR prompt.
- `skills/gadd-design/SKILL.md`
  - SE-hat SDD creation and ADR threshold check.
- `skills/gadd-plan/SKILL.md`
  - Implementation plan and generated `plan.html` from approved design.
- `skills/gadd-decompose/SKILL.md`
  - Approved plan slices become child vertical-slice tickets.
- `skills/gadd-implement/SKILL.md`
  - Plan execution with code and tests.
- `skills/gadd-*/agents/openai.yaml`
  - UI metadata for each installable command skill.
- `skills/gadd-setup/assets/templates/*`
  - Setup-owned templates copied into target repositories.
- `scripts/validate-gadd-mvp.sh`
  - Smoke test that validates the installable command skills and setup template set.

## Validation Contract

The validation script must fail if:

- any command skill is missing `SKILL.md`
- any command skill is missing `agents/openai.yaml`
- any command skill omits its `/gadd:<command>` invocation
- any command skill omits the repo-local ledger invariant
- any command skill omits human confirmation for external tracker mutations
- Product Manager commands can read the codebase as design input
- setup templates are missing or lose their expected headings/prompts

Run:

```sh
./scripts/validate-gadd-mvp.sh
```

Expected output:

```text
GADD MVP installable skills validated
```

## Completion Checklist

- [x] Command-shaped skills exist for setup, next, scope, elaborate, refine, design, plan, decompose, and implement.
- [x] Setup skill owns the target-repo templates.
- [x] Shared GADD invariants are present in every command skill.
- [x] `gadd-core` is not a user-facing installable skill.
- [x] Validation checks the command-shaped installable surface.
