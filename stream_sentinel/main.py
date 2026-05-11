import time
from pathlib import Path

import yaml
from rich import print

from downloader import DownloadError, run_job


CONFIG_PATH = 'config.yaml'


class ConfigError(RuntimeError):
    pass


def load_config(path: str = CONFIG_PATH) -> dict:
    config_file = Path(path)

    if not config_file.exists():
        raise ConfigError(
            'config.yaml not found. Copy config.example.yaml to config.yaml first.'
        )

    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ConfigError('Invalid YAML config')

    return config


def validate_job(job: dict) -> None:
    required = ['name', 'url', 'backend']

    for field in required:
        if field not in job:
            raise ConfigError(f'Missing field in job: {field}')


def run_loop() -> None:
    config = load_config()

    interval = int(config.get('interval_seconds', 300))
    output_dir = config.get('output_dir', './downloads')
    jobs = config.get('jobs', [])

    print(f'[green]Loaded {len(jobs)} jobs[/green]')

    while True:
        for job in jobs:
            try:
                if not job.get('enabled', True):
                    continue

                validate_job(job)

                print(f"[cyan]Running:[/cyan] {job['name']}")
                run_job(job, output_dir)
                print(f"[green]Finished:[/green] {job['name']}")

            except (ConfigError, DownloadError, Exception) as e:
                print(f'[red]{e}[/red]')

        print(f'[yellow]Sleeping {interval} seconds[/yellow]')
        time.sleep(interval)


if __name__ == '__main__':
    run_loop()
