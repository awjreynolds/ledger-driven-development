# GADD Package Model

The canonical package manifest is `agent-skills.json`.

The canonical skill source is the Agent Skills layout:

```text
skills/<skill-name>/SKILL.md
skills/<skill-name>/assets/
skills/<skill-name>/agents/openai.yaml
```

`agent-skills.json` lists every installable skill path and adapter manifest. Adapter-specific files point back to the matching skill. They are not a second source of truth.

Adapter manifests make the same skills installable in specific agents:

| Agent | Adapter files |
| --- | --- |
| Codex | `skills/gadd-*`, `agents/openai.yaml`, `agent-skills.json` |
| Claude Code | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `skills/gadd-*` |
| Gemini Command-Line Interface (CLI) | `gemini-extension.json`, `GEMINI.md`, `commands/gadd/*.toml`, `skills/gadd-*` |

GADD skills are standalone. They must not require other installed skills such as external Test-Driven Development, issue-generation, planning, triage, or debugging skills. A host agent may provide helpful tools, but every `/gadd:*` command must carry its own workflow contract.

The current workflow design is `docs/superpowers/specs/2026-05-12-local-ledger-mvp-design.md`. Supplemental design notes capture the GitNexus code-intelligence contract and documentation freshness contract. Older GitHub-ledger specs remain as historical context only.

## Codex

Use `$skill-installer` from inside Codex and ask it to install the skills listed by `agent-skills.json`:

```text
Use $skill-installer to install all skills from
https://github.com/awjreynolds/gadd
using agent-skills.json.
```

Until the stock installer reads `agent-skills.json` directly, install the paths in that manifest:

```text
skills/gadd-setup
skills/gadd-next
skills/gadd-research
skills/gadd-scope
skills/gadd-elaborate
skills/gadd-refine
skills/gadd-approve
skills/gadd-design
skills/gadd-plan
skills/gadd-decompose
skills/gadd-implement
skills/gadd-verify
skills/gadd-close
skills/gadd-archive
```

Installed Codex skills are local copies under `~/.codex/skills`. They are not live-linked to this repository. To update, remove the installed `gadd-*` skills, reinstall from the current `agent-skills.json`, and restart Codex.

## Claude Code

Add this repository as a plugin marketplace, then install the plugin:

```text
/plugin marketplace add awjreynolds/gadd
/plugin install gadd@gadd
```

Restart Claude Code after installing.

## Gemini CLI

Install this repository as a Gemini CLI extension:

```sh
gemini extensions install https://github.com/awjreynolds/gadd
```

Restart Gemini CLI after installing. The extension provides `commands/gadd/*.toml`, which map to `/gadd:setup`, `/gadd:next`, `/gadd:research`, `/gadd:scope`, `/gadd:elaborate`, `/gadd:refine`, `/gadd:approve`, `/gadd:design`, `/gadd:plan`, `/gadd:decompose`, `/gadd:implement`, `/gadd:verify`, `/gadd:close`, and `/gadd:archive`.
