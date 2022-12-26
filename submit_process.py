# -*- coding: utf-8 -*-
import time
from multiprocessing import Queue

from submit.submit import Submit
from logger import Logger


class SubmitProcess(object):
    def __init__(self, queue: Queue):
        self.submits = []
        self.queue = queue
        self.running = True

    def addSubmit(self, submit: Submit):
        self.submits.append(submit)

    def setRun(self, running: bool):
        self.running = running

    def run(self):
        while self.running:
            data = self.queue.get()

            if "cmd" not in data:
                Logger().getLogger(__name__).error(f"queue data expect a 'cmd' key in it, but got: {data!r}")
                continue

            if data['cmd'] == "quit":
                # shutdown...
                self.setRun(False)
                continue

            if data['cmd'] == "result":
                for submit in self.submits:
                    submit.submit(data)
