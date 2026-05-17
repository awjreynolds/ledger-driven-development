# GADD Level 2 Live-Style Tests

Level 2 tests validate GADD behavior in disposable target repositories seeded
from Level 1 fixtures. They are automated, but they intentionally avoid real
external tracker mutations.

The suite sits between deterministic Level 1 routing tests and future full
agent smoke tests:

- Level 1 derives workflow routing from fixture ledgers only.
- Level 2 creates a target repo, installs the GADD package surface, seeds a
  fixture, runs a runner adapter, and asserts observable output plus repo diffs.
- Later runner adapters can call Codex, Claude, Gemini, or another agent CLI
  without changing the scenario language.

## Run

```sh
python3 scripts/run-gadd-level2.py --runner fixture-next
```

The `fixture-next` runner is deterministic and read-only. It exercises the
Level 2 harness by deriving `/gadd:next` output from the seeded repo state.
Transcripts are written to a temp artifact directory reported by the runner.

## Scenario Format

Scenario files live in `tests/level2/scenarios/`.

```yaml
id: next-smoke
steps:
  - name: seeded needs_prd routes to research
    source_scenario: full-prd-workflow
    fixture: 01-needs-prd
    work_item: GADD-L1-PRD
    prompt: Use /gadd:next for GADD-L1-PRD.
    runner_command: /gadd:next GADD-L1-PRD
    expect_output_contains:
      - text: /gadd:research GADD-L1-PRD
    expect_changed_files: []
    expect_no_external_mutation: true
```

Fields:

- `source_scenario` and `fixture` select a Level 1 fixture to seed into the
  target repo.
- `work_item` names the Work Item under test.
- `prompt` records the live-agent prompt for transcript parity.
- `runner_command` records the intended GADD command.
- `expect_output_contains` checks transcript text. Use `text:` entries for
  command strings because the repo-local YAML subset parser treats colons as
  mapping separators inside list items.
- `expect_changed_files` asserts the full repo diff after the runner executes.
- `expect_no_external_mutation` requires the runner to report no external
  tracker writes.

## Adding Cases

For read-only navigation cases, start with `fixture-next` and assert no changed
files. For mutating command cases, add a runner adapter that executes the target
agent in the disposable repo, then assert exact changed files and ledger paths.
Keep external tracker calls behind explicit human approval in the runner.

## GitHub Projection Smoke

GitHub issue projection is a Level 2 live-adapter concern because it requires
valid `gh` API authentication. A projection smoke should use disposable issues,
record the created URLs, verify native sub-issue attachment when expected, and
close the issues after evidence is captured.

The exercised shape is:

- create one PRD issue with `gh issue create`
- create one SDD issue per affected repository
- attach SDD issues under the PRD with
  `gh api -X POST repos/<owner>/<repo>/issues/<prd-number>/sub_issues -F sub_issue_id=<issue-id>`
- verify `sub_issues_summary.total`
- close the disposable child issues and parent issue

Do not print, commit, or pass GitHub tokens through scenario files. Use the
current authenticated `gh` keyring state.
