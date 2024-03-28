from time import time
from datetime import datetime

class TimeProbe:
    def __init__(self, auto_start: bool = False):
        self._running = False
        self._start = 0.0
        self._end = 0.0

        if auto_start:
            self.start()

    def start(self) -> None:
        """Start timer. If timer is already running reset it."""
        if self._running:
            self.reset()

        self._start = time()
        self._running = True

    def stop(self, ret_string: bool = False) -> float|str:
        """
        Stop timer, reset probe and return elapsed time since self.start() in ms.
        \param ret_string (bool) : if true return the elapsed_time as string like "%M:%S.%f"[:-3]
        """
        if not self._running:
            return 0.0

        self._end = time()
        elapsed_time = self._end - self._start

        self.reset()

        if ret_string:
            value = datetime.fromtimestamp(elapsed_time)
            return value.strftime("%M:%S.%f")[:-3]

        return elapsed_time

    def reset(self) -> None:
        """Reset probe."""
        self._start = 0.0
        self._end = 0.0
        self._running = False
