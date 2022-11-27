# -*- coding: utf-8 -*-
import io

from process import Process

import util

from pathlib import Path

class Readfile(Process):
    def __init__(self, config, name):
        self._path = None
        self._length = 0
        self._fd = None
        super().__init__(config, name)

    def checkProcess(self):
        if self._method != "readfile":
            raise TypeError(f"ReadFile class need a readfile-type config, but find '{self._method}' type")

        self._path = Path(util.checkKey("path", self._config, str, "process"))
        self._length = util.checkKey("length", self._config, int, "process")

        if not self._path.is_absolute():
            raise ValueError(f"Readfile class file path '{self._path!r}' need a absolute path.")

        if not self._path.is_file():
            raise ValueError(f"Readfile class file path '{self._path!r}' must be a regular file.")

    def openFile(self):
        self._fd = self._path.open("r", encoding="utf-8")
    def setup(self):
        if not isinstance(self._path, Path):
            raise RuntimeError(f"Perfmon item {self._name} with readfile method has no valid path: '{self._path!r}'")
        if not isinstance(self._fd, io.TextIOWrapper) or self._fd.closed:
            self.openFile()

    def run(self):
        if not isinstance(self._fd, io.TextIOWrapper) or self._fd.closed:
            self.openFile()
        self._fd.seek(0)
        self._value = self._fd.read(self._length)

    def join(self):
        if isinstance(self._fd, io.TextIOWrapper) and not self._fd.closed:
            self._fd.close()
