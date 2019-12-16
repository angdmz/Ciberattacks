from unittest import TestCase

import requests

from extraction.extractor import DataExtractor


class RepoScrapper(object):
    def scrap(self, url):
        return requests.get(url)


class TestScrapper(TestCase):
    def setUp(self):
        self.url = 'https://github.com/mitre/cti/enterprise-attack/attack-pattern'
        self.scrapper = RepoScrapper()

    def test_simple_extraction(self):
        content = self.scrapper.scrap(self.url)
