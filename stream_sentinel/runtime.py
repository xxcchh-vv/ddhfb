import threading
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class RuntimeJob:
    name: str
    state: str = 'idle'
    started_at: Optional[str] = None
    updated_at: Optional[str] = None
    process: Optional[subprocess.Popen] = None
    stop_event: threading.Event = field(default_factory=threading.Event)


class RuntimeRegistry:
    def __init__(self):
        self._lock = threading.Lock()
        self._jobs: dict[str, RuntimeJob] = {}

    def ensure(self, name: str) -> RuntimeJob:
        with self._lock:
            if name not in self._jobs:
                self._jobs[name] = RuntimeJob(name=name)
            return self._jobs[name]

    def set_state(self, name: str, state: str):
        job = self.ensure(name)
        with self._lock:
            now = datetime.now().isoformat(timespec='seconds')
            job.state = state
            job.updated_at = now
            if state in {'recording', 'downloading'} and not job.started_at:
                job.started_at = now

    def request_stop(self, name: str):
        job = self.ensure(name)
        job.stop_event.set()
        if job.process and job.process.poll() is None:
            job.process.terminate()

    def list_jobs(self):
        with self._lock:
            return [
                {
                    'name': job.name,
                    'state': job.state,
                    'started_at': job.started_at,
                    'updated_at': job.updated_at,
                }
                for job in self._jobs.values()
            ]


runtime_registry = RuntimeRegistry()
