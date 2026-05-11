from dataclasses import dataclass, asdict
from datetime import datetime
from threading import Lock


@dataclass
class JobMetrics:
    job_name: str
    reconnects: int = 0
    segments: int = 0
    last_error: str = ''
    bitrate: str = ''
    speed: str = ''
    updated_at: str = ''


class MetricsRegistry:
    def __init__(self):
        self._lock = Lock()
        self._items: dict[str, JobMetrics] = {}

    def ensure(self, job_name: str) -> JobMetrics:
        with self._lock:
            if job_name not in self._items:
                self._items[job_name] = JobMetrics(job_name=job_name)
            return self._items[job_name]

    def update(self, job_name: str, **kwargs):
        item = self.ensure(job_name)
        with self._lock:
            for key, value in kwargs.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            item.updated_at = datetime.now().isoformat(timespec='seconds')

    def increment(self, job_name: str, field: str, amount: int = 1):
        item = self.ensure(job_name)
        with self._lock:
            setattr(item, field, getattr(item, field) + amount)
            item.updated_at = datetime.now().isoformat(timespec='seconds')

    def list(self):
        with self._lock:
            return [asdict(item) for item in self._items.values()]


metrics_registry = MetricsRegistry()
