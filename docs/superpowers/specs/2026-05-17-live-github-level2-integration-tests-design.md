# Live GitHub Level 2 Integration Tests Design

**Date:** 2026-05-17
**Status:** proposed design
**Context:** adding an integration test layer above the existing deterministic Level 1 workflow tests so GADD can prove its GitHub projection model against a real, persistent GitHub repository.

## Summary

GADD should add a Level 2 integration test suite that lives in this repository and runs against a configured persistent GitHub sandbox repository.

Level 1 already validates deterministic repo-local ledger routing. Level 2 should validate the enterprise-facing claim that GADD can operate with GitHub as an external collaboration surface while preserving the repo-local ledger as canonical workflow state. The sandbox GitHub repository is test state, not the home for the test definitions. The executable harness, scenarios, documentation, and cleanup tools live under `tests/level2/` in this repo.

The suite should be explicit opt-in. It must not run as part of normal local validation unless the required GitHub environment variables are present and the caller asks for Level 2. At first, CI should run it only through a manual or scheduled workflow, not on every pull request.

## Goals

- Prove GADD's GitHub projection behavior against real GitHub issues, comments, labels, branches, and pull requests.
- Keep repo-local `ledger.yml` state canonical even when GitHub state changes.
- Exercise adversarial drift where people or automation mutate GitHub after GADD last synchronized.
- Support long-running scenarios in a persistent sandbox repository rather than only sterile one-shot repos.
- Keep Level 2 separate from Level 1 so deterministic local validation remains fast and offline.
- Leave failed GitHub artifacts available for forensic inspection.
- Provide a cleanup path for completed successful runs.

## Non-Goals

- Do not replace Level 1 with live GitHub tests.
- Do not make GitHub state canonical.
- Do not require GitHub credentials for default local validation.
- Do not create or delete a fresh GitHub repository for every run.
- Do not test Linear, Jira, or other external trackers in this layer.
- Do not silently clean up failed runs before humans can inspect them.

## Test Layer Model

GADD should use three test layers:

```text
Level 1: deterministic local workflow tests
  - existing tests/level1/
  - no agent
  - no external tracker
  - no live mutation

Level 2: live GitHub projection integration tests
  - new tests/level2/
  - executable harness in this repo
  - persistent GitHub sandbox repo as external state
  - opt-in local/manual CI execution

Future Level 3: end-to-end agent workflow tests
  - optional later layer
  - may invoke agent commands across a full GADD workflow
```

Level 2 should test GitHub integration and sync semantics, not full autonomous agent behavior. It can use focused harness operations and fixture ledgers to simulate GADD command inputs and expected outputs.

## Repository Shape

Recommended structure:

```text
tests/level2/
  README.md
  scenarios/
    github-projection.yml
    github-drift.yml
    github-pr-evidence.yml
  fixtures/
    ...
  harness/
    github_client.py
    run_level2.py
    cleanup_level2.py
```

Top-level scripts should expose the suite without making it part of MVP validation:

```text
scripts/validate-gadd-level2-github.py
```

`scripts/validate-gadd-mvp.sh` should continue to run Level 1 and docs validation only. A future CI workflow can call the Level 2 script when GitHub secrets are configured.

## Sandbox Repository Contract

The sandbox is a persistent GitHub repository configured at runtime:

```sh
GADD_L2_GITHUB_REPO=owner/repo
GADD_L2_GITHUB_TOKEN=...
```

Optional controls:

```sh
GADD_L2_RUN_ID=...
GADD_L2_CLEANUP=success|always|never
GADD_L2_KEEP_FAILED=true
GADD_L2_DEFAULT_BRANCH=main
```

The token must be scoped narrowly enough for a sandbox but broad enough to create and update issues, labels, comments, branches, and pull requests in that repository.

The persistent repository should be treated like an arbitrary customer repository:

- it may already have unrelated files, issues, branches, labels, and pull requests,
- tests must avoid assuming a clean issue number sequence,
- tests must identify their own artifacts using run IDs and labels,
- cleanup must target only artifacts created by the current or selected historical run.

## Run Isolation

Every Level 2 run should generate or accept a stable run ID:

```text
gadd-l2-YYYYMMDD-HHMMSS-<short-random>
```

All GitHub artifacts created by the run should include the run ID through one or more of:

- label: `gadd-l2`
- label: `gadd-l2:<run-id>` when GitHub label syntax allows the chosen ID safely
- issue or PR title prefix: `[GADD L2 <run-id>]`
- body traceability block
- branch prefix: `gadd-l2/<run-id>/...`
- local result manifest

The harness should write a local result manifest for each run:

```text
tests/level2/.runs/<run-id>/manifest.json
```

The manifest should record issue numbers, PR numbers, branch names, labels, comments, timestamps, and cleanup status. `.runs/` should be gitignored.

## Required Scenarios

### 1. GitHub Projection

Validates that GADD can project a local Work Item boundary into GitHub.

Expected coverage:

- create or bind a GitHub issue for a Work Item,
- add a GADD traceability block or managed comment,
- apply additive managed labels,
- record external binding metadata in a fixture or generated ledger,
- verify that the local ledger remains the expected source of workflow state.

Key assertion: GitHub receives a useful projection, but local ledger fields still determine the next GADD command.

### 2. GitHub Drift

Validates adversarial external mutation.

Expected coverage:

- create a projected issue,
- record `external_updated_at` and body or comment hash,
- mutate the issue on the GitHub side as a different actor would,
- attempt a managed update using stale metadata,
- confirm the harness reports drift and refuses to overwrite without reconciliation.

Drift mutations should include at least:

- issue body edit,
- new human comment,
- label change that conflicts with managed GADD labels.

Key assertion: GADD stops automatic sync and asks for human reconciliation when GitHub changed after the last synchronized read.

### 3. GitHub PR Evidence

Validates pull request projection as implementation review evidence.

Expected coverage:

- create a test branch,
- open a pull request linked to a Work Item,
- read PR state, reviewable URL, merge state, and merge commit when available,
- confirm PR data can be recorded as implementation evidence,
- confirm PR state does not automatically close or verify the local Work Item.

Key assertion: GitHub PR state is evidence, not workflow closure.

### 4. Long-Running Reconciliation

Validates that the persistent sandbox can support scenarios across multiple invocations.

Expected coverage:

- start a run and leave an issue open intentionally,
- resume by run ID,
- read the existing GitHub artifact,
- detect whether it is unchanged, drifted, or already closed,
- apply the expected reconciliation behavior.

Key assertion: GADD can reason about durable external state rather than relying on one process lifetime.

## Cleanup Policy

Default cleanup should be conservative:

- successful runs may clean up created branches and close created issues/PRs when `GADD_L2_CLEANUP=success`,
- failed runs should leave artifacts open by default,
- cleanup should never touch artifacts that do not carry the run ID,
- cleanup should write its own summary into the run manifest.

`cleanup_level2.py` should support explicit cleanup by run ID:

```sh
python3 tests/level2/harness/cleanup_level2.py --run-id <run-id>
```

The cleanup command may close issues and PRs, delete test branches, and remove run-specific labels where safe. It should avoid deleting shared labels such as `gadd-l2` unless explicitly requested.

## Error Handling And Safety

The harness must fail closed.

- Missing `GADD_L2_GITHUB_REPO` or token: skip with a clear message unless strict mode is requested.
- Token lacks permissions: fail before creating partial state where possible.
- GitHub rate limit or transient failure: report enough context to resume or clean up.
- Existing sandbox artifacts conflict with a run ID: stop and ask for a new run ID or explicit resume.
- External drift detected: stop the scenario and report the exact changed surface.
- Cleanup failure: preserve the manifest and print the manual cleanup targets.

The harness should avoid broad destructive operations. It should never delete the sandbox repository, force-push over non-test branches, or mutate unmarked issues.

## CI And Local Execution

Local execution should be explicit:

```sh
GADD_L2_GITHUB_REPO=owner/sandbox \
GADD_L2_GITHUB_TOKEN=... \
python3 scripts/validate-gadd-level2-github.py
```

CI should start as manual or scheduled only:

- manual `workflow_dispatch` for active dogfooding,
- optional nightly run after stability improves,
- no required pull-request check until the suite is reliable and cleanup behavior is proven.

The CI workflow should use a sandbox-only secret and should preserve logs and the run manifest as artifacts.

## Relationship To GADD Product Semantics

Level 2 should reinforce the domain model:

- Work Item ledgers are canonical.
- GitHub issues are rich projections and external collaboration surfaces.
- GitHub labels are projection metadata.
- GitHub comments and issue bodies may be human-facing triage or traceability surfaces.
- GitHub PRs are implementation review evidence.
- External drift stops automatic sync until a human reconciles.

This suite should make those semantics executable.

## Implementation Defaults

The first implementation should use a thin Python harness with GitHub's REST API. It should avoid adding third-party dependencies unless the existing project adopts them elsewhere.

Scenario YAML should describe scenario names, required capabilities, and expected outcomes. Python harness code should own the detailed GitHub action sequence until the suite has enough repeated patterns to justify a richer scenario DSL.

Generated Level 2 local state should use temporary fixture directories under `tests/level2/.runs/<run-id>/local-repo/`. The generated ledgers should follow the same field names used by Level 1 fixtures and the setup templates, with external binding metadata added only where the scenario needs it.

The first implementation should not create a reusable fake GitHub adapter. It should keep GitHub operations behind a small `GitHubClient` class so a fake adapter can be added later without rewriting scenario logic.

The first implementation should build around the current skill contracts and templates rather than introducing a shared external sync module. If the tests reveal duplicated sync logic that belongs in product code, that extraction should become a separate follow-up Work Item.
