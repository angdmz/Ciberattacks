import os

from extraction.scrapper import RepoScrapper
from extraction.extractor import DataExtractor

url = os.getenv('REMOTE_REPO', 'https://github.com/mitre/cti')
clone_directory = os.getenv('CLONE_DIRECTORY', '/repo')
path_to_scrap = os.getenv('PATH_TO_SCRAP', '/enterprise-attack/attack-pattern')
target = ["id", "objects[0].name", "objects[0].kill_chain_phases"]

scrapper = RepoScrapper()
print(scrapper.scrap(url, clone_directory, clone_directory + path_to_scrap, target))