__author__ = 'xudshen@hotmail.com'

from enum import Enum

import requests
from lxml import etree

from forest.forest_factory import ForestAbsFactory


class HttpMethod(Enum):
    GET = 0
    POST = 1

    @classmethod
    def from_string(cls, value):
        return getattr(cls, value.upper(), None)


class ForestSource(object):
    def __init__(self, source_id, url, method="GET", headers=None, body="", result_type="html"):
        self.__id = source_id
        self.__url = url
        self.__method = HttpMethod.from_string(method)
        self.__headers = headers if headers is not None else {}
        self.__body = body
        self.__result_type = result_type

    def data(self):
        # send the request, get the data
        parser = etree.HTMLParser() if self.__result_type == "html" else etree.XMLParser(ns_clean=True, recover=True)
        if self.__method is HttpMethod.GET:
            r = requests.get(self.__url, headers=self.__headers, params={}, data=self.__body)
            return etree.fromstring(r.text.encode('utf-8'), parser=parser)
        elif self.__method is HttpMethod.POST:
            r = requests.post(self.__url, headers=self.__headers, params={}, data=self.__body)
            return etree.fromstring(r.text.encode('utf-8'), parser=parser)


class ForestSourceFactory(ForestAbsFactory):
    __sources = {}

    @classmethod
    def add(cls, source_id, item):
        if "url" not in item:
            raise AssertionError("not find the url")
        url = item["url"]
        method = item["method"] if "method" in item else "GET"
        headers = item["headers"] if "headers" in item else {}
        body = item["body"] if "body" in item else ""
        result_type = item["result_type"] if "result_type" in item else "html"

        cls.__sources[source_id] = ForestSource(source_id, url, method, headers, body, result_type)

    @classmethod
    def get(cls, source_id):
        return cls.__sources[source_id] if source_id in cls.__sources else None
