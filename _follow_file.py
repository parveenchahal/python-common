from typing import Union
from types import FunctionType, MethodType
import threading

class FollowFile(threading.Thread):
    def __init__(self,
        callback: Union[FunctionType, MethodType],
        path: str):
        super(FollowFile, self).__init__(target=self.__callback_for_thread,\
            name='follow_file')
        super(FollowFile, self).setDaemon(True)
        if not isinstance(callback, FunctionType)\
        and not isinstance(callback, MethodType):
            raise TypeError("callback passed is not type of function")
        self._callback = callback
        self._path = path
        self._stop_signal = False

    def __callback_for_thread(self):
        with open(self._path) as f:
            while not self._stop_signal:
                line = f.readline()
                if line and len(line) > 0:
                    line = line[:line.rfind('\n')]
                    self._callback(line)

    def stop(self):
        self._stop_signal = True
        while self.is_alive() and self._stop_signal:
            self.join(0.1)
