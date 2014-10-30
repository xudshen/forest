__author__ = 'xudshen@hotmail.com'

from forest.forest_factory import ForestAbsFactory
from forest.forest_source import ForestSourceFactory
from forest.forest_model import ForestModelFactory
from forest.forest_controller import ForestControllerFactory


class AbsPreprocessor(object):
    """abstract preprocessor"""

    def __init__(self, key, factory_cls):
        self.__key = key
        self.__factory_cls = factory_cls

    def process(self, obj):
        if self.__factory_cls is not None and issubclass(self.__factory_cls, ForestAbsFactory):
            [self.__factory_cls.add(item["id"], item) for item in obj if "id" in item and len(item["id"]) > 0]

    def key(self):
        return self.__key


class SourcePreprocessor(AbsPreprocessor):
    def __init__(self):
        # register the sources with ForestSourceFactory
        super().__init__("sources", ForestSourceFactory)


class ModelPreprocessor(AbsPreprocessor):
    def __init__(self):
        super().__init__("models", ForestModelFactory)


class ControllerPreprocessor(AbsPreprocessor):
    def __init__(self):
        super().__init__("controllers", ForestControllerFactory)
