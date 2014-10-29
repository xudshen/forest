__author__ = 'xudshen@hotmail.com'
import os
import json

from forest.logger import log_i
from forest.preprocessor import AbsPreprocessor


class Processor(object):
    """find all .json and parse"""

    def __init__(self, path):
        self.__config_path = []
        self.__suffix = ".json"

        if os.path.exists(path):
            # find all the json file under this path
            log_i("walking the path...")
            if os.path.isfile(path):
                if path.endswith(self.__suffix):
                    self.__config_path.append(path)
            else:
                for root, dirs, files in os.walk(path, topdown=False):
                    [self.__config_path.append(os.path.join(root, name))
                     for name in files if name.endswith(self.__suffix)]
        log_i("all the config paths:", self.__config_path)

        # prepare all the processors
        self.__preprocessors = {}
        for cls in AbsPreprocessor.__subclasses__():
            ins = cls()
            self.__preprocessors[ins.key()] = ins
        log_i("all the preprocessors:", self.__preprocessors)

    def process(self):
        for file in self.__config_path:
            log_i(">>processing" + file)
            with open(file) as content:
                j = json.load(content)
                for key in j:
                    if key in self.__preprocessors:
                        self.__preprocessors[key].process(j[key])


if __name__ == "__main__":
    processor = Processor("examples")
    processor.process()
