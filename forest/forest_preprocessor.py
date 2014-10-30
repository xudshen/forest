__author__ = 'xudshen@hotmail.com'

from forest.logger import log_d
from forest.forest_source import ForestSource, ForestSourceFactory


class AbsPreprocessor(object):
    """abstract preprocessor"""

    def __init__(self, key):
        self.__key = key

    def process(self, obj):
        raise NotImplementedError("not implement")

    def key(self):
        return self.__key


class SourcePreprocessor(AbsPreprocessor):
    def __init__(self):
        super().__init__("sources")

    def process(self, obj):
        # process the source type
        # add it to the source factory
        [ForestSourceFactory.add(item["id"],
                                 ForestSource(item["id"], item["url"], item["method"], item["headers"], item["body"],
                                              item["type"])) for item in obj if "id" in item and len(item["id"]) > 0]


class ModelPreprocessor(AbsPreprocessor):
    def __init__(self):
        super().__init__("models")

    def process(self, obj):
        log_d(obj)


class ControllerPreprocessor(AbsPreprocessor):
    def __init__(self):
        super().__init__("controllers")

    def process(self, obj):
        log_d(obj)
