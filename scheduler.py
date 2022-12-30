# -*- coding: utf-8 -*-

import os
from sched import scheduler

from process import Process
from perfmon import Prefmon

class Scheduler(object):
    def __init__(self, process_instance: Process):
        self.scheduler = scheduler()
        self.process_instance = process_instance
        self.prefmon = {}
        self.default_priority = 1

    def register_scheduler(self, prefmon: Prefmon):
        self.prefmon[prefmon.name] = prefmon
        self.scheduler.enter(prefmon.delay, self.default_priority, self.process_instance.run())
