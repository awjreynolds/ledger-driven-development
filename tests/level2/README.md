# GADD Level 2 Tests

Level 2 has two parts:

- `fixture-next`: offline smoke coverage for deterministic `/gadd:next` routing.
- Live GitHub quality suite: opt-in checks for GitHub ticket mechanics, ticket quality, artifact quality, drift handling, PR evidence, and agent handoff resilience.

## Offline Smoke

```sh
python3 scripts/run-gadd-level2.py --runner fixture-next
```

The offline runner creates a disposable target repo from Level 1 fixtures and asserts the derived `/gadd:next` output plus repo diffs. It does not mutate GitHub.

## Live GitHub Quality Suite

Required:

```sh
GADD_L2_GITHUB_REPO=owner/product-sandbox
```

Optional:

```sh
GADD_L2_GITHUB_TOKEN=...
GADD_L2_RENDER_REPO=owner/render-sandbox
GADD_L2_PRODUCT_REPO_PATH=/path/to/product/repo
GADD_L2_RENDER_REPO_PATH=/path/to/render/repo
GADD_L2_RUN_ID=gadd-l2-manual-001
GADD_L2_CLEANUP=success
```

When `GADD_L2_GITHUB_TOKEN` is omitted, the harness uses the current authenticated `gh` keyring state.

Run live creation and quality gates:

```sh
python3 scripts/validate-gadd-level2-github.py
```

Audit existing sandbox tickets without creating new issues:

```sh
python3 scripts/validate-gadd-level2-github.py --audit-existing
```

Clean up a run:

```sh
python3 tests/level2/harness/cleanup_level2.py --run-id <run-id>
```

## Quality Gate

The suite fails tickets that are vague, stale, missing labels, missing traceability, missing repo artifact links, closed with unchecked checklist items, or impossible for an engineer or external agent to pick up safely from GitHub plus the repository.

Ticket quality and artifact quality are checked together. A concise ticket can pass when it clearly points to strong repo-local artifacts. A long ticket can fail when it hides the boundary, next action, or verification evidence.

## Skill Hardening Loop

1. Run `--audit-existing`.
2. Run live Level 2 creation.
3. Fix GADD skills and templates.
4. Push the skill package.
5. Reinstall skills into sandbox repositories.
6. Rerun until ticket and artifact quality pass.

Print the push/reinstall commands:

```sh
python3 tests/level2/harness/skill_refresh.py
```

Execute them only when you intend to mutate the remote and sandboxes:

```sh
python3 tests/level2/harness/skill_refresh.py --execute
```

## Safety

- Only configured sandbox repositories may be mutated.
- Every live issue carries `gadd-l2` and `gadd-l2:<run-id>` labels.
- Cleanup refuses to touch issues missing those labels.
- Failed runs remain open by default for inspection.
- Tokens must not be committed, printed, or stored in scenario files.
