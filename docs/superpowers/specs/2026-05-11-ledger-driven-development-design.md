# Ledger-Driven Development — Superseded GitHub-Ledger Design

**Date:** 2026-05-11
**Status:** Superseded
**Superseded by:** `docs/superpowers/specs/2026-05-12-local-ledger-mvp-design.md`

This document previously described a GitHub-ledger-first MVP. That model is no longer the LDD MVP contract.

The current MVP uses repo-local `ledger.yml` files as canonical workflow state. GitHub, Linear, Jira, and similar systems are optional sync and review surfaces.

Current source-of-truth documents:

- `README.md` for package layout and installation.
- `CONTEXT.md` for canonical LDD terminology.
- `agent-skills.json` for installable skill discovery.
- `docs/superpowers/specs/2026-05-12-local-ledger-mvp-design.md` for workflow design.
- `skills/ldd-*/SKILL.md` for command behavior.

The superseded design was removed from this file to avoid stale guidance being mistaken for the current contract.
