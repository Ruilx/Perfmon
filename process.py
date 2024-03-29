# -*- coding: utf-8 -*-

from multiprocessing import Queue
from typing import overload

from logger import Logger
from process.process_base import ProcessBase

import util


class Process(object):
    def __init__(self, queue: Queue):
        self._queue = queue
        self._process_items = {}
        self.running = True

    def register_process(self, process: ProcessBase):
        self._process_items[process.name()] = process

    def setRun(self, running: bool):
        self.running = running

    def run(self):
        while self.running:
            data = self._queue.get()

            if "cmd" not in data:
                Logger().getLogger(__name__).error(f"queue data expect a 'cmd' key in it, but get: {data!r}")
                continue

            if data['cmd'] == "quit":
                # shutdown...
                self.setRun(False)
                continue

            if data['cmd'] == "process":
                if 'name' not in data:
                    Logger().getLogger(__name__).error(f"queue data expect a 'name' key in 'process' cmd, but get: {data!r}")
                    continue

                if data['name'] not in self._process_items:
                    Logger().getLogger(__name__).error(f"process name '{data['name']}' is not registered.")
                    Logger().getLogger(__name__).info(f"Registered process name:")
                    for item in self._process_items.keys():
                        Logger().getLogger(__name__).info(item)
                    Logger().getLogger(__name__).info("")
                    continue

                if 'params' not in data:
                    Logger().getLogger(__name__).error(f"queue data expect a 'param' key in it, but get: {data!r}")
                    continue

                process: ProcessBase = self._process_items[data['name']]
                try:
                    process.process(data['params'])
                except BaseException as e:
                    Logger().getLogger(__name__).error(f"Process {data['name']} has unhandled exception: {e!r}")
                    util.printTraceback(e, Logger().getLogger(__name__).error)
