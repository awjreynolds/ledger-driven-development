# GADD Level 3 Tests

Level 3 drives installed GADD skills through an agent adapter and verifies durable repo artifacts, tracker projections, approval gates, transcripts, and manifests.

Default runs are offline:

```sh
python3 scripts/run-gadd-level3.py --adapter scripted --tracker local
```

Codex execution is opt-in:

```sh
GADD_L3_CODEX_COMMAND="codex exec" \
python3 scripts/run-gadd-level3.py --adapter codex --tracker local --strict-adapter
```

Live GitHub remains opt-in and should reuse Level 2 configuration once the local tracker path passes.

Run artifacts are written to `tests/level3/.runs/<run-id>/`. Failed runs are preserved by default.

## GitHub Tracker Mode

GitHub tracker mode is explicit and skip-safe:

```sh
GADD_L3_GITHUB_REPO=owner/sandbox \
python3 scripts/run-gadd-level3.py --adapter scripted --tracker github
```

When `GADD_L3_GITHUB_REPO` is omitted, `--tracker github` skips without mutation. Use `--strict-tracker` when a missing GitHub sandbox should fail the run. `GADD_L2_GITHUB_REPO` and `GADD_L2_GITHUB_TOKEN` are accepted as fallbacks so Level 3 can reuse the Level 2 sandbox configuration.

## MVP Validation

`scripts/validate-gadd-mvp.sh` runs only the deterministic `scripted` Level 3 approval-gate scenario. Real agent execution remains opt-in through `--adapter codex` and `GADD_L3_CODEX_COMMAND`.
