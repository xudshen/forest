__author__ = 'xudshen@hotmail.com'

import re
import json

from forest.forest_factory import ForestAbsFactory
from forest.forest_source import ForestSourceFactory
from forest.logger import log_d


class Converter:
    @staticmethod
    def string(value):
        assert isinstance(value, object)
        return str(value)

    @staticmethod
    def int(value):
        return int(float(str(value)))


class ForestModel(object):
    __private_prefix = "__"
    __xpath = "__xpath"
    __convert = "convert"
    __default_convert = "string"
    __source_prefix = "source://"

    def __init__(self, model_id, meta=None, databases=None):
        self.__model_id = model_id
        self.__meta = self.__normalize_source(None, meta, 0, {"__xpath": ""})
        self.__databases = self.__normalize_source(None, databases, 0, {"__xpath": ""})

        self.depend_sources = {}
        self.grouped_depend_sources = {}
        self.__resolve_depend_source()

    @staticmethod
    def __match_xpath(xpath):
        m = re.match(r"^\{(.*)\}(\[(.*)\])?$", xpath)
        if m is not None:
            return m.group(1), m.group(3)
        else:
            return None, None

    @staticmethod
    def __split_source(uri):
        m = re.match(r"^(.*)://(\w+)(/.*)$", uri)
        if m is not None:
            return {"scheme": m.group(1), "loc": m.group(2), "path": m.group(3), "value": None}
        else:
            return None

    def __normalize_source(self, k, node, level, env):
        """
        traverse the json object, normalize the path
        :param k:     the key, if it is called from a list, key=""
        :param node:  the value
        :param level: just indicates current level
        :param env:  {"__xpath": ""}, stores the current env
        :return: the normalized json object
        """
        level += 1
        # when the node is the leaf
        if type(node) is str:
            path, convert = self.__match_xpath(node)
            # if the value match the source pattern
            if path is not None:
                # generate the full path
                full_path = None
                if not path.startswith(self.__source_prefix):
                    # path is not a full path(start with source://)
                    full_path = "{%s%s}[%s]" % (env[k] if k in env else env[self.__xpath], path,
                                                convert if convert is not None else self.__default_convert)
                elif convert is None or len(convert) == 0:
                    # path is a full path but has not convert definition
                    full_path = "{%s}[%s]" % (path, self.__default_convert)

                # if key of full_path is a simplified format, add the default "__xpath"
                node = {self.__xpath: full_path} if k not in env else full_path

            # if the value not match the source pattern
            else:
                # check if it is a simplified version of value
                node = {"value": node} if k is not None and not k.startswith(self.__private_prefix) and k != "value" \
                    else node
        # when the node is dict
        elif type(node) is dict:
            env_c = dict(env)
            # first process the items with "__" prefix
            for k, v in node.items():
                if k in env:
                    node[k] = self.__normalize_source(k, v, level, dict(env))
                    # the "__" prefix value will effect the following base value
                    env_c[k] += str(v)
            # then process the other items
            for k, v in node.items():
                if not k in env:
                    node[k] = self.__normalize_source(k, v, level, dict(env_c))
        # when the node is list
        elif type(node) is list:
            for i, v in enumerate(node):
                node[i] = self.__normalize_source(None, v, level, dict(env))
        return node

    def __resolve_depend_source(self):
        from collections import deque

        self.depend_sources = {}
        q = deque([[None, self.__meta], [None, self.__databases]])
        while len(q) > 0:
            [k, node] = q.popleft()
            if type(node) is str and k == self.__xpath:
                path, convert = self.__match_xpath(node)
                if path is not None:
                    self.depend_sources[node] = self.__split_source(path)
                    self.depend_sources[node][self.__convert] = convert
            if type(node) is dict:
                [q.append([k1, v1]) for k1, v1 in node.items()]
            if type(node) is list:
                [q.append([None, v1]) for v1 in node]

        for meta_source in self.depend_sources.values():
            if meta_source["loc"] not in self.grouped_depend_sources:
                self.grouped_depend_sources[meta_source["loc"]] = []
            self.grouped_depend_sources[meta_source["loc"]].append(meta_source)

    def __str__(self, *args, **kwargs):
        return json.dumps(
            {"id": self.__model_id, "meta": self.__meta, "databases": self.__databases,
             "depends": [self.depend_sources, self.grouped_depend_sources]},
            indent=2)

    def result(self):
        for k, meta_sources in self.grouped_depend_sources.items():
            if meta_sources is None:
                continue

            root = ForestSourceFactory.get(k).data()
            for meta_source in meta_sources:
                meta_source["value"] = [getattr(Converter, meta_source["convert"])(value)
                                        for value in root.xpath(meta_source["path"])]
                log_d(meta_source["value"])

 
class ForestModelFactory(ForestAbsFactory):
    __models = {}

    @classmethod
    def add(cls, model_id, item):
        cls.__models[model_id] = ForestModel(model_id, item["meta"], item["databases"])

    @classmethod
    def get(cls, model_id):
        return cls.__models[model_id] if model_id in cls.__models else None

    @classmethod
    def values(cls):
        return cls.__models.values()
