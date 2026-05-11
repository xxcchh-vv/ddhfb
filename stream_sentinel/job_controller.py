import threading

from runtime import runtime_registry


class JobController:
    def __init__(self):
        self._threads: dict[str, threading.Thread] = {}

    def register(self, job_name: str, thread: threading.Thread):
        self._threads[job_name] = thread

    def stop(self, job_name: str):
        runtime_registry.request_stop(job_name)

    def is_running(self, job_name: str) -> bool:
        thread = self._threads.get(job_name)
        return bool(thread and thread.is_alive())


job_controller = JobController()
