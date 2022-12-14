# -*- coding: utf-8 -*-
import json
import os.path


class Config(object):
    def __init__(self, filepath):
        self.cfg = {}
        self.__loadCfg(filepath)

    def setConfigPath(self, filepath):
        self.cfg = {}
        self.__loadCfg(filepath)

    def __loadCfg(self, filepath):
        if not os.path.exists(filepath):
            raise ValueError(f"CConfig: filepath: '{filepath}' not valid.")
        with open(filepath, 'r') as fd:
            self.cfg = json.load(fd)

    def __findKey(self, *keys):
        currentNode = self.cfg
        for key in keys:
            if isinstance(currentNode, dict):
                if key in currentNode:
                    currentNode = currentNode[key]
            elif isinstance(currentNode, (list, tuple)):
                if isinstance(key, int):
                    if key < len(currentNode):
                        currentNode = currentNode[key]
                    else:
                        currentNode = None
                        break
                elif isinstance(key, str):
                    result = []
                    for current in currentNode:
                        if isinstance(current, dict):
                            if key in current:
                                result.append(current[key])
                    currentNode = result
            else:
                return currentNode
        return currentNode

    def findKey(self, *key):
        return self.__findKey(*key)

    def getAgentName(self):
        return self.__findKey("agent_name")
