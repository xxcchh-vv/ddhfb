import time
from pathlib import Path

import yaml
from rich import print

from database import Database
from downloader import DownloadError, run_job
from live_check import LiveChecker
from worker_pool import WorkerPool


CONFIG_PATH = 'config.yaml'


class ConfigError(RuntimeError):
    pass


def load_config(path: str = CONFIG_PATH) -> dict:
    config_file = Path(path)
    if not config_file.exists():
        raise ConfigError('config.yaml not found. Copy config.example.yaml to config.yaml first.')
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    if not isinstance(config, dict):
        raise ConfigError('Invalid YAML config')
    return config


def validate_job(job: dict) -> None:
    for field in ['name', 'url', 'backend', 'type']:
        if field not in job:
            raise ConfigError(f'Missing field in job: {field}')


def handle_job(job: dict, config: dict, db: Database) -> None:
    validate_job(job)
    run_id = db.start_run(job['name'])

    try:
        if job.get('type') == 'live' and job.get('check_live', True):
            if not LiveChecker.is_live(job['url']):
                db.finish_run(run_id, 'skipped', 'stream is offline')
                print(f"[yellow]Offline:[/yellow] {job['name']}")
                return

        run_job(job, config.get('output_dir', './downloads'))
        db.finish_run(run_id, 'success', 'completed')
        print(f"[green]Finished:[/green] {job['name']}")

    except Exception as e:
        db.finish_run(run_id, 'failed', str(e))
        raise


def run_loop() -> None:
    config = load_config()
    interval = int(config.get('interval_seconds', 300))
    jobs = [job for job in config.get('jobs', []) if job.get('enabled', True)]
    db = Database(config.get('database_path', './data/stream_sentinel.db'))
    pool = WorkerPool(int(config.get('workers', 3)))

    print(f'[green]Loaded {len(jobs)} enabled jobs[/green]')

    while True:
        try:
            pool.run_jobs(jobs, lambda job: handle_job(job, config, db))
        except (ConfigError, DownloadError, Exception) as e:
            print(f'[red]{e}[/red]')

        print(f'[yellow]Sleeping {interval} seconds[/yellow]')
        time.sleep(interval)


if __name__ == '__main__':
    run_loop()
