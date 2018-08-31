# timer.py
# author: Jacob Schwartz (schwartzj1)

import signal
from contextlib import contextmanager


# Timeout call for server requests
class Timer:

    def __init__(self):
        self.sec = 15

    @contextmanager
    def timeout(self):
        signal.signal(signal.SIGALRM, self.raise_tout)

        signal.alarm(self.sec)

        try:
            yield
        except TimeoutError:
            pass
        finally:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)

        return None

    def raise_tout(self, signum, frame):
        raise TimeoutError