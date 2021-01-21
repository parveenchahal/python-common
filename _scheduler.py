from typing import Union
from types import FunctionType, MethodType
import threading
from datetime import timedelta

class Scheduler(threading.Thread):
    def __init__(self,
        callback: Union[FunctionType, MethodType],
        frequency: timedelta,
        name: str = None,
        *args,
        **kwargs):
        super(Scheduler, self).__init__(target=self.__callback_for_thread,\
            name=name,\
            *args,\
            **kwargs)
        super(Scheduler, self).setDaemon(True)
        if not isinstance(callback, FunctionType)\
        and not isinstance(callback, MethodType):
            raise TypeError("callback passed is not type of function")
        self.callback = callback
        self.frequency = frequency
        self.stop_signal = False
        self.thread_condition = threading.Condition()

    def __callback_for_thread(self):
        while not self.stop_signal:
            self.callback()
            try:
                self.thread_condition.acquire()
                self.thread_condition.wait(self.frequency.total_seconds())
            except (SystemExit, KeyboardInterrupt):
                raise
            finally:
                self.thread_condition.release()

    def stop(self):
        self.stop_signal = True
        while self.is_alive() and self.stop_signal:
            self.thread_condition.acquire()
            try:
                self.thread_condition.notify()
            finally:
                self.thread_condition.release()
            self.join(0.1)
