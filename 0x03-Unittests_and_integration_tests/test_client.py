#!/usr/bin/env python3
""" unittests"""


import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct org data."""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url returns correct URL."""
        mock_org.return_value = {"repos_url": "https://api.github.com/repos"}
        client = GithubOrgClient("test")
        self.assertEqual(client._public_repos_url, "https://api.github.com/repos")

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """Test public_repos returns correct list of repos."""
        mock_public_repos_url.return_value = "https://api.github.com/repos"
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("https://api.github.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean for given repo license."""
        client = GithubOrgClient("test")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload,
     "expected_repos": expected_repos, "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    @patch("client.requests.get")
    def setUpClass(cls, mock_get):
        """Setup class with mock responses for HTTP requests."""
        cls.get_patcher = patch("client.requests.get", side_effect=lambda url: Mock(json=lambda: {
            f"https://api.github.com/orgs/test": cls.org_payload,
            f"https://api.github.com/orgs/test/repos": cls.repos_payload
        }[url]))
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down class by stopping patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test GithubOrgClient.public_repos returns correct repos list."""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos only returns repos with specified license."""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
