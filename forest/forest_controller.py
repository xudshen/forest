__author__ = 'xudshen@hotmail.com'

from forest.forest_factory import ForestAbsFactory


class ForestControllerFactory(ForestAbsFactory):
    __controllers = {}

    @classmethod
    def add(cls, controller_id, item):
        pass

    @classmethod
    def get(cls, controller_id):
        return cls.__controllers[controller_id]