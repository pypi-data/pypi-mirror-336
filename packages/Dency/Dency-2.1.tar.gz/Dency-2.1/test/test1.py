import unittest
from dependency_fetcher.core import resolve_versions

class TestDependencyFetcher(unittest.TestCase):
    def test_resolve_versions(self):
        dependencies = {"requests"}
        resolved = resolve_versions(dependencies)
        self.assertIn("requests", resolved)
        self.assertTrue(resolved["requests"])

if __name__ == '__main__':
    unittest.main()
