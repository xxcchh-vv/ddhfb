import threading
import time

from runtime import runtime_registry


class Watchdog:
    def __init__(self, interval: int = 60):
        self.interval = interval
        self.thread = None
        self.running = False

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def loop(self):
        while self.running:
            jobs = runtime_registry.list_jobs()

            for job in jobs:
                state = job.get('state')

                if state == 'failed':
                    print(f'[watchdog] failed job detected: {job["name"]}')

            time.sleep(self.interval)

    def stop(self):
        self.running = False


watchdog = Watchdog()
