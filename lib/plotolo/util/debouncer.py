import threading
import time

from tornado.ioloop import IOLoop


class Debouncer:
    """
    "Debounces" a function so that is called after a waiting time.
    If the debouncer called again during the waiting time,
    the waiting time will be reset for the last call.
    An optional maximum waiting time can be set for the actual call.
    """

    def __init__(self, ioloop: IOLoop, wait_time, max_wait_time=None):
        self.wait_time_secs = wait_time
        self.max_wait_time_secs = max_wait_time
        self.ioloop: IOLoop = ioloop
        self.first_call_time = None
        self.timer = None

    def _is_waiting_expired(self):
        if self.max_wait_time_secs:
            return (time.time() - self.first_call_time) > self.max_wait_time_secs
        else:
            return False

    def call(self, function, *args, **kwargs):
        def call_function():
            self.first_call_time = None
            function(*args, **kwargs)

        if self.timer:
            self.timer.cancel()

        if not self.first_call_time:
            self.first_call_time = time.time()

        if self._is_waiting_expired():
            call_function()
        else:
            self.timer = threading.Timer(self.wait_time_secs, call_function)
            self.timer.start()
