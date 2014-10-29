__author__ = 'xudshen@hotmail.com'

from forest.logger import log_d


class AbsPreprocessor(object):
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
        log_d(obj)


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
