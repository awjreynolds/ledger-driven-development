# LDD Package Model

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
| Codex | `skills/ldd-*`, `agents/openai.yaml`, `agent-skills.json` |
| Claude Code | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `skills/ldd-*` |
| Gemini Command-Line Interface (CLI) | `gemini-extension.json`, `GEMINI.md`, `commands/ldd/*.toml`, `skills/ldd-*` |

LDD skills are standalone. They must not require other installed skills such as external Test-Driven Development, issue-generation, planning, triage, or debugging skills. A host agent may provide helpful tools, but every `/ldd:*` command must carry its own workflow contract.

The current workflow design is `docs/superpowers/specs/2026-05-12-local-ledger-mvp-design.md`. Supplemental design notes capture the GitNexus code-intelligence contract and documentation freshness contract. Older GitHub-ledger specs remain as historical context only.

## Codex

Use `$skill-installer` from inside Codex and ask it to install the skills listed by `agent-skills.json`:

```text
Use $skill-installer to install all skills from
https://github.com/awjreynolds/ledger-driven-development
using agent-skills.json.
```

Until the stock installer reads `agent-skills.json` directly, install the paths in that manifest:

```text
skills/ldd-setup
skills/ldd-next
skills/ldd-research
skills/ldd-scope
skills/ldd-elaborate
skills/ldd-refine
skills/ldd-approve
skills/ldd-design
skills/ldd-plan
skills/ldd-decompose
skills/ldd-implement
skills/ldd-verify
skills/ldd-close
skills/ldd-archive
```

Installed Codex skills are local copies under `~/.codex/skills`. They are not live-linked to this repository. To update, remove the installed `ldd-*` skills, reinstall from the current `agent-skills.json`, and restart Codex.

## Claude Code

Add this repository as a plugin marketplace, then install the plugin:

```text
/plugin marketplace add awjreynolds/ledger-driven-development
/plugin install ldd@ledger-driven-development
```

Restart Claude Code after installing.

## Gemini CLI

Install this repository as a Gemini CLI extension:

```sh
gemini extensions install https://github.com/awjreynolds/ledger-driven-development
```

Restart Gemini CLI after installing. The extension provides `commands/ldd/*.toml`, which map to `/ldd:setup`, `/ldd:next`, `/ldd:research`, `/ldd:scope`, `/ldd:elaborate`, `/ldd:refine`, `/ldd:approve`, `/ldd:design`, `/ldd:plan`, `/ldd:decompose`, `/ldd:implement`, `/ldd:verify`, `/ldd:close`, and `/ldd:archive`.
