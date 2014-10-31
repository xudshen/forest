__author__ = 'xudshen@hotmail.com'

import re
import json

from forest.forest_factory import ForestAbsFactory


class ForestModel(object):
    __fields = "fields"
    __fields_alias = "alias"
    __fields_convert = "convert"

    __base_xpath = "__base_xpath"
    __source_prefix = "source://"

    def __init__(self, model_id, meta={}, databases=[]):
        self.__model_id = model_id
        self.__meta = meta
        if self.__fields not in self.__meta:
            self.__meta[self.__fields] = {}
        self.__databases = databases

        self.__depend_sources = []
        self.resolve_depend_sources()

    @staticmethod
    def __match_xpath(xpath):
        m = re.match(r"^\{(.*)\}(\[(.*)\])?$", xpath)
        if m is not None:
            return m.group(1), m.group(3)
        else:
            return None, None

    def resolve_depend_sources(self):

        # resolve the meta
        meta_base_xpath = self.__meta[self.__base_xpath] if self.__base_xpath in self.__meta else ""
        for field_name, field_prop in self.__meta[self.__fields].items():
            if self.__fields_alias in field_prop:
                # when match {}[] pattern, assume it as the xpath
                sub_path, convert_func = self.__match_xpath(field_prop[self.__fields_alias])
                if sub_path is None:
                    continue
                # re-assign the alias value
                if not str.startswith(sub_path, self.__source_prefix):
                    sub_path = meta_base_xpath + sub_path

                self.__depend_sources.append(sub_path)
                field_prop[self.__fields_alias] = sub_path
                field_prop[self.__fields_convert] = convert_func

        # resolve databases
        for db in self.__databases:
            db_base_xpath = db[self.__base_xpath] if self.__base_xpath in db else ""
            for k, v in db.items():
                # when match {}[] pattern, assume it as the xpath
                sub_path, convert_func = self.__match_xpath(v)
                if sub_path is None:
                    continue
                # re-assign the alias value
                if not str.startswith(sub_path, self.__source_prefix):
                    sub_path = db_base_xpath + sub_path
                self.__depend_sources.append(sub_path)
                db[k] = sub_path

    def __str__(self, *args, **kwargs):
        return json.dumps({"id": self.__model_id, "meta": self.__meta, "databases": self.__databases}, indent=2)


class ForestModelFactory(ForestAbsFactory):
    __models = {}

    @classmethod
    def add(cls, model_id, item):
        cls.__models[model_id] = ForestModel(model_id, item["meta"], item["databases"])

    @classmethod
    def get(cls, model_id):
        return cls.__models[model_id]
