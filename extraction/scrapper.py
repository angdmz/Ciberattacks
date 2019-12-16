import logging
from os import listdir
from os.path import isfile, join

import git

from extraction.extractor import DataExtractor

logger = logging.getLogger(__name__)

class RepoScrapper(object):

    data_extractor = DataExtractor()

    def scrap(self, url, path, directory_to_scrap, target):
        logger.info("Cloning {} repo...".format(url))
        try:
            git.repo.Repo.clone_from(url, path)

            onlyfiles = [f for f in listdir(directory_to_scrap) if isfile(join(directory_to_scrap, f))]
            data = []
            logger.info("Iterating files in {}".format(directory_to_scrap))
            for file_name in onlyfiles:
                with open(directory_to_scrap + "/" + file_name, 'r') as f:
                    data.append(self.data_extractor.extract(f.read(), target))
        except Exception as e:
            logger.critical("Error during processing: {}".format(str(e)))

        return data