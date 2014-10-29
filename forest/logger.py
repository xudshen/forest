__author__ = 'xudshen@hotmail.com'

import logging
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