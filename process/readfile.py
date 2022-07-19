# -*- coding: utf-8 -*-

class Readfile(object):

    def __init__(self, name: str, process: dict):
        self.name = name,
        self.process = None
        self.setProcess(process)

    def setProcess(self, process: dict):
        assert "method" in process
        method = process['method']
        if method != "readfile":
            raise TypeError(f"ReadFile class need a readfile-type config, but find '{method}' type")

