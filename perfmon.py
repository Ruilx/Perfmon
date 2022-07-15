# -*- coding: utf-8 -*-

import util

class Prefmon(object):
    def __init__(self, agentName, prefmonCfg):
        self.agentName = agentName
        self.name = None
        self.type = None
        self.delay = None
        self.process = {}
        self.__parsePerfmonCfg(prefmonCfg)

    def __parsePerfmonCfg(self, perfmonCfg):
        if not isinstance(perfmonCfg, dict):
            raise ValueError(f"perfmonCfg need type 'dict' but '{type(perfmonCfg)}' found.")
        self.name = util.checkKey("name", perfmonCfg, str, "perfmonCfg")
        self.type = util.checkKey("type", perfmonCfg, str, "perfmonCfg")
        self.delay = util.checkKey("delay", perfmonCfg, (str, int), "perfmonCfg")
        self.process = util.checkKey("process", perfmonCfg, dict, "perfmonCfg")

        
