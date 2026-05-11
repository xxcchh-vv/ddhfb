import shutil
import time
from pathlib import Path


class FileManager:
    def __init__(self, root: str = './downloads'):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def list_files(self):
        files = []

        for file in self.root.rglob('*'):
            if file.is_file():
                stat = file.stat()
                files.append(
                    {
                        'path': str(file),
                        'size_mb': round(stat.st_size / 1024 / 1024, 2),
                        'modified_at': int(stat.st_mtime),
                    }
                )

        return sorted(files, key=lambda x: x['modified_at'], reverse=True)

    def disk_usage(self):
        usage = shutil.disk_usage(self.root)
        return {
            'total_gb': round(usage.total / 1024 / 1024 / 1024, 2),
            'used_gb': round(usage.used / 1024 / 1024 / 1024, 2),
            'free_gb': round(usage.free / 1024 / 1024 / 1024, 2),
        }

    def cleanup_old_segments(self, suffix: str = '.ts'):
        removed = 0

        for file in self.root.rglob(f'*{suffix}'):
            try:
                file.unlink()
                removed += 1
            except Exception:
                pass

        return removed

    def cleanup_older_than_days(self, days: int):
        cutoff = time.time() - days * 86400
        removed = 0

        for file in self.root.rglob('*'):
            if file.is_file() and file.stat().st_mtime < cutoff:
                try:
                    file.unlink()
                    removed += 1
                except Exception:
                    pass

        return removed
