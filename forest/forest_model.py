__author__ = 'xudshen@hotmail.com'

from forest.forest_factory import ForestAbsFactory


class ForestModel(object):
    def __init__(self, model_id, meta={}, databases=[]):
        self.__model_id = model_id
        self.__meta = meta
        if "fields" not in self.__meta:
            self.__meta["fields"] = {}
        self.__databases = databases

        self.__depend_sources = []

    def resolve_depend_sources(self):
        # resolve the meta
        meta_base_xpath = self.__meta["__base_xpath"]
        [self.__depend_sources.append(meta_base_xpath + field_prop["alias"]) for field_name, field_prop in
         self.__meta["fields"] if "alias" in field_prop]


class ForestModelFactory(ForestAbsFactory):
    __models = {}

    @classmethod
    def add(cls, model_id, item):
        cls.__models[model_id] = ForestModel(model_id, item["meta"], item["databases"])

    @classmethod
    def get(cls, model_id):
        return cls.__models[model_id]
