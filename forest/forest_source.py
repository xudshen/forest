__author__ = 'xudshen@hotmail.com'

from enum import Enum

import requests
from lxml import etree
from bs4 import BeautifulSoup

from forest.forest_factory import ForestAbsFactory


class HttpMethod(Enum):
    GET = 0
    POST = 1

    @classmethod
    def from_string(cls, value):
        return getattr(cls, value.upper(), None)


class ForestSource(object):
    def __init__(self, source_id, url, method="GET", headers=None, body="", parser="html5lib"):
        self.__id = source_id
        self.__url = url
        self.__method = HttpMethod.from_string(method)
        self.__headers = headers if headers is not None else {}
        self.__body = body
        self.__parser = parser

    def data(self):
        # send the request, get the data
        parser = etree.HTMLParser(recover=True) if self.__parser != "xml" \
            else etree.XMLParser(ns_clean=True, recover=True)
        content = ""
        if self.__method is HttpMethod.GET:
            r = requests.get(self.__url, headers=self.__headers, params={}, data=self.__body)
            content = r.text
        elif self.__method is HttpMethod.POST:
            r = requests.post(self.__url, headers=self.__headers, params={}, data=self.__body)
            content = r.text
        soup = BeautifulSoup(content, self.__parser)
        return etree.fromstring(str(soup), parser=parser)


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
        parser = item["parser"] if "parser" in item else "html5lib"

        cls.__sources[source_id] = ForestSource(source_id, url, method, headers, body, parser)

    @classmethod
    def get(cls, source_id) -> ForestSource:
        return cls.__sources[source_id] if source_id in cls.__sources else None
