__author__ = 'xudshen@hotmail.com'

from enum import Enum

import requests

from forest.forest_factory import ForestAbsFactory
from forest.logger import log_d


class HttpMethod(Enum):
    GET = 0
    POST = 1

    @classmethod
    def from_string(cls, value):
        return getattr(cls, value.upper(), None)


class ForestSource(object):
    def __init__(self, source_id, url, method, headers, body, result_type):
        self.__id = source_id
        self.__url = url
        self.__method = HttpMethod.from_string(method)
        self.__headers = headers
        self.__body = body
        self.__type = result_type

    def data(self):
        # send the request, get the data
        if self.__method is HttpMethod.GET:
            r = requests.get(self.__url, headers={}, params={}, data={})
            log_d(r.text)
        elif self.__method is HttpMethod.POST:
            r = requests.post(self.__url, headers={}, params={}, data={})
            log_d(r.text)


class ForestSourceFactory(ForestAbsFactory):
    __sources = {}

    @classmethod
    def add(cls, source_id, item):
        cls.__sources[source_id] = ForestSource(source_id, item["url"], item["method"], item["headers"], item["body"],
                                                item["type"])

    @classmethod
    def get(cls, source_id):
        return cls.__sources[source_id]
