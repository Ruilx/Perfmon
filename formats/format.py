# -*- coding: utf-8 -*-

from util import singleton


@singleton
class FormatFactory(object):
    def __init__(self):
        self.__formats = {}

    def __setitem__(self, key: str, value):
        self.__formats[key] = value

    def __getitem__(self, key: str):
        if key in self.__formats:
            return self.__formats[key]

    def __contains__(self, key: str):
        return key in self.__formats


def format(name):
    def decorator(func):
        if name not in FormatFactory():
            FormatFactory()[name] = func

            def inner(value):
                if callable(func):
                    return func(value)
                raise ValueError(f"function '{func}' cannot callable.")

            return inner
        else:
            raise NameError(f"name '{name}' already in format factory.")
    return decorator

class FormatError(RuntimeError):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg
