# -*- coding: utf-8 -*-

import util
from formats.format import FormatFactory


class Process(object):
    ValidExpectEnum = ('int', 'intOrNull', 'real', 'realOrNull', 'string', 'stringOrNull', 'null')

    def __init__(self, config):
        self._method = util.checkKey("method", config, str, "process")
        self._format = util.checkKey("format", config, (str, list), "process")
        self._expect = util.checkKey("expect", config, str, "process")
        self._waiting = util.checkKey("waiting", config, str, "process")

        expect = util.checkValueEnum(self._expect, Process.ValidExpectEnum, valueName="expect")

        self._value = None

    def _doFormat(self):
        """
        从
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
            else:
                raise ValueError(f"cur items need format str, but '{type(cur)}' found.")

        self._value = __doFormat(self._format)

    def __doHandleIntValue(self, nullable):
        """
        取得的value转换成int格式, 确保value类型是int(容忍value是int型str的转换)
        由_doExpect调用
        :return: void
        :raise: ValueError
        """
        if not isinstance(self._value, int):
            if nullable and self._value is None:
                return
            try:
                self._value = int(self._value)
            except (ValueError, TypeError) as e:
                raise ValueError(f"value expect type 'int'(int), but type '{type(self._value)}' found.")

    def __doHandleRealValue(self, nullable):
        if not isinstance(self._value, float):
            if nullable and self._value is None:
                return
            try:
                self._value = float(self._value)
            except (ValueError, TypeError) as e:
                raise ValueError(f"value expect type 'real'(float), but type '{type(self._value)}' found.")

    def __doHandleStringValue(self, nullable):
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


