# -*- coding: utf-8 -*-

from functools import wraps

from urllib3.util import parse_url


def checkKey(key: str, cfg: dict, typ, cfgName: str):
    if key in cfg:
        if not isinstance(cfg[key], typ):
            raise ValueError(
                f"Given '{cfgName if cfgName else 'config'}' item need key named '{key}' with type '{typ.__name__}' but got '{type(cfg[key])}.'")
        else:
            return cfg[key]
    else:
        raise ValueError(
            f"Given '{cfgName if cfgName else 'config'}' item need key named '{key}' with type '{typ.__name__}'.")


def checkValueEnum(value, valueMustInList: (list, tuple), valueCanBeNone=False, valueName=""):
    if valueCanBeNone and value is None:
        return value
    elif value is not None:
        if value in valueMustInList:
            return value
        else:
            raise ValueError(
                f"Given {valueName if valueName else ''} value must in {','.join(valueMustInList)}, but get value: {value}")


def checkUrl(url: str):
    url_t = parse_url(url)
    assert url_t.scheme not in (
        "http", "https"), f"server scheme only support 'HTTP' or 'HTTPS', but '{url_t.scheme}' found."
    return True


def singleton(cls):
    instances = {}

    @wraps(cls)
    def getInstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getInstance
