# -*- coding: utf-8 -*-

import util
from formats.format import FormatFactory

from multiprocessing import Queue

from logger import Logger


class ProcessBase(object):
    ValidExpectEnum = ['int', 'intOrNull', 'real', 'realOrNull', 'string', 'stringOrNull', 'null']

    def __init__(self, config, name, queue: Queue):
        self._name = name
        self._config = config
        self._queue = queue
        self._method = util.checkKey("method", config, str, "process")
        self._format = util.checkKey("format", config, (str, list), "process")
        self._expect = util.checkKey("expect", config, str, "process")
        self._waiting = util.checkKey("waiting", config, str, "process")

        try:
            self._retry = util.checkKey("retry", config, str, "process")
        except ValueError:
            self._retry = 3

        util.checkValueEnum(self._expect, ProcessBase.ValidExpectEnum, valueName="expect")
        self._value = None
        self.checkProcess()
        self.setup()

    def __del__(self):
        self.join()

    def name(self):
        return self._name

    def _doFormat(self):
        """
        从format工厂中处理所得到的值
        :return:
        """

        def __doFormat(cur):
            if isinstance(cur, str):
                return FormatFactory()[cur](self._value)
            elif isinstance(cur, list):
                currentValue = self._value
                for c in cur:
                    currentValue = __doFormat(c)
                    if not currentValue:
                        return None
                return currentValue
            elif cur is None:
                return self._value
            else:
                raise ValueError(f"cur items need format str, but '{type(cur)}' found.")

        self._value = __doFormat(self._format)

    def __doHandleIntValue(self, nullable):
        """
        取得的value转换成int格式, 确保value类型是int(容忍value是int型的字符串)
        由_doExpect调用
        :param nullable: bool value是否可以为None
        :return void: 内部改变self._value的值, 有问题走异常, 不需要返回
        :raise ValueError: 如果为None(nullable==False)或不能转换时将会抛出异常
        """
        if not isinstance(self._value, int):
            if nullable and self._value is None:
                return
            try:
                self._value = int(self._value)
            except (ValueError, TypeError) as e:
                raise ValueError(f"value expect type 'int'(int), but type '{type(self._value)}' found.")

    def __doHandleRealValue(self, nullable):
        """
        取得的value转成float格式, 确保value类型是float(容忍value是float型的字符串)
        由_doExpect调用
        :param nullable: bool value是否可以为None
        :return void: 内部改变self._value的值, 有问题走异常, 不需要返回
        :raise ValueError: 如果为None(nullable==False)或不能转换时将会抛出异常
        """
        if not isinstance(self._value, float):
            if nullable and self._value is None:
                return
            try:
                self._value = float(self._value)
            except (ValueError, TypeError) as e:
                raise ValueError(f"value expect type 'real'(float), but type '{type(self._value)}' found.")

    def __doHandleStringValue(self, nullable):
        """
        取得的value转成string格式, 确保value类型是string
        由_doExpect调用
        :param nullable: bool value是否可以为None
        :return: void: 内部改变self._value的值, 有问题走异常, 不需要返回
        :raise ValueError: 如果为None(nullable==False)或不能转换时将会抛出异常
        """
        if not isinstance(self._value, str):
            if nullable and self._value is None:
                return
            try:
                self._value = float(self._value)
            except (ValueError, TypeError) as e:
                raise ValueError(f"value expect type 'string'(str), but type '{type(self._value)}' found.")

    def __doHandleNullValue(self):
        if self._value is not None:
            raise ValueError(f"value expect type 'null'(None) but type '{type(self._value)}' found.")

    def _doExpect(self):
        """
        :param self:
        :return:
        :raise: ValueError
        """
        if self._expect == "int":
            self.__doHandleIntValue(False)
        elif self._expect == "intOrNull":
            self.__doHandleIntValue(True)
        elif self._expect == "real":
            self.__doHandleRealValue(False)
        elif self._expect == "realOrNone":
            self.__doHandleRealValue(True)
        elif self._expect == "string":
            self.__doHandleStringValue(False)
        elif self._expect == "stringOrNull":
            self.__doHandleStringValue(True)
        elif self._expect == "null":
            self.__doHandleNullValue()

    def checkProcess(self):
        raise NotImplementedError(f"{__name__}.{__method__} need implement.")

    def setup(self):
        raise NotImplementedError(f"{__name__}.{__method__} need implement.")

    def run(self, params):
        raise NotImplementedError(f"{__name__}.{__method__} need implement.")

    def join(self):
        raise NotImplementedError(f"{__name__}.{__method__} need implement.")

    def _doProcess(self, params):
        error = None
        for attempt in range(self._retry):
            try:
                self.run(params)
                self._doFormat()
                self._doExpect()
                error = None
                break
            except BaseException as e:
                Logger().getLogger(__name__).error(f"Exception occurred while processing: {e!r}")
                util.printTraceback(e, Logger().getLogger(__name__).error)
                error = e
                continue
        if error is not None:
            self.submitError(params, error)
        else:
            self.submit(params)

    def process(self, params):
        return self._doProcess(params)

    def submit(self, params):
        self._queue.put({
            'cmd': "result",
            'name': self._name,
            'params': params,
            'except': self._expect,
            'value': self._value,
            'errno': 0,
            'error': "",
            'timestamp': util.timestamp()
        })

    def submitError(self, params, exception: BaseException):
        self._queue.put({
            'cmd': "error",
            'name': self._name,
            'params': params,
            'except': self._expect,
            'value': self._value,
            'errno': 1,
            'error': "{}: {}".format(exception.__class__.__name__, exception.__repr__()),
            'timestamp': util.timestamp()
        })
