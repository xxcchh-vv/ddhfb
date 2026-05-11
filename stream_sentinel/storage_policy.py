from file_manager import FileManager


class StoragePolicy:
    def __init__(self, manager: FileManager):
        self.manager = manager

    def enforce(self, min_free_gb: float = 10.0, cleanup_days: int = 7):
        usage = self.manager.disk_usage()

        if usage['free_gb'] < min_free_gb:
            removed = self.manager.cleanup_older_than_days(cleanup_days)
            return {
                'cleanup_triggered': True,
                'removed_files': removed,
            }

        return {
            'cleanup_triggered': False,
            'removed_files': 0,
        }
