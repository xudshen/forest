__author__ = 'xudshen@hotmail.com'

import re
import json

from forest.forest_factory import ForestAbsFactory
from forest.forest_source import ForestSourceFactory

from forest.logger import log_d
from forest.path_parser import resolve_xpath, split_path


class Converter:
    @staticmethod
    def __parse_method(convert):
        if isinstance(convert, list) and len(convert) > 0:
            return convert[0], convert[1:]
        elif isinstance(convert, str):
            return convert, []
        else:
            return None, []

    @staticmethod
    def execute_filter(values, convert):
        method_name, args = Converter.__parse_method(convert)
        if method_name is None:
            return values, None
        # execute
        try:
            method = getattr(Converter, method_name)
            if callable(method):
                return method(values, *args)
            else:
                log_d("Converter.%s is not callable" % (method_name,))
                return values, None
        except AttributeError:
            log_d("not found Converter.%s" % (method_name,))

    @staticmethod
    def equal_method(convert_a, convert_b):
        method_name_a, _ = Converter.__parse_method(convert_a)
        method_name_b, _ = Converter.__parse_method(convert_b)
        return method_name_a == method_name_b

    @staticmethod
    def string(values):
        assert isinstance(values, object)
        return [str(value) for value in values], None

    @staticmethod
    def int(values):
        return [int(float(str(value))) for value in values], None

    @staticmethod
    def string_with_trim(values):
        return [str(value).strip() for value in values], None

    @staticmethod
    def regex(values, rule):
        ret = []
        for value in values:
            log_d(value)
            m = re.match(rule, value)
            if m is not None:
                ret.append(m)
        return ret, 'index'

    @staticmethod
    def index(values, key=0):
        ret = []
        for value in values:
            g = value.group(key)
            if g is not None:
                ret.append(g)
        return ret, None


class ForestModel(object):
    __private_prefix = "__"
    __xpath = "__xpath"
    __source_prefix = "source://"

    __field = "fields"
    __field_list = "__list"

    def __init__(self, model_id, meta=None, databases=None):
        self.__model_id = model_id
        self.__meta = meta
        self.__databases = databases

        self.depend_sources = {}
        self.grouped_depend_sources = {}
        # log_d(self)

    def __value_of_src(self, operation, src):
        path, chain = resolve_xpath(operation)
        if path is None and chain is None:
            return operation

        if path is not None:
            if path.startswith(self.__source_prefix):
                scheme, loc, xpath = split_path(path)
                src = ForestSourceFactory.get(loc).data()
            else:
                xpath = path
            # check the type here
            src = src.xpath(xpath)

        chain = chain if chain is not None else []
        for idx, _ in enumerate(chain):
            src, next_filter = Converter.execute_filter(src, chain[idx])
            # for the convert chain
            while not Converter.equal_method(next_filter,
                                             chain[idx + 1] if idx + 1 < len(chain) else None):
                src, next_filter = Converter.execute_filter(src, next_filter)

        return src

    def __result(self, key, node, src, level):
        level += 1
        if type(node) is str:
            src = self.__value_of_src(node, src)
            return key, (src[0] if type(src) is list and len(src) > 0 else src) \
                if key is not None else src
        elif type(node) is dict:
            if self.__xpath in node:
                src = self.__value_of_src(node[self.__xpath], src)

            src = src if type(src) is list else [src]
            node_r = []
            for idx, src_item in enumerate(src):
                node_r.append({})
                for k, v in node.items():
                    if not str.startswith(k, self.__private_prefix):
                        _, node_r[idx][k] = self.__result(k, v, src_item, level)
            return key, node_r
        elif type(node) is list:
            # if list, combine the list item to a new list
            node_r = []
            for k, v in enumerate(node):
                _, ret = self.__result(None, v, src, level)
                if type(ret) is list:
                    node_r += ret
                else:
                    node_r.append(ret)
            return key, node_r if len(node_r) > 1 else (node_r[0] if len(node_r) != 0 else None)
        return key, node

    def result(self):
        _, ret = self.__result(None, self.__databases, None, 0)
        log_d(json.dumps(ret, indent=2))

    def __str__(self, *args, **kwargs):
        return json.dumps(
            {"id": self.__model_id, "meta": self.__meta, "databases": self.__databases,
             "depend_sources": self.depend_sources, "grouped_depend_sources": self.grouped_depend_sources},
            indent=2)


class ForestModelFactory(ForestAbsFactory):
    __models = {}

    @classmethod
    def add(cls, model_id, item):
        meta = item["meta"] if "meta" in item else {}
        if "fields" not in meta:
            meta["fields"] = {}
        databases = item["databases"] if "databases" in item else {}
        cls.__models[model_id] = ForestModel(model_id, meta, databases)

    @classmethod
    def get(cls, model_id) -> ForestModel:
        return cls.__models[model_id] if model_id in cls.__models else None

    @classmethod
    def values(cls):
        """

        :rtype : list of ForestModel
        """
        return cls.__models.values()
