# -*- coding: utf-8 -*-

import logging
import sys

from util import singleton

@singleton
class Logger(object):
    def __init__(self):
        self.loggers = {}

    def addLogger(self, name, level=):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        self._setup(logger)
        self.loggers[name] = logger

    def getLogger(self, name):
        if name not in self.loggers:
            self.addLogger(name)
        return logging.getLogger(name)

    def _setup(self, logger):
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s(@%(threadName)s): %(filename)s:%(lineno)s: %(name)s: %(message)s")
        handler1 = logging.StreamHandler(stream=sys.stderr)
        handler1.setFormatter(self.formatter)
        # handler2 = logging.FileHandler(self.name, encoding="utf-8", delay=True)
        # handler2.setFormatter(self.formatter)
        logger.handlers.append(handler1)
        # logger.handlers.append(handler2)
