from pathlib import Path


class FileManager:
    def __init__(self, root: str = './downloads'):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def list_files(self):
        files = []

        for file in self.root.rglob('*'):
            if file.is_file():
                files.append(
                    {
                        'path': str(file),
                        'size_mb': round(file.stat().st_size / 1024 / 1024, 2),
                    }
                )

        return sorted(files, key=lambda x: x['path'])

    def cleanup_old_segments(self, suffix: str = '.ts'):
        removed = 0

        for file in self.root.rglob(f'*{suffix}'):
            try:
                file.unlink()
                removed += 1
            except Exception:
                pass

        return removed
