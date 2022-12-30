# -*- coding: utf-8 -*-

import util
from multiprocessing import Queue

from process import Process


class Prefmon(object):
    def __init__(self, agentName, prefmonCfg: dict, process_instance: Process, queue: Queue):
        self.agentName = agentName
        self.name = None
        self.type = None
        self.delay = None
        self.queue = queue
        self._process_instance = process_instance
        self.process = {}
        self.__parsePerfmonCfg(prefmonCfg)

    def __registerProcess(self):
        if not self.process:
            return
        method = util.checkKey("method", self.process, str, "process")
        match method:
            case "readfile":
                from process.readfile import Readfile
                self._process_instance.register_process(Readfile(self.process, self.name, self.queue))
            case "execute":
                ...
            case default:
                raise ValueError(f"process method: {method} is not support yet.")

    def __parsePerfmonCfg(self, perfmonCfg):
        if not isinstance(perfmonCfg, dict):
            raise ValueError(f"perfmonCfg need type 'dict' but '{type(perfmonCfg)}' found.")
        self.name = util.checkKey("name", perfmonCfg, str, "perfmonCfg")
        self.type = util.checkKey("type", perfmonCfg, str, "perfmonCfg")
        self.delay = util.checkKey("delay", perfmonCfg, (str, int), "perfmonCfg")
        self.process = util.checkKey("process", perfmonCfg, dict, "perfmonCfg")
        self.__registerProcess()
