import threading
import time


class Scheduler:
    def __init__(self):
        self.jobs = {}
        self.running = False

    def register(self, name: str, interval: int, callback):
        self.jobs[name] = {
            'interval': interval,
            'callback': callback,
            'last_run': 0,
        }

    def loop(self):
        self.running = True

        while self.running:
            now = time.time()

            for name, job in self.jobs.items():
                if now - job['last_run'] >= job['interval']:
                    threading.Thread(target=job['callback'], daemon=True).start()
                    job['last_run'] = now

            time.sleep(1)

    def start(self):
        threading.Thread(target=self.loop, daemon=True).start()

    def stop(self):
        self.running = False
