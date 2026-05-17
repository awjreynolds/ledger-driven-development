# Level 2 Ticket Quality Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a live GitHub Level 2 suite that fails weak GADD ticket projections, validates ticket-plus-artifact handoff resilience, and supports the fix-push-reinstall-rerun hardening loop.

**Architecture:** Keep the existing `fixture-next` smoke runner intact and add a separate opt-in GitHub harness under `tests/level2/harness/`. The harness uses small focused Python modules for GitHub access, ticket quality, artifact quality, scenario execution, cleanup, and skill refresh command orchestration. Unit tests validate rubric behavior offline; live commands require explicit GitHub sandbox configuration.

**Tech Stack:** Python 3 standard library, GitHub CLI/API, existing GitNexus MCP workflow, existing shell validation scripts, Markdown/YAML scenario metadata.

---

## File Structure

- Create `scripts/validate-gadd-level2-github.py`: thin entrypoint for live GitHub Level 2.
- Create `tests/level2/harness/__init__.py`: package marker.
- Create `tests/level2/harness/github_client.py`: GitHub API wrapper around `gh api` JSON calls.
- Create `tests/level2/harness/ticket_quality.py`: ticket rubric and secret scanning.
- Create `tests/level2/harness/artifact_quality.py`: repo-local artifact and ledger checks.
- Create `tests/level2/harness/gitnexus_evidence.py`: typed representation of GitNexus evidence provided by the runner.
- Create `tests/level2/harness/run_level2.py`: run/audit orchestration, manifest writing, and scenario dispatch.
- Create `tests/level2/harness/cleanup_level2.py`: cleanup run-marked GitHub artifacts.
- Create `tests/level2/harness/skill_refresh.py`: prints and optionally runs push/reinstall commands.
- Create `tests/level2/harness/tests/test_ticket_quality.py`: offline rubric tests.
- Create `tests/level2/harness/tests/test_artifact_quality.py`: offline artifact tests.
- Create `tests/level2/harness/tests/test_run_level2.py`: offline CLI/config tests.
- Create `tests/level2/scenarios/normal-product-flow.yml`: scenario metadata.
- Create `tests/level2/scenarios/bug-gitnexus-flow.yml`: scenario metadata.
- Create `tests/level2/scenarios/drift-reconciliation.yml`: scenario metadata.
- Create `tests/level2/scenarios/pr-evidence-closure.yml`: scenario metadata.
- Create `tests/level2/scenarios/handoff-resilience.yml`: scenario metadata.
- Modify `.gitignore`: ignore `tests/level2/.runs/`.
- Modify `tests/level2/README.md`: document live suite, audit mode, quality gates, cleanup, and skill refresh loop.

## Implementation Guardrails

- Before editing any Python function after it exists, run GitNexus impact on that symbol.
- Before committing, run `gitnexus_detect_changes()` for `gadd`.
- Do not wire live GitHub Level 2 into `scripts/validate-gadd-mvp.sh`.
- Do not write GitHub tokens into scenario files, manifests, logs, comments, or tickets.
- Do not mutate live GitHub unless `GADD_L2_GITHUB_REPO`, `GADD_L2_GITHUB_TOKEN`, and a live command are explicitly supplied.
- Keep `.claude/`, `AGENTS.md`, and `CLAUDE.md` unmodified unless the user separately asks to manage local agent instructions.

---

### Task 1: Scaffold Live Level 2 Entry Point And Scenario Metadata

**Files:**
- Create: `scripts/validate-gadd-level2-github.py`
- Create: `tests/level2/harness/__init__.py`
- Create: `tests/level2/scenarios/normal-product-flow.yml`
- Create: `tests/level2/scenarios/bug-gitnexus-flow.yml`
- Create: `tests/level2/scenarios/drift-reconciliation.yml`
- Create: `tests/level2/scenarios/pr-evidence-closure.yml`
- Create: `tests/level2/scenarios/handoff-resilience.yml`
- Modify: `.gitignore`

- [ ] **Step 1: Add the entrypoint**

Create `scripts/validate-gadd-level2-github.py`:

```python
#!/usr/bin/env python3
"""Run opt-in live GitHub-backed GADD Level 2 quality scenarios."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.level2.harness.run_level2 import main


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Add the harness package marker**

Create `tests/level2/harness/__init__.py`:

```python
"""Live GitHub-backed GADD Level 2 quality harness."""
```

- [ ] **Step 3: Add normal flow scenario metadata**

Create `tests/level2/scenarios/normal-product-flow.yml`:

```yaml
id: normal-product-flow
name: Normal product flow
requires:
  - issues
  - labels
  - sub_issues
  - repo_artifacts
quality_gates:
  - concise_prd_projection
  - repo_specific_sdd_projection
  - child_ticket_handoff
  - artifact_links
  - expected_labels
```

- [ ] **Step 4: Add bug GitNexus scenario metadata**

Create `tests/level2/scenarios/bug-gitnexus-flow.yml`:

```yaml
id: bug-gitnexus-flow
name: Bug triage with GitNexus
requires:
  - issues
  - comments
  - labels
  - gitnexus
quality_gates:
  - reproduction
  - gitnexus_evidence
  - route_decision
  - implementation_ready_or_precise_block
  - no_stale_gitnexus_claim
```

- [ ] **Step 5: Add drift scenario metadata**

Create `tests/level2/scenarios/drift-reconciliation.yml`:

```yaml
id: drift-reconciliation
name: Drift and reconciliation
requires:
  - issues
  - comments
  - labels
quality_gates:
  - body_drift_detected
  - comment_drift_detected
  - label_drift_detected
  - stale_update_blocked
  - reconciliation_action_clear
```

- [ ] **Step 6: Add PR evidence scenario metadata**

Create `tests/level2/scenarios/pr-evidence-closure.yml`:

```yaml
id: pr-evidence-closure
name: PR evidence and closure
requires:
  - pulls
  - branches
  - repo_artifacts
quality_gates:
  - pr_state_recorded
  - pr_not_treated_as_closure
  - verification_required_before_closure
  - closed_ticket_has_evidence
```

- [ ] **Step 7: Add handoff resilience scenario metadata**

Create `tests/level2/scenarios/handoff-resilience.yml`:

```yaml
id: handoff-resilience
name: Agent handoff resilience
requires:
  - issues
  - repo_artifacts
quality_gates:
  - ticket_has_canonical_artifact_path
  - artifact_contains_boundary
  - artifact_contains_acceptance_criteria
  - artifact_contains_verification
  - next_action_unambiguous
  - no_hidden_context_required
```

- [ ] **Step 8: Ignore generated run state**

Append this line to `.gitignore` if it is not already present:

```gitignore
tests/level2/.runs/
```

- [ ] **Step 9: Run syntax checks**

Run:

```sh
python3 -m py_compile scripts/validate-gadd-level2-github.py tests/level2/harness/__init__.py
```

Expected: no output and exit code `0`.

- [ ] **Step 10: Commit scaffold**

Run:

```sh
git add .gitignore scripts/validate-gadd-level2-github.py tests/level2/harness/__init__.py tests/level2/scenarios
git commit -m "test: scaffold live github level2 quality suite"
```

---

### Task 2: Implement Offline Ticket Quality Rubric

**Files:**
- Create: `tests/level2/harness/ticket_quality.py`
- Create: `tests/level2/harness/tests/test_ticket_quality.py`

- [ ] **Step 1: Write failing ticket quality tests**

Create `tests/level2/harness/tests/test_ticket_quality.py`:

```python
from tests.level2.harness.ticket_quality import Ticket, evaluate_ticket


def messages(findings):
    return [finding.message for finding in findings]


def test_closed_ticket_fails_with_unchecked_checklist():
    ticket = Ticket(
        role="PRD",
        title="PRD: CAD shared layer normalization",
        body=(
            "## Summary\nClear summary.\n\n"
            "## Boundary\nClear boundary.\n\n"
            "## Next Action\nReview linked SDD tickets.\n\n"
            "## GADD Trace\nRun: gadd-l2-test\nArtifact: gadd/work-items/CAD-PRD-1001/prd.md\n\n"
            "- [ ] The product boundary is clear.\n"
        ),
        state="closed",
        labels=["gadd-l2", "type:product-requirement"],
        comments=[],
    )

    assert "closed ticket has unchecked checklist items" in messages(evaluate_ticket(ticket))


def test_bug_ticket_fails_stale_gitnexus_missing_claim_when_evidence_exists():
    ticket = Ticket(
        role="Bug",
        title="Bug: whitespace-only layer names normalize to an empty key",
        body=(
            "## Observed Behavior\nnormalizeLayerName returns an empty string.\n\n"
            "## Expected Behavior\nReject whitespace-only names.\n\n"
            "## GADD Trace\nRun: gadd-l2-test\nArtifact: gadd/work-items/BUG-0001/triage.md\n\n"
            "GitNexus is not available in this test environment."
        ),
        state="open",
        labels=["gadd-l2", "type:bug"],
        comments=[],
        gitnexus_available=True,
    )

    assert "ticket claims GitNexus is missing while evidence is available" in messages(evaluate_ticket(ticket))


def test_concise_sdd_ticket_passes_with_artifact_and_next_action():
    ticket = Ticket(
        role="SDD",
        title="SDD: Product repo layer normalization",
        body=(
            "## Boundary\nProduct repo owns normalizeLayerName.\n\n"
            "## Files\n- cad.js\n- cad.test.js\n\n"
            "## Next Action\nReview the SDD and implementation evidence.\n\n"
            "## GADD Trace\nRun: gadd-l2-test\nArtifact: gadd/work-items/SDD-CAD-1001/sdd.md\n"
        ),
        state="open",
        labels=["gadd-l2", "type:engineering-change"],
        comments=[],
    )

    assert evaluate_ticket(ticket) == []
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:

```sh
python3 -m unittest tests.level2.harness.tests.test_ticket_quality -v
```

Expected: import failure because `tests.level2.harness.ticket_quality` does not exist.

- [ ] **Step 3: Implement ticket quality module**

Create `tests/level2/harness/ticket_quality.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
import re


ROLE_WORDS = {
    "PRD": ("prd", "product requirement"),
    "SDD": ("sdd", "design"),
    "Bug": ("bug",),
    "Child": ("child", "slice"),
    "Verification": ("verification",),
}

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(token|secret|password)\s*[:=]\s*[A-Za-z0-9_./-]{12,}"),
]


@dataclass(frozen=True)
class Ticket:
    role: str
    title: str
    body: str
    state: str
    labels: list[str]
    comments: list[str]
    gitnexus_available: bool = False
    max_words: int = 450


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    severity: str = "error"


def _has_heading(body: str, heading: str) -> bool:
    return re.search(rf"(?im)^##\s+{re.escape(heading)}\s*$", body) is not None


def _has_any_heading(body: str, headings: tuple[str, ...]) -> bool:
    return any(_has_heading(body, heading) for heading in headings)


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def _contains_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def _unchecked_checklist(body: str) -> bool:
    return re.search(r"(?m)^-\s+\[\s\]\s+", body) is not None


def _role_in_title(ticket: Ticket) -> bool:
    role_words = ROLE_WORDS.get(ticket.role, (ticket.role.lower(),))
    title = ticket.title.lower()
    return any(word in title for word in role_words)


def _has_trace(body: str) -> bool:
    return "gadd trace" in body.lower() and "artifact:" in body.lower()


def _has_next_action(body: str) -> bool:
    return _has_any_heading(body, ("Next Action", "Reviewer Focus", "Route Decision"))


def evaluate_ticket(ticket: Ticket) -> list[Finding]:
    findings: list[Finding] = []
    combined_text = "\n".join([ticket.body, *ticket.comments])

    if not ticket.title.strip() or not _role_in_title(ticket):
        findings.append(Finding("title-role", "title lacks clear ticket role"))
    if _word_count(ticket.body) > ticket.max_words:
        findings.append(Finding("body-too-long", "issue body exceeds configured word budget"))
    if not _has_trace(ticket.body):
        findings.append(Finding("missing-trace", "missing GADD trace with artifact reference"))
    if not _has_next_action(ticket.body):
        findings.append(Finding("missing-next-action", "missing next action or reviewer focus"))
    if "gadd-l2" not in ticket.labels:
        findings.append(Finding("missing-run-label", "missing gadd-l2 label"))
    if ticket.state.lower() == "closed" and _unchecked_checklist(ticket.body):
        findings.append(Finding("unchecked-closed", "closed ticket has unchecked checklist items"))
    if ticket.gitnexus_available and re.search(r"(?i)gitnexus\s+is\s+not\s+(currently\s+)?available|gitnexus\s+evidence:\s+missing", combined_text):
        findings.append(
            Finding(
                "stale-gitnexus",
                "ticket claims GitNexus is missing while evidence is available",
            )
        )
    if _contains_secret(combined_text):
        findings.append(Finding("secret-like-material", "ticket contains token-like or credential-like material"))

    if ticket.role in {"PRD", "SDD", "Child"} and not _has_any_heading(ticket.body, ("Boundary", "Scope", "Non-Goals")):
        findings.append(Finding("missing-boundary", "missing boundary or scope section"))
    if ticket.role == "Bug" and not _has_any_heading(ticket.body, ("Observed Behavior", "Reproduction")):
        findings.append(Finding("missing-reproduction", "bug ticket missing observed behavior or reproduction"))

    return findings
```

- [ ] **Step 4: Run ticket quality tests**

Run:

```sh
python3 -m unittest tests.level2.harness.tests.test_ticket_quality -v
```

Expected: 3 tests pass.

- [ ] **Step 5: Commit ticket quality module**

Run:

```sh
git add tests/level2/harness/ticket_quality.py tests/level2/harness/tests/test_ticket_quality.py
git commit -m "test: add level2 ticket quality rubric"
```

---

### Task 3: Implement Offline Artifact Quality Rubric

**Files:**
- Create: `tests/level2/harness/artifact_quality.py`
- Create: `tests/level2/harness/tests/test_artifact_quality.py`

- [ ] **Step 1: Write failing artifact quality tests**

Create `tests/level2/harness/tests/test_artifact_quality.py`:

```python
from pathlib import Path
import tempfile
import unittest

from tests.level2.harness.artifact_quality import ArtifactReference, evaluate_artifacts


class ArtifactQualityTests(unittest.TestCase):
    def test_missing_artifact_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            findings = evaluate_artifacts(
                Path(temp_dir),
                [ArtifactReference(path="gadd/work-items/BUG-0001/triage.md", kind="triage")],
            )
        self.assertEqual(["artifact path does not exist"], [finding.message for finding in findings])

    def test_thin_implementation_artifact_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "gadd/work-items/CHILD-1/work-item.md"
            path.parent.mkdir(parents=True)
            path.write_text("# Slice\n\nBuild the thing.\n", encoding="utf-8")
            findings = evaluate_artifacts(root, [ArtifactReference(path=str(path.relative_to(root)), kind="child")])
        self.assertIn("artifact missing acceptance criteria", [finding.message for finding in findings])

    def test_strong_triage_artifact_passes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "gadd/work-items/BUG-0001/triage.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "# Triage\n\n"
                "## Source\nGitHub issue.\n\n"
                "## Reproduction\n`npm test`\n\n"
                "## GitNexus Evidence\nnormalizeLayerName has one direct caller.\n\n"
                "## Route Decision\nready_for_implementation\n\n"
                "## Verification\nRun `npm test`.\n",
                encoding="utf-8",
            )
            findings = evaluate_artifacts(root, [ArtifactReference(path=str(path.relative_to(root)), kind="triage")])
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run artifact tests and verify they fail**

Run:

```sh
python3 -m unittest tests.level2.harness.tests.test_artifact_quality -v
```

Expected: import failure because `artifact_quality.py` does not exist.

- [ ] **Step 3: Implement artifact quality module**

Create `tests/level2/harness/artifact_quality.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class ArtifactReference:
    path: str
    kind: str


@dataclass(frozen=True)
class ArtifactFinding:
    path: str
    code: str
    message: str
    severity: str = "error"


REQUIRED_MARKERS = {
    "prd": ("acceptance", "non-goal"),
    "sdd": ("boundary", "verification"),
    "plan": ("task", "verification"),
    "triage": ("source", "reproduction", "gitnexus", "route decision", "verification"),
    "verification": ("command", "result"),
    "child": ("acceptance", "verification"),
}


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def evaluate_artifacts(repo_root: Path, references: list[ArtifactReference]) -> list[ArtifactFinding]:
    findings: list[ArtifactFinding] = []
    for reference in references:
        artifact_path = repo_root / reference.path
        if not artifact_path.is_file():
            findings.append(
                ArtifactFinding(
                    path=reference.path,
                    code="missing-artifact",
                    message="artifact path does not exist",
                )
            )
            continue

        text = artifact_path.read_text(encoding="utf-8")
        normalized = _normalized(text)
        for marker in REQUIRED_MARKERS.get(reference.kind, ()):
            if marker not in normalized:
                message = f"artifact missing {marker}"
                if marker == "acceptance":
                    message = "artifact missing acceptance criteria"
                findings.append(
                    ArtifactFinding(
                        path=reference.path,
                        code=f"missing-{marker.replace(' ', '-')}",
                        message=message,
                    )
                )
    return findings
```

- [ ] **Step 4: Run artifact quality tests**

Run:

```sh
python3 -m unittest tests.level2.harness.tests.test_artifact_quality -v
```

Expected: 3 tests pass.

- [ ] **Step 5: Commit artifact quality module**

Run:

```sh
git add tests/level2/harness/artifact_quality.py tests/level2/harness/tests/test_artifact_quality.py
git commit -m "test: add level2 artifact quality rubric"
```

---

### Task 4: Implement GitHub Client And Config Parsing

**Files:**
- Create: `tests/level2/harness/github_client.py`
- Create: `tests/level2/harness/run_level2.py`
- Create: `tests/level2/harness/tests/test_run_level2.py`

- [ ] **Step 1: Write failing config tests**

Create `tests/level2/harness/tests/test_run_level2.py`:

```python
import os
import unittest

from tests.level2.harness.run_level2 import Config, load_config


class RunLevel2ConfigTests(unittest.TestCase):
    def test_missing_live_env_skips_without_strict_mode(self):
        config = load_config(env={})
        self.assertTrue(config.skip_live)
        self.assertEqual("never", config.cleanup)

    def test_repo_ref_parses_owner_repo(self):
        config = load_config(
            env={
                "GADD_L2_GITHUB_REPO": "owner/repo",
                "GADD_L2_GITHUB_TOKEN": "token-value",
                "GADD_L2_PRODUCT_REPO_PATH": "/tmp/product",
                "GADD_L2_RENDER_REPO": "owner/render",
                "GADD_L2_RENDER_REPO_PATH": "/tmp/render",
            }
        )
        self.assertFalse(config.skip_live)
        self.assertEqual("owner", config.product_repo_owner)
        self.assertEqual("repo", config.product_repo_name)

    def test_invalid_cleanup_rejected(self):
        with self.assertRaises(ValueError):
            load_config(
                env={
                    "GADD_L2_GITHUB_REPO": "owner/repo",
                    "GADD_L2_GITHUB_TOKEN": "token-value",
                    "GADD_L2_CLEANUP": "sometimes",
                }
            )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run config tests and verify they fail**

Run:

```sh
python3 -m unittest tests.level2.harness.tests.test_run_level2 -v
```

Expected: import failure because `run_level2.py` does not exist.

- [ ] **Step 3: Implement GitHub client**

Create `tests/level2/harness/github_client.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
import json
import subprocess


class GitHubError(Exception):
    pass


@dataclass(frozen=True)
class RepoRef:
    owner: str
    repo: str

    @classmethod
    def parse(cls, value: str) -> "RepoRef":
        parts = value.split("/", 1)
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError("repository must use owner/repo format")
        return cls(owner=parts[0], repo=parts[1])

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.repo}"


class GitHubClient:
    def __init__(self, token: str):
        self.token = token

    def api(self, method: str, path: str, *fields: str) -> dict | list | None:
        command = ["gh", "api", "-X", method, path, *fields]
        env = {"GH_TOKEN": self.token}
        result = subprocess.run(command, text=True, capture_output=True, env=env, check=False)
        if result.returncode != 0:
            raise GitHubError(result.stderr.strip() or result.stdout.strip())
        text = result.stdout.strip()
        if not text:
            return None
        return json.loads(text)

    def get_issue(self, repo: RepoRef, number: int) -> dict:
        return self.api("GET", f"repos/{repo.full_name}/issues/{number}")

    def create_issue(self, repo: RepoRef, title: str, body: str, labels: list[str]) -> dict:
        fields = [f"-f=title={title}", f"-f=body={body}"]
        for label in labels:
            fields.append(f"-f=labels[]={label}")
        return self.api("POST", f"repos/{repo.full_name}/issues", *fields)

    def close_issue(self, repo: RepoRef, number: int, reason: str = "completed") -> dict:
        return self.api(
            "PATCH",
            f"repos/{repo.full_name}/issues/{number}",
            "-f=state=closed",
            f"-f=state_reason={reason}",
        )

    def add_comment(self, repo: RepoRef, number: int, body: str) -> dict:
        return self.api("POST", f"repos/{repo.full_name}/issues/{number}/comments", f"-f=body={body}")

    def list_comments(self, repo: RepoRef, number: int) -> list[dict]:
        value = self.api("GET", f"repos/{repo.full_name}/issues/{number}/comments?per_page=100")
        return value if isinstance(value, list) else []
```

- [ ] **Step 4: Implement config skeleton**

Create `tests/level2/harness/run_level2.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import os
import sys

from tests.level2.harness.github_client import RepoRef


ROOT = Path(__file__).resolve().parents[3]
RUNS_DIR = ROOT / "tests" / "level2" / ".runs"


@dataclass(frozen=True)
class Config:
    skip_live: bool
    product_repo: RepoRef | None
    product_repo_path: Path | None
    render_repo: RepoRef | None
    render_repo_path: Path | None
    token: str | None
    cleanup: str
    run_id: str

    @property
    def product_repo_owner(self) -> str | None:
        return self.product_repo.owner if self.product_repo else None

    @property
    def product_repo_name(self) -> str | None:
        return self.product_repo.repo if self.product_repo else None


def load_config(env: dict[str, str] | None = None) -> Config:
    values = dict(os.environ if env is None else env)
    cleanup = values.get("GADD_L2_CLEANUP", "never")
    if cleanup not in {"never", "success", "always"}:
        raise ValueError("GADD_L2_CLEANUP must be one of: never, success, always")

    repo_value = values.get("GADD_L2_GITHUB_REPO")
    token = values.get("GADD_L2_GITHUB_TOKEN")
    run_id = values.get("GADD_L2_RUN_ID", "gadd-l2-local")
    if not repo_value or not token:
        return Config(
            skip_live=True,
            product_repo=None,
            product_repo_path=None,
            render_repo=None,
            render_repo_path=None,
            token=None,
            cleanup=cleanup,
            run_id=run_id,
        )

    render_repo = RepoRef.parse(values["GADD_L2_RENDER_REPO"]) if values.get("GADD_L2_RENDER_REPO") else None
    render_path = Path(values["GADD_L2_RENDER_REPO_PATH"]) if values.get("GADD_L2_RENDER_REPO_PATH") else None
    return Config(
        skip_live=False,
        product_repo=RepoRef.parse(repo_value),
        product_repo_path=Path(values["GADD_L2_PRODUCT_REPO_PATH"]) if values.get("GADD_L2_PRODUCT_REPO_PATH") else None,
        render_repo=render_repo,
        render_repo_path=render_path,
        token=token,
        cleanup=cleanup,
        run_id=run_id,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run live GitHub-backed GADD Level 2 quality checks.")
    parser.add_argument("--audit-existing", action="store_true", help="Inspect existing sandbox tickets without creating new artifacts.")
    parser.add_argument("--strict", action="store_true", help="Fail instead of skipping when live GitHub env is missing.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        config = load_config()
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    if config.skip_live:
        message = "Skipping Level 2 GitHub tests: set GADD_L2_GITHUB_REPO and GADD_L2_GITHUB_TOKEN to run live checks."
        print(message)
        return 1 if args.strict else 0
    print(f"Level 2 GitHub config loaded for {config.product_repo.full_name}; run_id={config.run_id}")
    return 0
```

- [ ] **Step 5: Run config tests**

Run:

```sh
python3 -m unittest tests.level2.harness.tests.test_run_level2 -v
```

Expected: 3 tests pass.

- [ ] **Step 6: Run entrypoint without env**

Run:

```sh
python3 scripts/validate-gadd-level2-github.py
```

Expected:

```text
Skipping Level 2 GitHub tests: set GADD_L2_GITHUB_REPO and GADD_L2_GITHUB_TOKEN to run live checks.
```

- [ ] **Step 7: Commit GitHub client and config**

Run:

```sh
git add tests/level2/harness/github_client.py tests/level2/harness/run_level2.py tests/level2/harness/tests/test_run_level2.py
git commit -m "test: add level2 github client and config"
```

---

### Task 5: Implement Audit-Existing Mode

**Files:**
- Modify: `tests/level2/harness/run_level2.py`
- Modify: `tests/level2/harness/tests/test_run_level2.py`

- [ ] **Step 1: Add an audit result unit test**

Append to `tests/level2/harness/tests/test_run_level2.py`:

```python
from tests.level2.harness.run_level2 import summarize_findings


class FindingSummaryTests(unittest.TestCase):
    def test_summary_reports_error_count(self):
        findings = [
            {"target": "issue/1", "message": "missing gadd-l2 label"},
            {"target": "issue/2", "message": "closed ticket has unchecked checklist items"},
        ]
        self.assertEqual("2 quality findings", summarize_findings(findings))
```

- [ ] **Step 2: Run test and verify it fails**

Run:

```sh
python3 -m unittest tests.level2.harness.tests.test_run_level2 -v
```

Expected: import failure for `summarize_findings`.

- [ ] **Step 3: Add audit helpers to runner**

Add this code to `tests/level2/harness/run_level2.py` above `main`:

```python
from tests.level2.harness.ticket_quality import Ticket, evaluate_ticket


EXISTING_PRODUCT_ISSUES = (1, 2, 4)
EXISTING_RENDER_ISSUES = (1,)


def summarize_findings(findings: list[dict]) -> str:
    count = len(findings)
    if count == 0:
        return "0 quality findings"
    if count == 1:
        return "1 quality finding"
    return f"{count} quality findings"


def _ticket_from_issue(issue: dict, role: str, gitnexus_available: bool) -> Ticket:
    labels = [label["name"] if isinstance(label, dict) else str(label) for label in issue.get("labels", [])]
    comments = [comment.get("body", "") for comment in issue.get("comments", [])]
    return Ticket(
        role=role,
        title=issue.get("title", ""),
        body=issue.get("body") or "",
        state=issue.get("state", "open"),
        labels=labels,
        comments=comments,
        gitnexus_available=gitnexus_available,
    )


def audit_existing(config: Config, client) -> list[dict]:
    findings: list[dict] = []
    role_by_product_issue = {1: "PRD", 2: "SDD", 4: "Bug"}
    for number in EXISTING_PRODUCT_ISSUES:
        issue = client.get_issue(config.product_repo, number)
        issue["comments"] = client.list_comments(config.product_repo, number)
        ticket = _ticket_from_issue(issue, role_by_product_issue[number], gitnexus_available=True)
        for finding in evaluate_ticket(ticket):
            findings.append({"target": f"{config.product_repo.full_name}#{number}", "message": finding.message})
    if config.render_repo:
        for number in EXISTING_RENDER_ISSUES:
            issue = client.get_issue(config.render_repo, number)
            issue["comments"] = client.list_comments(config.render_repo, number)
            ticket = _ticket_from_issue(issue, "SDD", gitnexus_available=False)
            for finding in evaluate_ticket(ticket):
                findings.append({"target": f"{config.render_repo.full_name}#{number}", "message": finding.message})
    return findings
```

Update `main` after the `config.skip_live` block:

```python
    from tests.level2.harness.github_client import GitHubClient

    client = GitHubClient(config.token)
    if args.audit_existing:
        findings = audit_existing(config, client)
        for finding in findings:
            print(f"{finding['target']}: {finding['message']}", file=sys.stderr)
        print(summarize_findings(findings))
        return 1 if findings else 0
```

- [ ] **Step 4: Run offline tests**

Run:

```sh
python3 -m unittest tests.level2.harness.tests.test_run_level2 -v
```

Expected: 4 tests pass.

- [ ] **Step 5: Run audit against live sandbox**

Run:

```sh
GADD_L2_GITHUB_REPO=awjreynolds/gadd-cad-live-test-product \
GADD_L2_RENDER_REPO=awjreynolds/gadd-cad-live-test-render \
GADD_L2_GITHUB_TOKEN="$GITHUB_TOKEN" \
python3 scripts/validate-gadd-level2-github.py --audit-existing
```

Expected: non-zero exit while current sandbox tickets still have missing labels, unchecked closed checklist items, and stale GitNexus claims.

- [ ] **Step 6: Commit audit mode**

Run:

```sh
git add tests/level2/harness/run_level2.py tests/level2/harness/tests/test_run_level2.py
git commit -m "test: add level2 existing ticket audit"
```

---

### Task 6: Implement Live Scenario Creation And Manifest Writing

**Files:**
- Modify: `tests/level2/harness/run_level2.py`
- Create: `tests/level2/harness/gitnexus_evidence.py`

- [ ] **Step 1: Add GitNexus evidence representation**

Create `tests/level2/harness/gitnexus_evidence.py`:

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GitNexusEvidence:
    symbol: str
    file_path: str
    direct_callers: list[str]
    risk: str
    summary: str

    def to_markdown(self) -> str:
        callers = ", ".join(self.direct_callers) if self.direct_callers else "none detected"
        return (
            "## GitNexus Evidence\n\n"
            f"- Symbol: `{self.symbol}`\n"
            f"- File: `{self.file_path}`\n"
            f"- Direct callers: {callers}\n"
            f"- Risk: {self.risk}\n"
            f"- Summary: {self.summary}\n"
        )
```

- [ ] **Step 2: Add manifest helpers to runner**

Add to `tests/level2/harness/run_level2.py`:

```python
import json
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def manifest_path(run_id: str) -> Path:
    return RUNS_DIR / run_id / "manifest.json"


def write_manifest(run_id: str, manifest: dict) -> None:
    path = manifest_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
```

- [ ] **Step 3: Add issue body builders**

Add to `tests/level2/harness/run_level2.py`:

```python
def trace_block(run_id: str, artifact: str) -> str:
    return f"## GADD Trace\n\nRun: {run_id}\nArtifact: {artifact}\n"


def normal_prd_body(run_id: str) -> str:
    return (
        "## Summary\nValidate concise GitHub handoff for shared CAD layer normalization.\n\n"
        "## Boundary\nProduct rule: trim layer names, lowercase them, and use the normalized value for comparison.\n\n"
        "## Non-Goals\nNo parser, renderer rewrite, credential, or migration work.\n\n"
        "## Repository Ownership\nProduct repo owns authoring behavior. Render repo owns render lookup behavior.\n\n"
        "## Next Action\nReview the linked repo-specific SDD tickets.\n\n"
        f"{trace_block(run_id, 'gadd/work-items/CAD-PRD-1001/prd.md')}"
    )


def product_sdd_body(run_id: str) -> str:
    return (
        "## Boundary\nProduct repo owns `normalizeLayerName` behavior.\n\n"
        "## Files\n- `cad.js`\n- `cad.test.js`\n\n"
        "## Next Action\nReview implementation evidence and run `npm test`.\n\n"
        f"{trace_block(run_id, 'gadd/work-items/SDD-CAD-1001/sdd.md')}"
    )


def bug_body(run_id: str, evidence_markdown: str) -> str:
    return (
        "## Observed Behavior\n`normalizeLayerName(\"   \")` returns an empty key.\n\n"
        "## Expected Behavior\nWhitespace-only layer names are rejected or represented explicitly before comparison.\n\n"
        "## Reproduction\n`node -e \"import('./cad.js').then(({normalizeLayerName}) => console.log(JSON.stringify(normalizeLayerName('   '))))\"`\n\n"
        f"{evidence_markdown}\n"
        "## Route Decision\nready_for_implementation with GitNexus evidence.\n\n"
        "## Next Action\nImplement the behavior with a failing test first, then run `npm test`.\n\n"
        f"{trace_block(run_id, 'gadd/work-items/BUG-0001-whitespace-layer-name/triage.md')}"
    )
```

- [ ] **Step 4: Add live scenario runner**

Add to `tests/level2/harness/run_level2.py`:

```python
from tests.level2.harness.gitnexus_evidence import GitNexusEvidence


def run_live_scenarios(config: Config, client) -> dict:
    labels = ["gadd-l2", f"gadd-l2:{config.run_id}"]
    evidence = GitNexusEvidence(
        symbol="normalizeLayerName",
        file_path="cad.js",
        direct_callers=["cad.test.js"],
        risk="low",
        summary="Single exported normalization function with direct test coverage.",
    )
    prd = client.create_issue(
        config.product_repo,
        f"[GADD L2 {config.run_id}] PRD: CAD shared layer normalization",
        normal_prd_body(config.run_id),
        labels + ["type:product-requirement"],
    )
    product_sdd = client.create_issue(
        config.product_repo,
        f"[GADD L2 {config.run_id}] SDD: Product repo layer normalization",
        product_sdd_body(config.run_id),
        labels + ["type:engineering-change"],
    )
    bug = client.create_issue(
        config.product_repo,
        f"[GADD L2 {config.run_id}] Bug: whitespace-only layer names normalize to an empty key",
        bug_body(config.run_id, evidence.to_markdown()),
        labels + ["type:bug"],
    )
    manifest = {
        "run_id": config.run_id,
        "created_at": utc_now(),
        "issues": [
            {"repo": config.product_repo.full_name, "number": prd["number"], "role": "PRD", "url": prd["html_url"]},
            {"repo": config.product_repo.full_name, "number": product_sdd["number"], "role": "SDD", "url": product_sdd["html_url"]},
            {"repo": config.product_repo.full_name, "number": bug["number"], "role": "Bug", "url": bug["html_url"]},
        ],
        "status": "created",
    }
    write_manifest(config.run_id, manifest)
    return manifest
```

Update `main` after `audit_existing` handling:

```python
    manifest = run_live_scenarios(config, client)
    print(f"GADD Level 2 GitHub scenarios created for run {config.run_id}")
    print(f"Manifest: {manifest_path(config.run_id)}")
    return 0
```

- [ ] **Step 5: Run offline tests**

Run:

```sh
python3 -m unittest discover tests/level2/harness/tests -v
```

Expected: all offline harness tests pass.

- [ ] **Step 6: Run live creation against sandbox**

Run:

```sh
GADD_L2_GITHUB_REPO=awjreynolds/gadd-cad-live-test-product \
GADD_L2_RENDER_REPO=awjreynolds/gadd-cad-live-test-render \
GADD_L2_GITHUB_TOKEN="$GITHUB_TOKEN" \
GADD_L2_RUN_ID="gadd-l2-manual-$(date +%Y%m%d%H%M%S)" \
python3 scripts/validate-gadd-level2-github.py
```

Expected: creates run-marked PRD, SDD, and bug issues, writes `tests/level2/.runs/<run-id>/manifest.json`, and prints the manifest path.

- [ ] **Step 7: Commit live scenario creation**

Run:

```sh
git add tests/level2/harness/run_level2.py tests/level2/harness/gitnexus_evidence.py
git commit -m "test: create live level2 github quality scenarios"
```

---

### Task 7: Evaluate Newly Created Live Tickets

**Files:**
- Modify: `tests/level2/harness/run_level2.py`
- Modify: `tests/level2/harness/tests/test_run_level2.py`

- [ ] **Step 1: Add quality assertion helper test**

Append to `tests/level2/harness/tests/test_run_level2.py`:

```python
from tests.level2.harness.run_level2 import fail_on_quality_findings


class QualityFailureTests(unittest.TestCase):
    def test_fail_on_quality_findings_returns_one(self):
        self.assertEqual(1, fail_on_quality_findings([{"target": "issue/1", "message": "missing label"}]))

    def test_fail_on_quality_findings_returns_zero_without_findings(self):
        self.assertEqual(0, fail_on_quality_findings([]))
```

- [ ] **Step 2: Run test and verify it fails**

Run:

```sh
python3 -m unittest tests.level2.harness.tests.test_run_level2 -v
```

Expected: import failure for `fail_on_quality_findings`.

- [ ] **Step 3: Add quality evaluation for manifest issues**

Add to `tests/level2/harness/run_level2.py`:

```python
def fail_on_quality_findings(findings: list[dict]) -> int:
    return 1 if findings else 0


def evaluate_manifest_issues(config: Config, client, manifest: dict) -> list[dict]:
    findings: list[dict] = []
    for item in manifest.get("issues", []):
        repo = RepoRef.parse(item["repo"])
        issue = client.get_issue(repo, int(item["number"]))
        issue["comments"] = client.list_comments(repo, int(item["number"]))
        ticket = _ticket_from_issue(issue, item["role"], gitnexus_available=item["role"] == "Bug")
        for finding in evaluate_ticket(ticket):
            findings.append({"target": f"{repo.full_name}#{item['number']}", "message": finding.message})
    return findings
```

Update the live scenario branch in `main`:

```python
    manifest = run_live_scenarios(config, client)
    findings = evaluate_manifest_issues(config, client, manifest)
    manifest["quality_findings"] = findings
    manifest["status"] = "failed" if findings else "passed"
    write_manifest(config.run_id, manifest)
    for finding in findings:
        print(f"{finding['target']}: {finding['message']}", file=sys.stderr)
    print(f"GADD Level 2 GitHub scenarios evaluated for run {config.run_id}: {summarize_findings(findings)}")
    print(f"Manifest: {manifest_path(config.run_id)}")
    return fail_on_quality_findings(findings)
```

- [ ] **Step 4: Run offline tests**

Run:

```sh
python3 -m unittest discover tests/level2/harness/tests -v
```

Expected: all offline harness tests pass.

- [ ] **Step 5: Run live creation and evaluation**

Run:

```sh
GADD_L2_GITHUB_REPO=awjreynolds/gadd-cad-live-test-product \
GADD_L2_RENDER_REPO=awjreynolds/gadd-cad-live-test-render \
GADD_L2_GITHUB_TOKEN="$GITHUB_TOKEN" \
GADD_L2_RUN_ID="gadd-l2-manual-$(date +%Y%m%d%H%M%S)" \
python3 scripts/validate-gadd-level2-github.py
```

Expected: exit code reflects ticket quality findings. The initial implementation should pass for generated tickets and fail only if the rubric catches a real issue in the generated bodies.

- [ ] **Step 6: Commit live quality evaluation**

Run:

```sh
git add tests/level2/harness/run_level2.py tests/level2/harness/tests/test_run_level2.py
git commit -m "test: gate live level2 tickets on quality"
```

---

### Task 8: Implement Cleanup Tool

**Files:**
- Create: `tests/level2/harness/cleanup_level2.py`
- Modify: `tests/level2/harness/run_level2.py`

- [ ] **Step 1: Create cleanup script**

Create `tests/level2/harness/cleanup_level2.py`:

```python
#!/usr/bin/env python3
"""Clean up run-marked GADD Level 2 GitHub artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from tests.level2.harness.github_client import GitHubClient, RepoRef
from tests.level2.harness.run_level2 import load_config, manifest_path, utc_now, write_manifest


def cleanup_run(run_id: str) -> int:
    config = load_config()
    if config.skip_live:
        print("Cannot clean up without GADD_L2_GITHUB_REPO and GADD_L2_GITHUB_TOKEN.", file=sys.stderr)
        return 2
    path = manifest_path(run_id)
    if not path.is_file():
        print(f"Missing manifest: {path}", file=sys.stderr)
        return 2
    manifest = json.loads(path.read_text(encoding="utf-8"))
    client = GitHubClient(config.token)
    closed = []
    for issue in manifest.get("issues", []):
        repo = RepoRef.parse(issue["repo"])
        number = int(issue["number"])
        live = client.get_issue(repo, number)
        labels = [label["name"] for label in live.get("labels", [])]
        if "gadd-l2" not in labels or f"gadd-l2:{run_id}" not in labels:
            print(f"Refusing to clean unmarked issue {repo.full_name}#{number}", file=sys.stderr)
            return 1
        client.close_issue(repo, number)
        closed.append({"repo": repo.full_name, "number": number})
    manifest["cleanup"] = {"status": "closed_issues", "at": utc_now(), "closed": closed}
    write_manifest(run_id, manifest)
    print(f"Cleaned GADD Level 2 run {run_id}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args(argv)
    return cleanup_run(args.run_id)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Add cleanup-on-success hook**

In `tests/level2/harness/run_level2.py`, before returning from live scenario evaluation, add:

```python
    if config.cleanup in {"success", "always"} and not findings:
        from tests.level2.harness.cleanup_level2 import cleanup_run

        cleanup_run(config.run_id)
```

- [ ] **Step 3: Run syntax checks**

Run:

```sh
python3 -m py_compile tests/level2/harness/cleanup_level2.py tests/level2/harness/run_level2.py
```

Expected: no output and exit code `0`.

- [ ] **Step 4: Run cleanup against a live run**

Run:

```sh
GADD_L2_GITHUB_REPO=awjreynolds/gadd-cad-live-test-product \
GADD_L2_GITHUB_TOKEN="$GITHUB_TOKEN" \
python3 tests/level2/harness/cleanup_level2.py --run-id <run-id>
```

Expected: closes only issues carrying both `gadd-l2` and `gadd-l2:<run-id>`.

- [ ] **Step 5: Commit cleanup**

Run:

```sh
git add tests/level2/harness/cleanup_level2.py tests/level2/harness/run_level2.py
git commit -m "test: add level2 github cleanup"
```

---

### Task 9: Implement Skill Refresh Command Helper

**Files:**
- Create: `tests/level2/harness/skill_refresh.py`

- [ ] **Step 1: Create skill refresh helper**

Create `tests/level2/harness/skill_refresh.py`:

```python
#!/usr/bin/env python3
"""Print or execute the GADD skill push and sandbox reinstall loop commands."""

from __future__ import annotations

import argparse
import subprocess
import sys


COMMANDS = [
    ["git", "push"],
    ["npx", "skills", "add", "awjreynolds/gadd", "--all", "-y"],
]


def format_commands() -> str:
    return "\n".join(" ".join(command) for command in COMMANDS)


def run_commands() -> int:
    for command in COMMANDS:
        result = subprocess.run(command, check=False)
        if result.returncode != 0:
            return result.returncode
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Run commands instead of printing them.")
    args = parser.parse_args(argv)
    if not args.execute:
        print(format_commands())
        return 0
    return run_commands()


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run helper in print mode**

Run:

```sh
python3 tests/level2/harness/skill_refresh.py
```

Expected:

```text
git push
npx skills add awjreynolds/gadd --all -y
```

- [ ] **Step 3: Commit skill refresh helper**

Run:

```sh
git add tests/level2/harness/skill_refresh.py
git commit -m "test: add level2 skill refresh helper"
```

---

### Task 10: Update Documentation And Final Validation

**Files:**
- Modify: `tests/level2/README.md`

- [ ] **Step 1: Replace README with live suite documentation**

Update `tests/level2/README.md` to include:

```markdown
# GADD Level 2 Tests

Level 2 has two parts:

- `fixture-next`: offline smoke coverage for deterministic `/gadd:next` routing.
- live GitHub quality suite: opt-in checks for GitHub ticket mechanics, ticket quality, artifact quality, drift handling, PR evidence, and agent handoff resilience.

## Offline Smoke

```sh
python3 scripts/run-gadd-level2.py --runner fixture-next
```

## Live GitHub Quality Suite

Required:

```sh
GADD_L2_GITHUB_REPO=owner/product-sandbox
GADD_L2_GITHUB_TOKEN=...
```

Recommended for multi-repo checks:

```sh
GADD_L2_RENDER_REPO=owner/render-sandbox
GADD_L2_PRODUCT_REPO_PATH=/path/to/product/repo
GADD_L2_RENDER_REPO_PATH=/path/to/render/repo
```

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

## Skill Hardening Loop

1. Run `--audit-existing`.
2. Run live Level 2 creation.
3. Fix GADD skills and templates.
4. Push the skill package.
5. Reinstall skills into sandbox repositories.
6. Rerun until ticket and artifact quality pass.
```

- [ ] **Step 2: Run all offline validation**

Run:

```sh
python3 -m unittest discover tests/level2/harness/tests -v
python3 scripts/run-gadd-level2.py --runner fixture-next
python3 scripts/validate-gadd-level1.py
python3 scripts/validate-gadd-level2-github.py
```

Expected:

- offline harness tests pass,
- fixture-next validates 1 scenario,
- Level 1 validates all scenarios,
- live GitHub entrypoint skips without env vars and exits 0.

- [ ] **Step 3: Run full MVP validation**

Run:

```sh
./scripts/validate-gadd-mvp.sh
```

Expected: pass.

- [ ] **Step 4: Run live audit and live creation**

Run:

```sh
GADD_L2_GITHUB_REPO=awjreynolds/gadd-cad-live-test-product \
GADD_L2_RENDER_REPO=awjreynolds/gadd-cad-live-test-render \
GADD_L2_GITHUB_TOKEN="$GITHUB_TOKEN" \
python3 scripts/validate-gadd-level2-github.py --audit-existing
```

Expected: current existing tickets produce quality findings until the skills/templates and existing artifacts are hardened.

Run:

```sh
GADD_L2_GITHUB_REPO=awjreynolds/gadd-cad-live-test-product \
GADD_L2_RENDER_REPO=awjreynolds/gadd-cad-live-test-render \
GADD_L2_GITHUB_TOKEN="$GITHUB_TOKEN" \
GADD_L2_RUN_ID="gadd-l2-manual-$(date +%Y%m%d%H%M%S)" \
python3 scripts/validate-gadd-level2-github.py
```

Expected: creates run-marked tickets, evaluates them, and writes a manifest.

- [ ] **Step 5: Run GitNexus change detection**

Run:

```text
gitnexus_detect_changes(scope="all", repo="gadd")
```

Expected: affected symbols and processes match the Level 2 harness/documentation changes.

- [ ] **Step 6: Commit final docs and validation polish**

Run:

```sh
git add tests/level2/README.md
git commit -m "docs: document level2 ticket quality suite"
```

---

## Plan Self-Review

- Spec coverage: Tasks cover live suite scaffold, ticket rubric, artifact rubric, GitHub API access, audit-existing, live creation, quality gating, cleanup, skill refresh, docs, and validation.
- Placeholder scan: This plan uses concrete files, commands, code snippets, expected outputs, and commit messages. It does not include deferred implementation markers.
- Type consistency: `Ticket`, `Finding`, `ArtifactReference`, `ArtifactFinding`, `RepoRef`, `GitHubClient`, `Config`, `GitNexusEvidence`, and runner helper names are introduced before later tasks use them.
- Scope check: The plan implements the harness and hardening loop. Actual skill prompt/template improvements are intentionally driven by findings from the new suite after it exists.
