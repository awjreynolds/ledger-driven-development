from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Protocol

from tests.level2.harness.github_client import GitHubClient, RepoRef
from tests.level3.harness.local_tracker import LocalIssue


class GitHubIssueClient(Protocol):
    def ensure_label(self, repo: RepoRef, label: str) -> None:
        """Ensure a label exists in the configured repository."""

    def create_issue(self, repo: RepoRef, title: str, body: str, labels: list[str]) -> dict:
        """Create an issue and return the GitHub API response."""


@dataclass(frozen=True)
class GitHubTrackerConfig:
    skip_live: bool
    repo: RepoRef | None
    token: str | None
    run_id: str

    @classmethod
    def from_repo_name(cls, repo_name: str, run_id: str, token: str | None) -> "GitHubTrackerConfig":
        return cls(skip_live=False, repo=RepoRef.parse(repo_name), token=token, run_id=run_id)


def load_github_tracker_config(
    env: dict[str, str] | None,
    run_id: str,
    strict: bool,
) -> GitHubTrackerConfig:
    values = dict(os.environ if env is None else env)
    repo_name = values.get("GADD_L3_GITHUB_REPO") or values.get("GADD_L2_GITHUB_REPO")
    token = values.get("GADD_L3_GITHUB_TOKEN") or values.get("GADD_L2_GITHUB_TOKEN")
    if not repo_name:
        if strict:
            raise ValueError("GADD_L3_GITHUB_REPO or GADD_L2_GITHUB_REPO is required for strict GitHub tracker mode")
        return GitHubTrackerConfig(skip_live=True, repo=None, token=token, run_id=run_id)
    return GitHubTrackerConfig.from_repo_name(repo_name, run_id=run_id, token=token)


class GitHubTracker:
    def __init__(self, config: GitHubTrackerConfig, client: GitHubIssueClient | None = None) -> None:
        if config.repo is None:
            raise ValueError("GitHub tracker requires a configured repo")
        self.config = config
        self.repo = config.repo
        self.client = client or GitHubClient(config.token)
        self._created: list[LocalIssue] = []

    def create_issue(self, issue: LocalIssue) -> LocalIssue:
        labels = self._managed_labels(issue.labels)
        for label in labels:
            self.client.ensure_label(self.repo, label)
        created = self.client.create_issue(self.repo, issue.title, issue.body, labels)
        stored = LocalIssue(
            role=issue.role,
            title=str(created.get("title", issue.title)),
            body=str(created.get("body", issue.body) or ""),
            labels=_labels_from_response(created, fallback=labels),
            state=str(created.get("state", issue.state)),
            number=int(created["number"]),
        )
        self._created.append(stored)
        return stored

    def list_issues(self) -> list[LocalIssue]:
        return list(self._created)

    def _managed_labels(self, labels: list[str]) -> list[str]:
        managed = ["gadd-l3", f"gadd-l3:{self.config.run_id}"]
        result = list(labels)
        for label in managed:
            if label not in result:
                result.append(label)
        return result


def _labels_from_response(response: dict, fallback: list[str]) -> list[str]:
    raw_labels = response.get("labels")
    if not raw_labels:
        return fallback
    labels = []
    for label in raw_labels:
        labels.append(str(label["name"] if isinstance(label, dict) else label))
    return labels
