__author__ = 'xudshen@hotmail.com'
import os
import logging

logging.basicConfig(level=logging.INFO)


class ForestPreprocessor:
    """find all .json and parse"""

    def __init__(self, path):
        self.__source_path = []
        self.__suffix = ".json"

        if os.path.exists(path):
            logging.info("walking the path...")
            if os.path.isfile(path):
                if path.endswith(self.__suffix):
                    self.__source_path.append(path)
            else:
                for root, dirs, files in os.walk(path, topdown=False):
                    [self.__source_path.append(os.path.join(root, name)) for name in files
                     if name.endswith(self.__suffix)]
        logging.info(self.__source_path)


if __name__ == "__main__":
    ForestPreprocessor("examples")
    ForestPreprocessor("examples/api/")
    ForestPreprocessor("examples/api/meta.api.json")
