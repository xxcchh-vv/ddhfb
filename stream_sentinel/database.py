import sqlite3
from contextlib import closing
from pathlib import Path


SCHEMA = '''
CREATE TABLE IF NOT EXISTS job_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name TEXT NOT NULL,
    status TEXT NOT NULL,
    message TEXT,
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at TEXT
);

CREATE TABLE IF NOT EXISTS downloaded_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name TEXT NOT NULL,
    item_key TEXT NOT NULL,
    file_path TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(job_name, item_key)
);
'''


class Database:
    def __init__(self, path: str = './data/stream_sentinel.db'):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.init_schema()

    def connect(self):
        return sqlite3.connect(self.path)

    def init_schema(self) -> None:
        with closing(self.connect()) as conn:
            conn.executescript(SCHEMA)
            conn.commit()

    def start_run(self, job_name: str) -> int:
        with closing(self.connect()) as conn:
            cursor = conn.execute(
                'INSERT INTO job_runs(job_name, status) VALUES (?, ?)',
                (job_name, 'running'),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def finish_run(self, run_id: int, status: str, message: str = '') -> None:
        with closing(self.connect()) as conn:
            conn.execute(
                'UPDATE job_runs SET status = ?, message = ?, finished_at = CURRENT_TIMESTAMP WHERE id = ?',
                (status, message, run_id),
            )
            conn.commit()

    def has_item(self, job_name: str, item_key: str) -> bool:
        with closing(self.connect()) as conn:
            row = conn.execute(
                'SELECT 1 FROM downloaded_items WHERE job_name = ? AND item_key = ?',
                (job_name, item_key),
            ).fetchone()
            return row is not None

    def add_item(self, job_name: str, item_key: str, file_path: str = '') -> None:
        with closing(self.connect()) as conn:
            conn.execute(
                'INSERT OR IGNORE INTO downloaded_items(job_name, item_key, file_path) VALUES (?, ?, ?)',
                (job_name, item_key, file_path),
            )
            conn.commit()
