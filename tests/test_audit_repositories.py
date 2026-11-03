import unittest
from unittest.mock import patch

import scripts.audit_repositories as audit


class RepositoryDiscoveryTests(unittest.TestCase):
    def test_discovery_paginates_and_unions_fallback(self):
        first_page = [{"full_name": f"owner/repo-{index}"} for index in range(100)]
        second_page = [{"full_name": "owner/repo-extra"}]

        with patch.object(
            audit,
            "request",
            side_effect=[(200, first_page), (200, second_page)],
        ):
            repositories = audit.discover_repositories(
                ["owner/repo-0", "owner/fallback"]
            )

        self.assertEqual(len(repositories), 102)
        self.assertIn("owner/repo-extra", repositories)
        self.assertIn("owner/fallback", repositories)
        self.assertEqual(repositories, sorted(repositories, key=str.casefold))

    def test_discovery_fails_closed_when_a_page_is_blocked(self):
        with patch.object(audit, "request", return_value=(403, {"message": "forbidden"})):
            with self.assertRaisesRegex(RuntimeError, "HTTP 403"):
                audit.discover_repositories([])


class RepositoryPathTests(unittest.TestCase):
    def test_missing_path_is_not_reported_as_a_missing_repository(self):
        with patch.object(audit, "request", return_value=(404, {"message": "not visible"})):
            result = audit.check_path("owner/repo", "README.md", "main")

        self.assertEqual(result["status"], "ABSENT_OR_NOT_VISIBLE")

    def test_forbidden_path_is_reported_as_blocked(self):
        with patch.object(audit, "request", return_value=(403, {"message": "forbidden"})):
            result = audit.check_path("owner/repo", "README.md", "main")

        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["http_status"], 403)


class RepositoryAuditTests(unittest.TestCase):
    def test_inaccessible_repository_is_not_reported_as_pass(self):
        with patch.object(audit, "request", return_value=(404, {"message": "not visible"})):
            result = audit.audit("owner/repo")

        self.assertEqual(result["status"], "NOT_FOUND_OR_NOT_VISIBLE")
        self.assertEqual(result["http_status"], 404)


if __name__ == "__main__":
    unittest.main()
