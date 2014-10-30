__author__ = 'xudshen@hotmail.com'


class ForestAbsFactory(object):
    """abstract factory"""

    @classmethod
    def add(cls, obj_id, obj):
        raise NotImplementedError("not implement")

    @classmethod
    def get(cls, obj_id):
        raise NotImplementedError("not implement")