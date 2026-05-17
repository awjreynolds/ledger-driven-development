# Level 3 Agent End-To-End Tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first Level 3 harness that drives GADD through an agent-adapter contract, validates approval gates and durable artifacts, and provides an opt-in Codex execution path.

**Architecture:** Add `tests/level3/` as a separate suite with small harness modules for adapters, sandbox setup, transcripts, local tracker state, assertions, and orchestration. Default unit tests use a deterministic scripted adapter so local validation stays offline; the Codex adapter is available through explicit configuration for real agent runs.

**Tech Stack:** Python 3 standard library, `unittest`, existing Level 2 ticket/artifact quality modules, YAML subset parser from the Level 1 validator, subprocess-based agent execution.

---

## File Structure

- Create `scripts/run-gadd-level3.py`: top-level Level 3 runner entrypoint.
- Create `tests/level3/README.md`: usage, safety, adapter, tracker, and artifact documentation.
- Create `tests/level3/harness/__init__.py`: package marker.
- Create `tests/level3/harness/agent_adapter.py`: adapter protocol, execution request/result dataclasses, adapter registry.
- Create `tests/level3/harness/codex_adapter.py`: opt-in subprocess adapter for Codex execution.
- Create `tests/level3/harness/scripted_adapter.py`: deterministic adapter used by tests and dry-run scenarios.
- Create `tests/level3/harness/transcript.py`: transcript file writer and secret scanner.
- Create `tests/level3/harness/sandbox.py`: sandbox repo creation and package seeding.
- Create `tests/level3/harness/local_tracker.py`: local tracker issue model and filesystem persistence.
- Create `tests/level3/harness/assertions.py`: approval, artifact, tracker, and quality assertions.
- Create `tests/level3/harness/run_level3.py`: config parsing, scenario loading, step execution, manifest writing.
- Create `tests/level3/harness/tests/test_agent_adapter.py`: adapter model and registry tests.
- Create `tests/level3/harness/tests/test_local_tracker.py`: local tracker tests.
- Create `tests/level3/harness/tests/test_assertions.py`: assertion tests.
- Create `tests/level3/harness/tests/test_run_level3.py`: runner config and dry-run execution tests.
- Create `tests/level3/scenarios/approval-gate-stop.yml`: default approval gate scenario.
- Create `tests/level3/scenarios/scripted-approval-full-flow.yml`: scripted full-flow scenario.
- Create `tests/level3/scenarios/small-tdd-implementation.yml`: small implementation scenario metadata.
- Modify `.gitignore`: ignore `tests/level3/.runs/`.
- Modify `scripts/validate-gadd-mvp.sh`: run Level 3 dry-run harness only if it is deterministic and offline.

## Implementation Guardrails

- Before editing any existing Python function, run GitNexus impact on that symbol if the symbol is indexed.
- Before committing, run `gitnexus_detect_changes()` for `gadd`.
- Keep live agent and live GitHub execution opt-in. Default validation must not require network, credentials, or a specific agent binary.
- Do not store tokens in manifests, transcripts, tracker files, or scenario YAML.
- Preserve failed Level 3 run directories by default.
- Keep `.claude/`, `AGENTS.md`, and `CLAUDE.md` ignored as local GitNexus artifacts.

---

### Task 1: Scaffold Level 3 Entrypoint, Package, Scenarios, And Ignore Rules

**Files:**
- Create: `scripts/run-gadd-level3.py`
- Create: `tests/level3/README.md`
- Create: `tests/level3/harness/__init__.py`
- Create: `tests/level3/scenarios/approval-gate-stop.yml`
- Create: `tests/level3/scenarios/scripted-approval-full-flow.yml`
- Create: `tests/level3/scenarios/small-tdd-implementation.yml`
- Modify: `.gitignore`

- [ ] **Step 1: Add the top-level runner entrypoint**

Create `scripts/run-gadd-level3.py`:

```python
#!/usr/bin/env python3
"""Run GADD Level 3 agent end-to-end scenarios."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.level3.harness.run_level3 import main


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Add the Level 3 harness package marker**

Create `tests/level3/harness/__init__.py`:

```python
"""GADD Level 3 agent end-to-end harness."""
```

- [ ] **Step 3: Add the Level 3 README**

Create `tests/level3/README.md`:

```markdown
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
```

- [ ] **Step 4: Add the approval gate scenario**

Create `tests/level3/scenarios/approval-gate-stop.yml`:

```yaml
id: approval-gate-stop
name: Approval gate stop
adapter: scripted
tracker: local
steps:
  - name: intake
    prompt: "Use GADD to scope a CAD layer normalization request. Stop when human approval is required."
    scripted_response: "Created gadd/work-items/CAD-PRD-1001/prd.md and stopped for human approval.\nApproval required before design continues.\n"
    scripted_files:
      gadd/work-items/CAD-PRD-1001/ledger.yml: |
        id: CAD-PRD-1001
        state: awaiting_prd_approval
        next_command: /gadd:approve CAD-PRD-1001
      gadd/work-items/CAD-PRD-1001/prd.md: |
        # PRD

        ## Problem
        CAD layer names need consistent comparison.

        ## Scope
        Normalize layer names for comparison.

        ## Non-Goals
        No renderer rewrite.

        ## Acceptance Criteria
        - Layer names are trimmed before comparison.

        ## Approval
        Human approval is required before design.
    expect:
      - approval_gate_requested: true
      - no_continuation_past_approval: true
      - artifact_exists: gadd/work-items/CAD-PRD-1001/prd.md
```

- [ ] **Step 5: Add the scripted approval full-flow scenario**

Create `tests/level3/scenarios/scripted-approval-full-flow.yml`:

```yaml
id: scripted-approval-full-flow
name: Scripted approval full flow
adapter: scripted
tracker: local
steps:
  - name: approved-design
    prompt: "Approved. Continue to design and planning for CAD layer normalization."
    scripted_response: "Created SDD and plan. Approval required before decomposition.\n"
    scripted_files:
      gadd/work-items/CAD-PRD-1001/sdd.md: |
        # SDD

        ## Boundary
        Product repo owns normalizeLayerName behavior.

        ## Affected Modules
        - cad.js

        ## Tradeoffs
        Keep normalization local to comparison logic.

        ## Verification
        Run npm test.
      gadd/work-items/CAD-PRD-1001/plan.md: |
        # Plan

        ## Slice 1
        Add failing tests for whitespace and case normalization.

        ## Slice 2
        Implement normalizeLayerName changes.
    expect:
      - artifact_exists: gadd/work-items/CAD-PRD-1001/sdd.md
      - artifact_exists: gadd/work-items/CAD-PRD-1001/plan.md
  - name: approved-decompose
    prompt: "Approved. Decompose into child work."
    scripted_response: "Created child work item and local tracker issue.\n"
    scripted_files:
      gadd/work-items/CAD-PRD-1001/children/CAD-0001/ledger.yml: |
        id: CAD-0001
        state: ready_for_implementation
        next_command: /gadd:implement CAD-0001
      gadd/work-items/CAD-PRD-1001/children/CAD-0001/work-item.md: |
        # Child Work Item

        ## Boundary
        Implement product repo normalization only.

        ## Acceptance Criteria
        - Whitespace is trimmed.
        - Case is normalized.

        ## Verification
        Run npm test.
    scripted_issues:
      - role: Child
        title: "Child: Normalize product layer names"
        body: |
          ## Boundary
          Implement product repo normalization only.

          ## Acceptance Criteria
          Whitespace is trimmed and case is normalized.

          ## Verification
          Run `npm test`.

          ## Next Action
          Implement with a failing test first.

          ## GADD Trace
          Run: scripted
          Artifact: gadd/work-items/CAD-PRD-1001/children/CAD-0001/work-item.md
        labels:
          - gadd-l2
          - type:task
    expect:
      - artifact_exists: gadd/work-items/CAD-PRD-1001/children/CAD-0001/work-item.md
      - tickets_pass_quality: true
```

- [ ] **Step 6: Add the small TDD implementation scenario metadata**

Create `tests/level3/scenarios/small-tdd-implementation.yml`:

```yaml
id: small-tdd-implementation
name: Small TDD implementation
adapter: scripted
tracker: local
steps:
  - name: implement-child
    prompt: "Implement child work item CAD-0001 with TDD and record verification."
    scripted_response: "Added failing test, implemented normalizeLayerName, reran npm test, and recorded verification.\n"
    scripted_files:
      cad.test.js: |
        import { normalizeLayerName } from "./cad.js";

        test("normalizes layer names for comparison", () => {
          expect(normalizeLayerName(" Walls ")).toBe("walls");
        });
      cad.js: |
        export function normalizeLayerName(name) {
          return name.trim().toLowerCase();
        }
      gadd/work-items/CAD-PRD-1001/children/CAD-0001/verification.md: |
        # Verification

        ## Commands
        npm test

        ## Output
        PASS cad.test.js

        ## Evidence
        Failing test was added before implementation in the agent transcript.

        ## Residual Risk
        No renderer behavior was changed.
    expect:
      - artifact_exists: gadd/work-items/CAD-PRD-1001/children/CAD-0001/verification.md
      - implementation_changed_files:
          - cad.js
          - cad.test.js
      - verification_recorded: true
```

- [ ] **Step 7: Ignore Level 3 run artifacts**

Append this line to `.gitignore` if it is not present:

```gitignore
tests/level3/.runs/
```

- [ ] **Step 8: Run syntax checks**

Run:

```sh
python3 -m py_compile scripts/run-gadd-level3.py tests/level3/harness/__init__.py
```

Expected: no output and exit code `0`.

- [ ] **Step 9: Commit the scaffold**

Run:

```sh
git add .gitignore scripts/run-gadd-level3.py tests/level3
git commit -m "test: scaffold level3 agent e2e suite"
```

---

### Task 2: Implement Agent Adapter Models And Scripted Adapter

**Files:**
- Create: `tests/level3/harness/agent_adapter.py`
- Create: `tests/level3/harness/scripted_adapter.py`
- Create: `tests/level3/harness/tests/test_agent_adapter.py`

- [ ] **Step 1: Write failing adapter tests**

Create `tests/level3/harness/tests/test_agent_adapter.py`:

```python
from pathlib import Path
import tempfile
import unittest

from tests.level3.harness.agent_adapter import AdapterRegistry, AgentExecutionRequest
from tests.level3.harness.scripted_adapter import ScriptedAgentAdapter


class AgentAdapterTests(unittest.TestCase):
    def test_registry_creates_scripted_adapter(self):
        registry = AdapterRegistry()
        registry.register("scripted", ScriptedAgentAdapter)

        adapter = registry.create("scripted")

        self.assertIsInstance(adapter, ScriptedAgentAdapter)

    def test_scripted_adapter_writes_files_and_transcript(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            request = AgentExecutionRequest(
                run_id="run-1",
                scenario_id="scenario",
                step_name="step",
                sandbox_path=root,
                prompt="Create the artifact.",
                step={
                    "scripted_response": "Approval required before design.\n",
                    "scripted_files": {
                        "gadd/work-items/ITEM/prd.md": "# PRD\n\n## Approval\nApproval required.\n"
                    },
                },
                timeout_seconds=30,
                transcript_dir=root / ".runs" / "transcripts",
            )

            result = ScriptedAgentAdapter().run(request)

            self.assertEqual(0, result.exit_status)
            self.assertTrue((root / "gadd/work-items/ITEM/prd.md").is_file())
            self.assertTrue(result.transcript_path.is_file())
            self.assertIn("Approval required", result.transcript_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the failing adapter tests**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_agent_adapter -v
```

Expected: fails with `ModuleNotFoundError` or missing classes.

- [ ] **Step 3: Implement the adapter model**

Create `tests/level3/harness/agent_adapter.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class AgentExecutionRequest:
    run_id: str
    scenario_id: str
    step_name: str
    sandbox_path: Path
    prompt: str
    step: dict
    timeout_seconds: int
    transcript_dir: Path


@dataclass(frozen=True)
class AgentExecutionResult:
    exit_status: int
    transcript_path: Path
    stdout_path: Path | None
    stderr_path: Path | None
    files_changed: list[str]
    duration_seconds: float
    failure_reason: str | None = None


class AgentAdapter(Protocol):
    def run(self, request: AgentExecutionRequest) -> AgentExecutionResult:
        """Execute one scenario step in the sandbox and return normalized evidence."""


class AdapterRegistry:
    def __init__(self) -> None:
        self._factories: dict[str, type[AgentAdapter]] = {}

    def register(self, name: str, factory: type[AgentAdapter]) -> None:
        self._factories[name] = factory

    def create(self, name: str) -> AgentAdapter:
        try:
            factory = self._factories[name]
        except KeyError as error:
            known = ", ".join(sorted(self._factories)) or "none"
            raise ValueError(f"unknown Level 3 adapter {name!r}; known adapters: {known}") from error
        return factory()
```

- [ ] **Step 4: Implement the scripted adapter**

Create `tests/level3/harness/scripted_adapter.py`:

```python
from __future__ import annotations

from pathlib import Path
import time

from tests.level3.harness.agent_adapter import AgentExecutionRequest, AgentExecutionResult


def _safe_relative_path(path: str) -> Path:
    relative = Path(path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"scripted file path must stay inside sandbox: {path}")
    return relative


class ScriptedAgentAdapter:
    def run(self, request: AgentExecutionRequest) -> AgentExecutionResult:
        started = time.monotonic()
        transcript_dir = request.transcript_dir
        transcript_dir.mkdir(parents=True, exist_ok=True)
        transcript_path = transcript_dir / f"{request.scenario_id}-{request.step_name}.md"
        response = str(request.step.get("scripted_response", ""))
        changed: list[str] = []

        for raw_path, content in request.step.get("scripted_files", {}).items():
            relative = _safe_relative_path(str(raw_path))
            target = request.sandbox_path / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(str(content), encoding="utf-8")
            changed.append(str(relative))

        transcript_path.write_text(
            f"# Transcript\n\n## Prompt\n{request.prompt}\n\n## Response\n{response}",
            encoding="utf-8",
        )
        return AgentExecutionResult(
            exit_status=0,
            transcript_path=transcript_path,
            stdout_path=None,
            stderr_path=None,
            files_changed=sorted(changed),
            duration_seconds=round(time.monotonic() - started, 3),
        )
```

- [ ] **Step 5: Run adapter tests**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_agent_adapter -v
```

Expected: 2 tests pass.

- [ ] **Step 6: Commit adapter models**

Run:

```sh
git add tests/level3/harness/agent_adapter.py tests/level3/harness/scripted_adapter.py tests/level3/harness/tests/test_agent_adapter.py
git commit -m "test: add level3 agent adapter contract"
```

---

### Task 3: Implement Transcript Secret Scanning

**Files:**
- Create: `tests/level3/harness/transcript.py`
- Modify: `tests/level3/harness/tests/test_agent_adapter.py`

- [ ] **Step 1: Add failing transcript scan tests**

Append to `tests/level3/harness/tests/test_agent_adapter.py`:

```python
from tests.level3.harness.transcript import find_secret_like_values


class TranscriptSafetyTests(unittest.TestCase):
    def test_secret_scanner_flags_token_like_values(self):
        findings = find_secret_like_values("GH_TOKEN=ghp_abcdefghijklmnopqrstuvwxyz123456")

        self.assertEqual(["token-like value detected"], [finding.message for finding in findings])

    def test_secret_scanner_allows_normal_transcript(self):
        findings = find_secret_like_values("Approval required before design continues.")

        self.assertEqual([], findings)
```

- [ ] **Step 2: Run the failing transcript tests**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_agent_adapter -v
```

Expected: fails because `tests.level3.harness.transcript` does not exist.

- [ ] **Step 3: Implement transcript secret scanning**

Create `tests/level3/harness/transcript.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
import re


TOKEN_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*=\s*[A-Za-z0-9_./-]{16,}"),
]


@dataclass(frozen=True)
class TranscriptFinding:
    message: str


def find_secret_like_values(text: str) -> list[TranscriptFinding]:
    findings: list[TranscriptFinding] = []
    for pattern in TOKEN_PATTERNS:
        if pattern.search(text):
            findings.append(TranscriptFinding("token-like value detected"))
            break
    return findings
```

- [ ] **Step 4: Run transcript tests**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_agent_adapter -v
```

Expected: all adapter and transcript tests pass.

- [ ] **Step 5: Commit transcript safety**

Run:

```sh
git add tests/level3/harness/transcript.py tests/level3/harness/tests/test_agent_adapter.py
git commit -m "test: add level3 transcript safety checks"
```

---

### Task 4: Implement Local Tracker Persistence

**Files:**
- Create: `tests/level3/harness/local_tracker.py`
- Create: `tests/level3/harness/tests/test_local_tracker.py`

- [ ] **Step 1: Write failing local tracker tests**

Create `tests/level3/harness/tests/test_local_tracker.py`:

```python
from pathlib import Path
import tempfile
import unittest

from tests.level3.harness.local_tracker import LocalIssue, LocalTracker


class LocalTrackerTests(unittest.TestCase):
    def test_creates_issue_file_with_labels(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            tracker = LocalTracker(Path(temp_dir))
            issue = tracker.create_issue(
                LocalIssue(
                    role="Child",
                    title="Child: Normalize product layer names",
                    body="## Next Action\nImplement with a failing test first.\n",
                    labels=["gadd-l2", "type:task"],
                )
            )

            self.assertEqual(1, issue.number)
            issue_path = Path(temp_dir) / "tracker" / "issues" / "1.json"
            self.assertTrue(issue_path.is_file())
            self.assertIn("type:task", issue_path.read_text(encoding="utf-8"))

    def test_lists_created_issues(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            tracker = LocalTracker(Path(temp_dir))
            tracker.create_issue(LocalIssue(role="PRD", title="PRD: Example", body="## Next Action\nReview.\n", labels=["gadd-l2"]))

            issues = tracker.list_issues()

            self.assertEqual(["PRD: Example"], [issue.title for issue in issues])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the failing local tracker tests**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_local_tracker -v
```

Expected: fails because `local_tracker.py` does not exist.

- [ ] **Step 3: Implement local tracker persistence**

Create `tests/level3/harness/local_tracker.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class LocalIssue:
    role: str
    title: str
    body: str
    labels: list[str]
    state: str = "open"
    number: int | None = None


class LocalTracker:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.issue_dir = root / "tracker" / "issues"

    def create_issue(self, issue: LocalIssue) -> LocalIssue:
        self.issue_dir.mkdir(parents=True, exist_ok=True)
        number = self._next_number()
        stored = LocalIssue(
            role=issue.role,
            title=issue.title,
            body=issue.body,
            labels=list(issue.labels),
            state=issue.state,
            number=number,
        )
        self._write_issue(stored)
        return stored

    def list_issues(self) -> list[LocalIssue]:
        if not self.issue_dir.is_dir():
            return []
        return [self._read_issue(path) for path in sorted(self.issue_dir.glob("*.json"), key=lambda item: int(item.stem))]

    def _next_number(self) -> int:
        existing = [int(path.stem) for path in self.issue_dir.glob("*.json") if path.stem.isdigit()]
        return max(existing, default=0) + 1

    def _write_issue(self, issue: LocalIssue) -> None:
        path = self.issue_dir / f"{issue.number}.json"
        path.write_text(
            json.dumps(
                {
                    "number": issue.number,
                    "role": issue.role,
                    "title": issue.title,
                    "body": issue.body,
                    "labels": issue.labels,
                    "state": issue.state,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    def _read_issue(self, path: Path) -> LocalIssue:
        data = json.loads(path.read_text(encoding="utf-8"))
        return LocalIssue(
            number=int(data["number"]),
            role=str(data["role"]),
            title=str(data["title"]),
            body=str(data["body"]),
            labels=[str(label) for label in data.get("labels", [])],
            state=str(data.get("state", "open")),
        )
```

- [ ] **Step 4: Run local tracker tests**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_local_tracker -v
```

Expected: 2 tests pass.

- [ ] **Step 5: Commit local tracker**

Run:

```sh
git add tests/level3/harness/local_tracker.py tests/level3/harness/tests/test_local_tracker.py
git commit -m "test: add level3 local tracker"
```

---

### Task 5: Implement Sandbox Seeding

**Files:**
- Create: `tests/level3/harness/sandbox.py`
- Create: `tests/level3/harness/tests/test_run_level3.py`

- [ ] **Step 1: Write failing sandbox test**

Create `tests/level3/harness/tests/test_run_level3.py`:

```python
from pathlib import Path
import tempfile
import unittest

from tests.level3.harness.sandbox import create_sandbox


class SandboxTests(unittest.TestCase):
    def test_create_sandbox_seeds_package_and_target_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            run_root = Path(temp_dir)
            sandbox = create_sandbox(
                run_root=run_root,
                scenario_id="scenario",
                seed_files={"cad.js": "export function normalizeLayerName(name) { return name; }\n"},
            )

            self.assertTrue((sandbox.path / "skills").is_dir())
            self.assertTrue((sandbox.path / "cad.js").is_file())
            self.assertEqual("scenario", sandbox.scenario_id)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the failing sandbox test**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_run_level3 -v
```

Expected: fails because `sandbox.py` does not exist.

- [ ] **Step 3: Implement sandbox seeding**

Create `tests/level3/harness/sandbox.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[3]
PACKAGE_PATHS = [
    "skills",
    "agent-skills.json",
    "README.md",
    "docs/skills.md",
    "docs/workflow.md",
    "docs/package-model.md",
]


@dataclass(frozen=True)
class Sandbox:
    scenario_id: str
    path: Path


def _copy_path(source: Path, target: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _safe_relative_path(path: str) -> Path:
    relative = Path(path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"seed file path must stay inside sandbox: {path}")
    return relative


def create_sandbox(run_root: Path, scenario_id: str, seed_files: dict[str, str] | None = None) -> Sandbox:
    sandbox_path = run_root / "sandboxes" / scenario_id
    sandbox_path.mkdir(parents=True, exist_ok=True)
    for relative_path in PACKAGE_PATHS:
        source = ROOT / relative_path
        if source.exists():
            _copy_path(source, sandbox_path / relative_path)

    for raw_path, content in (seed_files or {}).items():
        relative = _safe_relative_path(raw_path)
        target = sandbox_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    return Sandbox(scenario_id=scenario_id, path=sandbox_path)
```

- [ ] **Step 4: Run sandbox test**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_run_level3 -v
```

Expected: sandbox test passes.

- [ ] **Step 5: Commit sandbox seeding**

Run:

```sh
git add tests/level3/harness/sandbox.py tests/level3/harness/tests/test_run_level3.py
git commit -m "test: add level3 sandbox seeding"
```

---

### Task 6: Implement Assertions And Reuse Level 2 Quality Rubrics

**Files:**
- Create: `tests/level3/harness/assertions.py`
- Create: `tests/level3/harness/tests/test_assertions.py`

- [ ] **Step 1: Write failing assertion tests**

Create `tests/level3/harness/tests/test_assertions.py`:

```python
from pathlib import Path
import tempfile
import unittest

from tests.level3.harness.assertions import evaluate_expectations
from tests.level3.harness.agent_adapter import AgentExecutionResult
from tests.level3.harness.local_tracker import LocalIssue, LocalTracker


class Level3AssertionTests(unittest.TestCase):
    def test_approval_gate_detected_from_transcript(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            transcript = root / "transcript.md"
            transcript.write_text("Approval required before design continues.\n", encoding="utf-8")
            result = AgentExecutionResult(0, transcript, None, None, [], 0.1)

            findings = evaluate_expectations(root, result, [{"approval_gate_requested": True}], LocalTracker(root))

            self.assertEqual([], findings)

    def test_missing_artifact_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            transcript = root / "transcript.md"
            transcript.write_text("Done.\n", encoding="utf-8")
            result = AgentExecutionResult(0, transcript, None, None, [], 0.1)

            findings = evaluate_expectations(root, result, [{"artifact_exists": "gadd/work-items/ITEM/prd.md"}], LocalTracker(root))

            self.assertEqual(["missing expected artifact: gadd/work-items/ITEM/prd.md"], [finding.message for finding in findings])

    def test_ticket_quality_reuses_level2_rubric(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tracker = LocalTracker(root)
            tracker.create_issue(
                LocalIssue(
                    role="Child",
                    title="Child: Normalize product layer names",
                    body=(
                        "## Boundary\nImplement product repo normalization only.\n\n"
                        "## Acceptance Criteria\nWhitespace is trimmed.\n\n"
                        "## Verification\nRun `npm test`.\n\n"
                        "## Next Action\nImplement with a failing test first.\n\n"
                        "## GADD Trace\nRun: scripted\nArtifact: gadd/work-items/CAD-0001/work-item.md\n"
                    ),
                    labels=["gadd-l2", "type:task"],
                )
            )
            transcript = root / "transcript.md"
            transcript.write_text("Created issue.\n", encoding="utf-8")
            result = AgentExecutionResult(0, transcript, None, None, [], 0.1)

            findings = evaluate_expectations(root, result, [{"tickets_pass_quality": True}], tracker)

            self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the failing assertion tests**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_assertions -v
```

Expected: fails because `assertions.py` does not exist.

- [ ] **Step 3: Implement assertions**

Create `tests/level3/harness/assertions.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tests.level2.harness.ticket_quality import Ticket, evaluate_ticket
from tests.level3.harness.agent_adapter import AgentExecutionResult
from tests.level3.harness.local_tracker import LocalTracker


@dataclass(frozen=True)
class Level3Finding:
    message: str


def evaluate_expectations(
    sandbox_path: Path,
    result: AgentExecutionResult,
    expectations: list[dict],
    tracker: LocalTracker,
) -> list[Level3Finding]:
    findings: list[Level3Finding] = []
    transcript_text = result.transcript_path.read_text(encoding="utf-8") if result.transcript_path.is_file() else ""
    for expectation in expectations:
        if "approval_gate_requested" in expectation:
            if expectation["approval_gate_requested"] and "approval required" not in transcript_text.lower():
                findings.append(Level3Finding("approval gate was not requested"))
        elif "no_continuation_past_approval" in expectation:
            if expectation["no_continuation_past_approval"] and "continuing without approval" in transcript_text.lower():
                findings.append(Level3Finding("agent continued past approval gate"))
        elif "artifact_exists" in expectation:
            relative = str(expectation["artifact_exists"])
            if not (sandbox_path / relative).is_file():
                findings.append(Level3Finding(f"missing expected artifact: {relative}"))
        elif "tickets_pass_quality" in expectation:
            if expectation["tickets_pass_quality"]:
                findings.extend(_evaluate_local_ticket_quality(tracker))
        elif "verification_recorded" in expectation:
            if expectation["verification_recorded"] and not _has_verification_artifact(sandbox_path):
                findings.append(Level3Finding("verification artifact was not recorded"))
        elif "implementation_changed_files" in expectation:
            expected = sorted(str(path) for path in expectation["implementation_changed_files"])
            actual = sorted(path for path in result.files_changed if not path.startswith("gadd/"))
            if actual != expected:
                findings.append(Level3Finding(f"implementation changed files mismatch: expected {expected}, got {actual}"))
        else:
            findings.append(Level3Finding(f"unsupported expectation: {expectation}"))
    return findings


def _evaluate_local_ticket_quality(tracker: LocalTracker) -> list[Level3Finding]:
    findings: list[Level3Finding] = []
    for issue in tracker.list_issues():
        ticket = Ticket(
            role=issue.role,
            title=issue.title,
            body=issue.body,
            state=issue.state,
            labels=issue.labels,
            comments=[],
        )
        for finding in evaluate_ticket(ticket):
            findings.append(Level3Finding(f"issue {issue.number}: {finding.message}"))
    return findings


def _has_verification_artifact(sandbox_path: Path) -> bool:
    return any(path.name == "verification.md" for path in sandbox_path.glob("gadd/work-items/**/verification.md"))
```

- [ ] **Step 4: Run assertion tests**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_assertions -v
```

Expected: 3 tests pass.

- [ ] **Step 5: Commit assertions**

Run:

```sh
git add tests/level3/harness/assertions.py tests/level3/harness/tests/test_assertions.py
git commit -m "test: add level3 quality assertions"
```

---

### Task 7: Implement Level 3 Runner

**Files:**
- Create: `tests/level3/harness/run_level3.py`
- Modify: `tests/level3/harness/tests/test_run_level3.py`

- [ ] **Step 1: Add failing runner tests**

Append to `tests/level3/harness/tests/test_run_level3.py`:

```python
from tests.level3.harness.run_level3 import load_config, main, summarize_findings


class RunLevel3ConfigTests(unittest.TestCase):
    def test_default_config_uses_scripted_local(self):
        config = load_config(env={})

        self.assertEqual("scripted", config.adapter)
        self.assertEqual("local", config.tracker)

    def test_invalid_tracker_rejected(self):
        with self.assertRaises(ValueError):
            load_config(env={"GADD_L3_TRACKER": "jira"})

    def test_summary_reports_findings(self):
        self.assertEqual("2 Level 3 findings", summarize_findings(["a", "b"]))


class RunLevel3MainTests(unittest.TestCase):
    def test_scripted_runner_executes_single_case(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            exit_code = main(
                [
                    "--adapter",
                    "scripted",
                    "--tracker",
                    "local",
                    "--case",
                    "approval-gate-stop",
                    "--runs-dir",
                    temp_dir,
                ]
            )

            self.assertEqual(0, exit_code)
```

- [ ] **Step 2: Run the failing runner tests**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_run_level3 -v
```

Expected: fails because `run_level3.py` does not exist.

- [ ] **Step 3: Implement the Level 3 runner**

Create `tests/level3/harness/run_level3.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import argparse
import json
import os
from pathlib import Path
import sys

from tests.level3.harness.agent_adapter import AdapterRegistry, AgentExecutionRequest
from tests.level3.harness.assertions import evaluate_expectations
from tests.level3.harness.local_tracker import LocalIssue, LocalTracker
from tests.level3.harness.sandbox import create_sandbox
from tests.level3.harness.scripted_adapter import ScriptedAgentAdapter


ROOT = Path(__file__).resolve().parents[3]
SCENARIOS = ROOT / "tests" / "level3" / "scenarios"
RUNS_DIR = ROOT / "tests" / "level3" / ".runs"


@dataclass(frozen=True)
class Config:
    adapter: str
    tracker: str
    run_id: str
    strict_adapter: bool


class Level3Error(Exception):
    pass


def load_config(env: dict[str, str] | None = None) -> Config:
    values = dict(os.environ if env is None else env)
    adapter = values.get("GADD_L3_ADAPTER", "scripted")
    tracker = values.get("GADD_L3_TRACKER", "local")
    if tracker not in {"local", "github"}:
        raise ValueError("GADD_L3_TRACKER must be one of: local, github")
    run_id = values.get("GADD_L3_RUN_ID", f"gadd-l3-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}")
    return Config(
        adapter=adapter,
        tracker=tracker,
        run_id=run_id,
        strict_adapter=values.get("GADD_L3_STRICT_ADAPTER", "false").lower() == "true",
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run GADD Level 3 agent end-to-end scenarios.")
    parser.add_argument("--adapter", choices=["scripted", "codex"], help="Agent adapter to use.")
    parser.add_argument("--tracker", choices=["local", "github"], help="Tracker mode to use.")
    parser.add_argument("--case", help="Scenario file stem or name to run.")
    parser.add_argument("--runs-dir", type=Path, default=RUNS_DIR, help="Directory for Level 3 run artifacts.")
    parser.add_argument("--strict-adapter", action="store_true", help="Fail when the requested adapter is unavailable.")
    return parser.parse_args(argv)


def summarize_findings(findings: list) -> str:
    count = len(findings)
    if count == 0:
        return "0 Level 3 findings"
    if count == 1:
        return "1 Level 3 finding"
    return f"{count} Level 3 findings"


def load_level1_module():
    import importlib.util

    script_path = ROOT / "scripts" / "validate-gadd-level1.py"
    spec = importlib.util.spec_from_file_location("gadd_level1", script_path)
    if not spec or not spec.loader:
        raise Level3Error(f"unable to load Level 1 validator from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LEVEL1 = load_level1_module()


def load_scenarios(case: str | None) -> list[dict]:
    paths = sorted(SCENARIOS.glob("*.yml"))
    if case:
        paths = [path for path in paths if path.stem == case or path.name == case]
    if not paths:
        raise Level3Error(f"no Level 3 scenarios found for case {case!r}")
    scenarios = []
    for path in paths:
        scenario = LEVEL1.parse_yaml_subset(path)
        for required in ("id", "steps"):
            if required not in scenario:
                raise Level3Error(f"{path}: missing required field {required}")
        scenarios.append(scenario)
    return scenarios


def build_registry() -> AdapterRegistry:
    registry = AdapterRegistry()
    registry.register("scripted", ScriptedAgentAdapter)
    try:
        from tests.level3.harness.codex_adapter import CodexAgentAdapter

        registry.register("codex", CodexAgentAdapter)
    except ImportError:
        pass
    return registry


def write_manifest(path: Path, manifest: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _create_scripted_issues(step: dict, tracker: LocalTracker) -> None:
    for issue in step.get("scripted_issues", []):
        tracker.create_issue(
            LocalIssue(
                role=str(issue["role"]),
                title=str(issue["title"]),
                body=str(issue["body"]),
                labels=[str(label) for label in issue.get("labels", [])],
            )
        )


def run_scenario(config: Config, scenario: dict, runs_dir: Path, adapter_name: str, tracker_mode: str) -> list[str]:
    run_root = runs_dir / config.run_id / scenario["id"]
    sandbox = create_sandbox(run_root, scenario["id"], scenario.get("seed_files", {}))
    tracker = LocalTracker(sandbox.path)
    adapter = build_registry().create(adapter_name)
    findings: list[str] = []
    step_results = []

    for index, step in enumerate(scenario["steps"], start=1):
        step_name = str(step.get("name", index)).replace("/", "-").replace(" ", "-")
        request = AgentExecutionRequest(
            run_id=config.run_id,
            scenario_id=str(scenario["id"]),
            step_name=step_name,
            sandbox_path=sandbox.path,
            prompt=str(step.get("prompt", "")),
            step=step,
            timeout_seconds=int(step.get("timeout_seconds", 120)),
            transcript_dir=run_root / "transcripts",
        )
        result = adapter.run(request)
        _create_scripted_issues(step, tracker)
        step_findings = evaluate_expectations(sandbox.path, result, step.get("expect", []), tracker)
        findings.extend(f"{scenario['id']} / {step_name}: {finding.message}" for finding in step_findings)
        step_results.append(
            {
                "name": step_name,
                "exit_status": result.exit_status,
                "transcript": str(result.transcript_path),
                "files_changed": result.files_changed,
                "findings": [finding.message for finding in step_findings],
            }
        )

    write_manifest(
        run_root / "manifest.json",
        {
            "run_id": config.run_id,
            "scenario": scenario["id"],
            "adapter": adapter_name,
            "tracker": tracker_mode,
            "steps": step_results,
            "findings": findings,
        },
    )
    return findings


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        base_config = load_config()
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    config = Config(
        adapter=args.adapter or base_config.adapter,
        tracker=args.tracker or base_config.tracker,
        run_id=base_config.run_id,
        strict_adapter=args.strict_adapter or base_config.strict_adapter,
    )
    try:
        scenarios = load_scenarios(args.case)
        findings: list[str] = []
        for scenario in scenarios:
            findings.extend(run_scenario(config, scenario, args.runs_dir, config.adapter, config.tracker))
    except (Level3Error, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1

    for finding in findings:
        print(finding, file=sys.stderr)
    print(f"GADD Level 3 scenarios evaluated: {summarize_findings(findings)}")
    print(f"Artifacts: {args.runs_dir / config.run_id}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run runner tests**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_run_level3 -v
```

Expected: all runner and sandbox tests pass.

- [ ] **Step 5: Run the scripted Level 3 scenario**

Run:

```sh
python3 scripts/run-gadd-level3.py --adapter scripted --tracker local --case approval-gate-stop
```

Expected output includes:

```text
GADD Level 3 scenarios evaluated: 0 Level 3 findings
Artifacts: tests/level3/.runs/
```

- [ ] **Step 6: Commit runner**

Run:

```sh
git add scripts/run-gadd-level3.py tests/level3/harness/run_level3.py tests/level3/harness/tests/test_run_level3.py
git commit -m "test: add level3 scripted runner"
```

---

### Task 8: Add Opt-In Codex Adapter

**Files:**
- Create: `tests/level3/harness/codex_adapter.py`
- Create: `tests/level3/harness/tests/test_codex_adapter.py`

- [ ] **Step 1: Write failing Codex adapter tests**

Create `tests/level3/harness/tests/test_codex_adapter.py`:

```python
from pathlib import Path
import tempfile
import unittest

from tests.level3.harness.agent_adapter import AgentExecutionRequest
from tests.level3.harness.codex_adapter import CodexAgentAdapter, codex_command_from_env


class CodexAdapterTests(unittest.TestCase):
    def test_codex_command_defaults_to_codex_exec(self):
        self.assertEqual(["codex", "exec"], codex_command_from_env({}))

    def test_codex_command_reads_env_string(self):
        self.assertEqual(["codex", "exec", "--model", "gpt-5.2"], codex_command_from_env({"GADD_L3_CODEX_COMMAND": "codex exec --model gpt-5.2"}))

    def test_missing_codex_binary_returns_failure_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            adapter = CodexAgentAdapter(command=["/definitely/missing/codex"])
            request = AgentExecutionRequest(
                run_id="run",
                scenario_id="scenario",
                step_name="step",
                sandbox_path=root,
                prompt="Run GADD.",
                step={},
                timeout_seconds=1,
                transcript_dir=root / "transcripts",
            )

            result = adapter.run(request)

            self.assertNotEqual(0, result.exit_status)
            self.assertEqual("adapter executable not found", result.failure_reason)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the failing Codex adapter tests**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_codex_adapter -v
```

Expected: fails because `codex_adapter.py` does not exist.

- [ ] **Step 3: Implement the Codex adapter**

Create `tests/level3/harness/codex_adapter.py`:

```python
from __future__ import annotations

import os
import shlex
import subprocess
import time
from pathlib import Path

from tests.level3.harness.agent_adapter import AgentExecutionRequest, AgentExecutionResult


def codex_command_from_env(env: dict[str, str] | None = None) -> list[str]:
    values = dict(os.environ if env is None else env)
    return shlex.split(values.get("GADD_L3_CODEX_COMMAND", "codex exec"))


def _snapshot_files(root: Path) -> dict[str, float]:
    return {str(path.relative_to(root)): path.stat().st_mtime for path in root.rglob("*") if path.is_file()}


class CodexAgentAdapter:
    def __init__(self, command: list[str] | None = None) -> None:
        self.command = command or codex_command_from_env()

    def run(self, request: AgentExecutionRequest) -> AgentExecutionResult:
        started = time.monotonic()
        request.transcript_dir.mkdir(parents=True, exist_ok=True)
        stdout_path = request.transcript_dir / f"{request.scenario_id}-{request.step_name}.stdout.txt"
        stderr_path = request.transcript_dir / f"{request.scenario_id}-{request.step_name}.stderr.txt"
        transcript_path = request.transcript_dir / f"{request.scenario_id}-{request.step_name}.md"
        before = _snapshot_files(request.sandbox_path)

        try:
            completed = subprocess.run(
                [*self.command, request.prompt],
                cwd=request.sandbox_path,
                text=True,
                capture_output=True,
                timeout=request.timeout_seconds,
                check=False,
            )
            stdout_path.write_text(completed.stdout, encoding="utf-8")
            stderr_path.write_text(completed.stderr, encoding="utf-8")
            transcript_path.write_text(
                f"# Transcript\n\n## Prompt\n{request.prompt}\n\n## Stdout\n{completed.stdout}\n\n## Stderr\n{completed.stderr}\n",
                encoding="utf-8",
            )
            after = _snapshot_files(request.sandbox_path)
            changed = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
            return AgentExecutionResult(
                exit_status=completed.returncode,
                transcript_path=transcript_path,
                stdout_path=stdout_path,
                stderr_path=stderr_path,
                files_changed=changed,
                duration_seconds=round(time.monotonic() - started, 3),
                failure_reason=None if completed.returncode == 0 else "adapter command failed",
            )
        except FileNotFoundError:
            transcript_path.write_text(f"# Transcript\n\nAdapter executable not found: {self.command[0]}\n", encoding="utf-8")
            return AgentExecutionResult(
                exit_status=127,
                transcript_path=transcript_path,
                stdout_path=None,
                stderr_path=None,
                files_changed=[],
                duration_seconds=round(time.monotonic() - started, 3),
                failure_reason="adapter executable not found",
            )
        except subprocess.TimeoutExpired:
            transcript_path.write_text("# Transcript\n\nAdapter timed out.\n", encoding="utf-8")
            return AgentExecutionResult(
                exit_status=124,
                transcript_path=transcript_path,
                stdout_path=None,
                stderr_path=None,
                files_changed=[],
                duration_seconds=round(time.monotonic() - started, 3),
                failure_reason="adapter timed out",
            )
```

- [ ] **Step 4: Run Codex adapter tests**

Run:

```sh
python3 -m unittest tests.level3.harness.tests.test_codex_adapter -v
```

Expected: 3 tests pass.

- [ ] **Step 5: Commit Codex adapter**

Run:

```sh
git add tests/level3/harness/codex_adapter.py tests/level3/harness/tests/test_codex_adapter.py
git commit -m "test: add opt-in level3 codex adapter"
```

---

### Task 9: Wire Level 3 Into Offline Validation

**Files:**
- Modify: `scripts/validate-gadd-mvp.sh`
- Modify: `tests/level3/README.md`

- [ ] **Step 1: Run impact analysis before editing existing validation script**

Run GitNexus impact for the validation script target:

```text
gitnexus_impact({target: "scripts/validate-gadd-mvp.sh", direction: "upstream", repo: "gadd"})
```

Expected: low or no indexed impact. If HIGH or CRITICAL, stop and warn the user before editing.

- [ ] **Step 2: Add Level 3 dry-run validation to MVP script**

Modify `scripts/validate-gadd-mvp.sh` so the deterministic validation block includes:

```sh
python3 scripts/run-gadd-level3.py --adapter scripted --tracker local --case approval-gate-stop
```

Place it after the Level 2 offline smoke check and before docs validation. The script should still avoid live GitHub and live agent execution.

- [ ] **Step 3: Update Level 3 README with MVP behavior**

Append this section to `tests/level3/README.md`:

```markdown
## MVP Validation

`scripts/validate-gadd-mvp.sh` runs only the deterministic `scripted` Level 3 approval-gate scenario. Real agent execution remains opt-in through `--adapter codex` and `GADD_L3_CODEX_COMMAND`.
```

- [ ] **Step 4: Run MVP validation**

Run:

```sh
./scripts/validate-gadd-mvp.sh
```

Expected output includes:

```text
GADD Level 3 scenarios evaluated: 0 Level 3 findings
GADD MVP installable skills validated
```

- [ ] **Step 5: Commit validation wiring**

Run:

```sh
git add scripts/validate-gadd-mvp.sh tests/level3/README.md
git commit -m "test: include deterministic level3 check in mvp validation"
```

---

### Task 10: Final Verification And Documentation Check

**Files:**
- Modify only if verification finds a concrete defect.

- [ ] **Step 1: Run Level 3 unit tests**

Run:

```sh
python3 -m unittest discover tests/level3/harness/tests -v
```

Expected: all Level 3 harness tests pass.

- [ ] **Step 2: Run Level 2 unit tests**

Run:

```sh
python3 -m unittest discover tests/level2/harness/tests -v
```

Expected: all Level 2 harness tests pass.

- [ ] **Step 3: Run deterministic Level 3 suite**

Run:

```sh
python3 scripts/run-gadd-level3.py --adapter scripted --tracker local
```

Expected: all scripted scenarios pass with `0 Level 3 findings`.

- [ ] **Step 4: Run docs validation**

Run:

```sh
python3 scripts/validate-gadd-docs.py
```

Expected:

```text
GADD documentation freshness validated
```

- [ ] **Step 5: Run MVP validation**

Run:

```sh
./scripts/validate-gadd-mvp.sh
```

Expected: Level 1, Level 2 offline, Level 3 scripted, docs, and installable skills checks all pass.

- [ ] **Step 6: Run GitNexus change detection before final commit or push**

Run:

```text
gitnexus_detect_changes({repo: "gadd", scope: "all"})
```

Expected: risk is low or expected, with no surprising affected execution flows. If the risk is HIGH or CRITICAL, report it before proceeding.

- [ ] **Step 7: Inspect git status**

Run:

```sh
git status --branch --short
```

Expected: only intended Level 3 files are changed.

- [ ] **Step 8: Push after all commits are present**

Run:

```sh
git push
```

Expected: `main` pushes successfully to `origin`.

