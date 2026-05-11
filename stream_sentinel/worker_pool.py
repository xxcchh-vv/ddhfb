from concurrent.futures import ThreadPoolExecutor, as_completed


class WorkerPool:
    def __init__(self, workers: int = 3):
        self.executor = ThreadPoolExecutor(max_workers=workers)

    def run_jobs(self, jobs, handler):
        futures = []

        for job in jobs:
            futures.append(self.executor.submit(handler, job))

        for future in as_completed(futures):
            future.result()
