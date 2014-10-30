__author__ = 'xudshen@hotmail.com'

from forest.forest_factory import ForestAbsFactory


class ForestModel(object):
    def __init__(self):
        pass


class ForestModelFactory(ForestAbsFactory):
    __models = {}

    @classmethod
    def add(cls, model_id, model):
        cls.__models[model_id] = model