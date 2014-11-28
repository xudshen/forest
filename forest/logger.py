__author__ = 'xudshen@hotmail.com'

import logging, json
from pprint import pformat

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s: %(message)s")


def log_i(msg, obj=None):
    if obj is not None:
        logging.info(msg + "\n%s", pformat(obj, indent=2))
    else:
        logging.info(msg)


def log_d(msg, obj=None):
    if obj is not None:
        logging.debug(msg + "\n%s", pformat(obj, indent=2))
    else:
        logging.debug(msg)


class OperationParseError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ForestError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__position = {}

    def attach(self, key, node):
        self.__position = {key: node}

    def __str__(self, *args, **kwargs):
        return "@%s: %s" % (json.dumps(self.__position), super().__str__(*args, **kwargs))