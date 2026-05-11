import re
from metrics import metrics_registry


class FFmpegMonitor:
    SPEED_RE = re.compile(r'speed=\s*([0-9\.]+)x')
    BITRATE_RE = re.compile(r'bitrate=\s*([0-9\.kmg]+bits/s)')

    @classmethod
    def parse_line(cls, job_name: str, line: str):
        speed_match = cls.SPEED_RE.search(line)
        bitrate_match = cls.BITRATE_RE.search(line)

        updates = {}

        if speed_match:
            updates['speed'] = speed_match.group(1)

        if bitrate_match:
            updates['bitrate'] = bitrate_match.group(1)

        if updates:
            metrics_registry.update(job_name, **updates)
