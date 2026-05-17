import unittest

from tests.level2.harness.run_level2 import load_config


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
