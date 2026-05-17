import unittest

from tests.level3.harness.github_tracker import GitHubTracker, GitHubTrackerConfig, load_github_tracker_config
from tests.level3.harness.local_tracker import LocalIssue


class FakeGitHubClient:
    def __init__(self):
        self.labels = []
        self.issues = []

    def ensure_label(self, repo, label):
        self.labels.append((repo.full_name, label))

    def create_issue(self, repo, title, body, labels):
        self.issues.append((repo.full_name, title, body, labels))
        return {"number": 7, "state": "open", "title": title, "body": body, "labels": [{"name": label} for label in labels]}


class GitHubTrackerConfigTests(unittest.TestCase):
    def test_missing_repo_skips_without_strict_mode(self):
        config = load_github_tracker_config(env={}, run_id="gadd-l3-test", strict=False)

        self.assertTrue(config.skip_live)

    def test_missing_repo_fails_with_strict_mode(self):
        with self.assertRaises(ValueError):
            load_github_tracker_config(env={}, run_id="gadd-l3-test", strict=True)


class GitHubTrackerTests(unittest.TestCase):
    def test_create_issue_adds_run_labels(self):
        config = GitHubTrackerConfig.from_repo_name("owner/repo", run_id="gadd-l3-test", token=None)
        client = FakeGitHubClient()
        tracker = GitHubTracker(config, client=client)

        issue = tracker.create_issue(
            LocalIssue(
                role="Child",
                title="Child: Normalize product layer names",
                body="## Next Action\nImplement with a failing test first.\n",
                labels=["type:task"],
            )
        )

        self.assertEqual(7, issue.number)
        self.assertIn(("owner/repo", "gadd-l3"), client.labels)
        self.assertIn(("owner/repo", "gadd-l3:gadd-l3-test"), client.labels)
        self.assertEqual(["type:task", "gadd-l3", "gadd-l3:gadd-l3-test"], client.issues[0][3])
        self.assertEqual([7], [issue.number for issue in tracker.list_issues()])


if __name__ == "__main__":
    unittest.main()
