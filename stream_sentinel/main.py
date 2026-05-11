import time

from rich import print

from config import ConfigError, load_config, validate_job
from database import Database
from downloader import DownloadError, run_job
from live_check import LiveChecker
from logger import Logger
from runtime import runtime_registry
from state import JobState
from worker_pool import WorkerPool


def handle_job(job: dict, config: dict, db: Database, logger: Logger) -> None:
    validate_job(job)
    name = job['name']
    run_id = db.start_run(name)
    runtime_registry.set_state(name, JobState.CHECKING.value)
    logger.write(name, 'job started')

    try:
        if job.get('type') == 'live' and job.get('check_live', True):
            logger.write(name, 'checking live status')
            if not LiveChecker.is_live(job['url']):
                runtime_registry.set_state(name, JobState.OFFLINE.value)
                db.finish_run(run_id, 'skipped', 'stream is offline')
                logger.write(name, 'stream is offline')
                print(f"[yellow]Offline:[/yellow] {name}")
                return

        if job.get('type') == 'live':
            runtime_registry.set_state(name, JobState.RECORDING.value)
        else:
            runtime_registry.set_state(name, JobState.DOWNLOADING.value)

        run_job(job, config.get('output_dir', './downloads'))

        runtime_registry.set_state(name, JobState.SUCCESS.value)
        db.finish_run(run_id, 'success', 'completed')
        logger.write(name, 'job completed')
        print(f"[green]Finished:[/green] {name}")

    except Exception as e:
        runtime_registry.set_state(name, JobState.FAILED.value)
        db.finish_run(run_id, 'failed', str(e))
        logger.write(name, f'job failed: {e}')
        raise


def run_loop() -> None:
    logger = Logger()

    while True:
        config = load_config()
        interval = int(config.get('interval_seconds', 300))
        jobs = [job for job in config.get('jobs', []) if job.get('enabled', True)]
        db = Database(config.get('database_path', './data/stream_sentinel.db'))
        pool = WorkerPool(int(config.get('workers', 3)))

        print(f'[green]Loaded {len(jobs)} enabled jobs[/green]')

        try:
            pool.run_jobs(jobs, lambda job: handle_job(job, config, db, logger))
        except (ConfigError, DownloadError, Exception) as e:
            print(f'[red]{e}[/red]')

        print(f'[yellow]Sleeping {interval} seconds[/yellow]')
        time.sleep(interval)


if __name__ == '__main__':
    run_loop()
