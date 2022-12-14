# -*- coding: utf-8 -*-

from queue import Queue


class Process(object):
    def __init__(self, queue: Queue):
        self._queue = queue
        self._process_item = []
