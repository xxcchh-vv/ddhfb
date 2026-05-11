import time
import yaml
from rich import print
from downloader import download_job


def load_config(path='config.yaml'):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def run_loop():
    config = load_config()
    interval = config.get('interval_seconds', 300)
    jobs = config.get('jobs', [])

    print(f'[green]Loaded {len(jobs)} jobs[/green]')

    while True:
        for job in jobs:
            if not job.get('enabled', True):
                continue

            try:
                print(f"[cyan]Checking:[/cyan] {job['name']}")
                download_job(job, config.get('output_dir', './downloads'))
            except Exception as e:
                print(f'[red]{e}[/red]')

        time.sleep(interval)


if __name__ == '__main__':
    run_loop()
