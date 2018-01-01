#!/usr/bin/python3
# -*- coding: utf-8 -*-

import inspect
import datetime
import threading

from lib.psDebug import DBG, ERR
from lib.utils import Stamp
from lib.cacaostock import CacaoStock


class Schedule(threading.Thread):
    class Activity:
        def execute(self, dt=None):
            emsg = '%s@execute(Not Implemented)' % self.__class__.__name__
            ERR(emsg)
            raise NotImplementedError(emsg)

    def __init__(self):
        threading.Thread.__init__(self)
        self.fgRun = True
        self.cond = threading.Condition(threading.Lock())
        self.actPool = []
        self.start()

    def registerActivity(self, act):
        with self.cond:
            if isinstance(act, Schedule.Activity):
                self.actPool.append(act)
                return
        emsg = '"%s" is not instance of Schedule.Activity.' % act.__class__.__name__
        ERR(emsg)
        raise RuntimeError(emsg)

    def trigger(self, dt):
        with self.cond:
            delAct = []
            for act in self.actPool:
                if act.execute(dt):
                    continue
                delAct.append(act)
            for dact in delAct:
                self.actPool.remove(dact)

    def run(self):
        fgChgMinute = False
        dcurr = datetime.datetime.now()
        while self.fgRun:
            with self.cond:
                cv = self.cond.wait(1)
            dprev = dcurr
            dcurr = datetime.datetime.now()
            if dprev.minute != dcurr.minute:
                fgChgMinute = True

            if fgChgMinute:
                fgChgMinute = False
                DBG('# %s %s' % (str(cv), Stamp.now('%Y-%m-%d %H:%M:%S.%f')))
                self.trigger(dcurr)

    def stop(self):
        with self.cond:
            self.fgRun = False
            self.cond.notify()
            DBG('## STOP')


class Stock(CacaoStock, Schedule.Activity):
    def execute(self, dt):
        for code in ['095700', '002390', '066570', '000660']:
            s = self.getStock(code)
            if s:
                DBG(s.toString())
        return True

if __name__ == '__main__':
    import time
    s = Schedule()
    s.registerActivity(Stock())
    time.sleep(130)
    s.stop()
