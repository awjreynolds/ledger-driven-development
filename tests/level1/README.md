# GADD Level 1 Workflow Tests

Level 1 tests validate deterministic repo-local workflow state. They do not run
an agent, call external trackers, or mutate real Work Items.

The suite is intentionally narrow:

- scenario YAML files define the expected route at each gate
- fixture `ledger.yml` files provide canonical GADD state
- `scripts/validate-gadd-level1.py` derives the next command from fixture state
- `scripts/validate-gadd-docs.py` keeps README, workflow docs, and shareable workflow assets fresh
- `scripts/validate-gadd-mvp.sh` runs the Level 1 suite as part of repo validation

## Coverage

The initial suite covers the three route families:

- `direct-implementation.yml`: approved triage -> implementation -> verification -> closure -> optional archive
- `sdd-engineering-change.yml`: `needs_sdd` -> SDD approval -> single implementation or plan/decompose route
- `full-prd-workflow.yml`: `needs_prd` -> research/scope/elaborate/refine -> PRD approval -> design -> SDD approval -> plan -> plan approval -> decompose -> child implementation/verification/closure -> parent roll-up closure
- `terminal-triage.yml`: duplicate, out-of-scope, and not-GADD-work routes remain blocked terminal states

## Scenario Format

Each scenario has a stable `id`, parent `work_item`, and ordered `steps`.
Every step must assert `expect_next_command`; optional cleanup expectations can
use a concrete command or `absent`.

```yaml
id: direct-implementation
work_item: GADD-L1-DIRECT
steps:
  - name: approved triage routes to implementation
    fixture: 01-ready
    expect_next_command: /gadd:implement GADD-L1-DIRECT
    expect_next_human_action: none
```

Each step points to a fixture directory:

```text
tests/level1/fixtures/<scenario-id>/<fixture>/
  gadd/work-items/<work-item-id>/ledger.yml
```

Child Work Items live under the parent fixture:

```text
gadd/work-items/<parent-id>/children/<child-id>/ledger.yml
```

## Adding A Route Test

1. Add or extend a scenario in `tests/level1/scenarios/`.
2. Add a fixture ledger under `tests/level1/fixtures/<scenario-id>/<fixture>/`.
3. Run:

```sh
python3 scripts/validate-gadd-level1.py
```

4. Run the full repository validation:

```sh
./scripts/validate-gadd-mvp.sh
```

## Documentation Freshness

The shareable workflow image is generated from
`docs/assets/gadd-sdlc-workflow.source.svg`. The exported SVG and PNG must stay
byte-for-byte fresh. The docs validator regenerates the PNG with `rsvg-convert`
and fails if the committed image is stale.

The validator also checks current workflow language across README,
`docs/workflow.md`, `docs/skills.md`, and the SVG source. If a GADD route,
gate, or maturity statement changes, update the docs and image in the same
change as the skill contract.
