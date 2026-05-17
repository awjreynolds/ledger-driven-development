# Level 3 Agent End-To-End Test Design

**Date:** 2026-05-17
**Status:** proposed design
**Context:** adding a real agent execution layer above deterministic Level 1 workflow tests and live Level 2 GitHub quality checks.

## Summary

GADD Level 3 should prove that installed GADD skills work when driven by a real agent runtime, not only by deterministic harness code. Level 1 validates local workflow logic. Level 2 validates live GitHub projection mechanics, ticket quality, artifact quality, drift behavior, and handoff resilience through a deterministic harness. Level 3 should exercise the whole agent-facing workflow: prompts, approval gates, skill execution, repo-local artifacts, tracker projections, implementation evidence, and verification records.

The first Level 3 implementation should be runtime-agnostic by design, with one concrete Codex adapter. The harness should default to an offline local tracker so it can run without credentials, and support opt-in live GitHub mode once local behavior is stable.

## Goals

- Prove GADD skills can be installed into a sandbox repo and used by a real agent runtime.
- Verify that agents stop at human approval gates and do not invent approval.
- Drive a full scripted approval flow through durable repo artifacts and tracker projections.
- Exercise one small TDD implementation scenario with test, code, verification, and evidence.
- Reuse Level 2 ticket and artifact quality rubrics instead of duplicating quality logic.
- Preserve transcripts, manifests, sandboxes, and failure artifacts for debugging.
- Keep the architecture open to later Claude, Gemini, or other agent adapters without making them part of the first deliverable.

## Non-Goals

- Do not certify every agent runtime in the first Level 3 implementation.
- Do not make live GitHub required for default local validation.
- Do not bypass GADD approval gates in order to make tests easier.
- Do not treat transcript text as the only source of truth; durable artifacts must be inspected.
- Do not wire Level 3 into required pull request validation until it is stable.
- Do not mutate production repositories or unmarked tracker artifacts.

## Test Layer Model

GADD should use three explicit test layers:

```text
Level 1: deterministic local workflow tests
  - no external tracker
  - no real agent runtime
  - fast offline validation of workflow state

Level 2: live GitHub projection and quality tests
  - deterministic harness
  - real GitHub sandbox repositories when configured
  - ticket, artifact, drift, PR evidence, and handoff quality gates

Level 3: agent end-to-end workflow tests
  - installed GADD skills
  - real agent runtime through an adapter
  - local tracker by default
  - opt-in live GitHub tracker mode
```

Level 3 is not a replacement for Level 2. It should call or reuse Level 2 quality checks after the agent creates artifacts and tickets.

## Architecture

Create a separate Level 3 suite:

```text
tests/level3/
  README.md
  scenarios/
    approval-gate-stop.yml
    scripted-approval-full-flow.yml
    small-tdd-implementation.yml
    adversarial-handoff.yml
    drift-and-recovery.yml
  harness/
    __init__.py
    agent_adapter.py
    codex_adapter.py
    local_tracker.py
    github_tracker.py
    run_level3.py
    assertions.py
    transcript.py
    sandbox.py
```

The harness owns scenario setup, sandbox creation, skill installation, tracker setup, prompt sequencing, scripted approvals, timeouts, transcript capture, manifest writing, and post-run assertions.

Agent execution sits behind an `AgentAdapter` contract. The adapter receives a sandbox path, scenario step, environment, and timeout. It returns a normalized execution result with exit status, transcript path, command output, changed files, duration, and failure reason.

The first concrete adapter should drive Codex. The scenario model should not depend on Codex-specific transcript formatting outside the adapter.

## Tracker Modes

Level 3 should support two tracker modes:

- `local`: default mode. The harness writes local issue records in a deterministic format and applies the same quality expectations without requiring GitHub credentials.
- `github`: opt-in mode. The harness uses configured sandbox repositories and reuses Level 2 GitHub client, cleanup, and ticket quality behavior.

The scenario contract should be identical where practical. A scenario that passes in local mode can later run against GitHub to prove the external collaboration surface.

## Scenario Set

### 1. Approval Gate Stop

The agent receives a weak but plausible product request. It must create or update the appropriate GADD artifact and then stop at a human approval gate.

Passing requires:

- the transcript shows an explicit approval request,
- the agent does not silently continue past the gate,
- ledger state and next command match the gate,
- no tracker projection claims approval that was not supplied.

### 2. Scripted Approval Full Flow

The harness supplies explicit approval prompts at known gates. The agent proceeds from intake or scope through PRD or triage, SDD and plan, decomposition, and tracker projection.

Passing requires:

- repo-local PRD or triage artifact exists,
- SDD and plan exist where required,
- child work items exist and are independently grabbable,
- tracker tickets pass Level 2 ticket quality,
- artifact links resolve to durable repo files.

### 3. Small TDD Implementation

The agent picks one child work item and performs a small implementation slice.

Passing requires:

- a test is added or changed before the implementation is accepted,
- code changes are bounded to the child work item,
- verification command output is captured,
- `verification.md` records commands, results, evidence links, and residual risk,
- work is not closed solely because a PR or code diff exists.

### 4. Adversarial Handoff

The agent starts from an incomplete or stale local or GitHub ticket.

Passing requires:

- the agent repairs the handoff by creating precise artifacts or tracker updates, or stops with a specific blocker,
- no hidden conversation context is required to continue,
- next action is explicit and useful to a non-GADD engineer or external agent.

### 5. Drift And Recovery

The harness mutates tracker state after projection. The agent must detect drift and ask for reconciliation instead of overwriting human changes.

Passing requires:

- body, comment, or label drift is detected,
- stale managed updates are blocked,
- the reconciliation action names the changed surface and required human decision.

## Execution Model

Each scenario runs in an isolated sandbox worktree or temporary repository. The harness installs the current GADD skills into the sandbox, initializes tracker mode, and invokes the selected adapter.

Scenario files should use a turn-based structure:

```yaml
id: scripted-approval-full-flow
name: Scripted approval full flow
adapter: codex
tracker: local
steps:
  - name: scope-intake
    prompt: "Run GADD for this product request..."
    expect:
      - artifact_exists: prd
      - approval_gate_requested: prd
  - name: design-after-approval
    prompt: "Approved. Continue to design."
    expect:
      - artifact_exists: sdd
      - artifact_exists: plan
  - name: decompose-after-approval
    prompt: "Approved. Decompose into child work."
    expect:
      - child_items_exist: true
      - tickets_pass_quality: true
```

The adapter returns normalized execution data:

```text
exit_status
transcript_path
stdout_path
stderr_path
files_changed
duration_seconds
failure_reason
```

The harness writes a manifest for every run under an ignored run directory. Failed runs preserve the sandbox and transcript by default.

## Quality Gates

Level 3 passes only when both behavior and artifacts are correct.

Behavior gates:

- The agent stops at required approval gates.
- The agent does not invent or imply human approval.
- Weak or code-impacting input is routed to the correct GADD workflow path.
- Uncertainty and blockers are recorded instead of hidden.
- Hidden conversation context is not treated as durable workflow state.
- Work is not closed based only on PR existence or partial implementation.

Artifact gates:

- Ledger state matches the next command.
- PRD, SDD, plan, child work, and verification artifacts contain enough detail for handoff.
- Tracker tickets pass the Level 2 ticket quality rubric.
- Repo-local artifacts pass the Level 2 artifact quality rubric.
- Implementation scenarios include test-first evidence or a failing-then-passing test transcript.
- Verification records commands, outputs, evidence links, and residual risk.

Safety gates:

- Tokens and credentials do not appear in transcripts, manifests, tickets, or artifacts.
- Live GitHub mutation happens only when explicitly configured.
- Cleanup only touches run-marked artifacts.
- Failed runs are preserved by default.
- Timeouts stop runaway agent sessions and record enough evidence to resume or diagnose.

## First Implementation Boundary

The first Level 3 implementation should include:

- `tests/level3/` harness skeleton,
- scenario YAML format,
- local tracker adapter,
- Codex agent adapter contract and one executable path,
- transcript and manifest capture,
- approval-gate assertions,
- scripted full-flow scenario,
- small TDD implementation scenario,
- reuse of Level 2 ticket and artifact quality rubrics,
- opt-in live GitHub tracker mode only after local mode passes.

Deferred:

- Claude, Gemini, and other runtime adapters,
- required CI execution,
- broad multi-repo implementation,
- long-running scheduled runs,
- automatic PR creation in production repositories,
- support for non-GitHub external trackers.

## Error Handling

The harness should fail closed with actionable diagnostics.

- Missing adapter executable: skip only when non-strict mode is requested; otherwise fail.
- Agent timeout: stop the scenario, preserve transcript and sandbox, and report the last completed step.
- Missing approval gate: fail with transcript location and expected gate.
- Unexpected continuation past approval: fail and report changed files or tracker mutations after the gate.
- Missing tracker credentials in GitHub mode: skip or fail according to strictness, before mutation.
- Drift in tracker mode: stop and report the exact changed surface.
- Cleanup failure: preserve manifest and print manual cleanup targets.

## Success Criteria

Level 3 is successful when:

- at least one real agent adapter can install and run GADD skills in a sandbox,
- approval gate behavior is observable and enforced,
- a scripted approval flow produces coherent repo artifacts and tracker projections,
- a small TDD implementation produces bounded code changes and verification evidence,
- local mode runs without GitHub credentials,
- live GitHub mode can reuse Level 2 quality gates when configured,
- failures leave enough transcript and manifest evidence for a developer to fix the skill or harness.

