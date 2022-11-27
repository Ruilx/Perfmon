# -*- coding: utf-8 -*-
import datetime
import logging
from threading import Timer


class Submit(object):
    def __init__(self, capacity: int = 20, timeout: int = 10000):
        self.capacity = capacity
        self.timeout = timeout
        self.buf = []

        self.timer = Timer(self.timeout / 1000, self.timerEvent)

        self.logger = logging.getLogger(__name__)

    def send(self) -> bool:
        raise NotImplementedError(f"{__name__}.{__method__} need implement.")

    def ready(self):
        self.logger.debug("Submit: Ready to send data")
        result = self.send()
        if result:
            self.logger.debug("Submit: committed.")
            self.buf = []

    def checkBuf(self):
        if len(self.buf) >= self.capacity:
            self.ready()

    def timerEvent(self):
        if len(self.buf) == 0:
            self.logger.debug("Timer trigger with no buffer data")
            return
        self.ready()

    def timerStop(self):
        if self.timer.is_alive():
            self.timer.cancel()
            self.timer.finished.clear()
            self.logger.debug("Timer stopped")

    def timeStart(self):
        if not self.timer.is_alive():
            self.logger.debug("Timer start")
            self.timer.run()

    def submit(self, data: dict):
        if "create_time" not in data:
            data['create_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.buf.append(data)
        self.timerStop()
        self.checkBuf()
        self.timeStart()
