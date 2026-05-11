import time
from dataclasses import dataclass


@dataclass
class StreamCandidate:
    url: str
    quality: int | None = None
    codec: str | None = None
    format: str | None = None
    failed_at: float | None = None
    fail_count: int = 0


class CDNFailover:
    def __init__(self, cooldown_seconds: int = 120):
        self.cooldown_seconds = cooldown_seconds

    def choose(self, candidates: list[dict]) -> StreamCandidate | None:
        if not candidates:
            return None

        sorted_candidates = sorted(
            candidates,
            key=lambda item: (
                item.get('quality') or 0,
                1 if item.get('format') == 'fmp4' else 0,
            ),
            reverse=True,
        )

        item = sorted_candidates[0]
        return StreamCandidate(
            url=item['url'],
            quality=item.get('quality'),
            codec=item.get('codec'),
            format=item.get('format'),
        )

    def mark_failed(self, candidate: StreamCandidate):
        candidate.failed_at = time.time()
        candidate.fail_count += 1
