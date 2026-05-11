from datetime import datetime
from pathlib import Path

from ws_log_stub import runtime_logs


class Logger:
    def __init__(self, log_dir: str = './logs'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def write(self, job_name: str, message: str):
        file_path = self.log_dir / f'{job_name}.log'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        line = f'[{timestamp}] [{job_name}] {message}'

        runtime_logs.push(line)

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
