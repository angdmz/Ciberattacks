from unittest import TestCase

from extraction.scrapper import RepoScrapper


class TestScrapper(TestCase):
    def setUp(self):
        self.repo_url = 'https://github.com/mitre/cti'
        self.repo_path = "/repo"
        self.directory = self.repo_path + '/enterprise-attack/attack-pattern'
        self.scrapper = RepoScrapper()
        self.target = ["id", "objects[0].name", "objects[0].kill_chain_phases"]

    def test_simple_extraction(self):
        content = self.scrapper.scrap(self.repo_url, self.repo_path, self.directory, self.target)
        for c in content:
            self.assertIn("id", c)
            self.assertIn("objects[0].name", c)
            self.assertIn("objects[0].kill_chain_phases", c)
