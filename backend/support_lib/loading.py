import sys
import threading
import time


class Spinner:
    """
    Simple CLI loading spinner:
    / | \\ -
    Usage:
        spinner = Spinner("Processing")
        spinner.start()
        ... long task ...
        spinner.stop()
    """

    def __init__(self, message="Loading"):
        self.message = message
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin, daemon=True)

    def _spin(self):
        spinner_chars = ["/", "|", "\\", "-"]
        idx = 0

        while not self._stop_event.is_set():
            char = spinner_chars[idx % len(spinner_chars)]
            sys.stdout.write(f"\r{self.message} {char}")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)

        # clear line when done
        sys.stdout.write("\r" + " " * (len(self.message) + 4) + "\r")
        sys.stdout.flush()

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()
