from pathlib import Path
from typing import Any

import yaml


CONFIG_PATH = 'config.yaml'


class ConfigError(RuntimeError):
    pass


def load_config(path: str = CONFIG_PATH) -> dict[str, Any]:
    config_file = Path(path)
    if not config_file.exists():
        raise ConfigError('config.yaml not found. Copy config.example.yaml to config.yaml first.')
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    if not isinstance(config, dict):
        raise ConfigError('Invalid YAML config')
    return config


def save_config(config: dict[str, Any], path: str = CONFIG_PATH) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False)


def find_job(config: dict[str, Any], name: str) -> dict[str, Any] | None:
    for job in config.get('jobs', []):
        if job.get('name') == name:
            return job
    return None


def validate_job(job: dict[str, Any]) -> None:
    for field in ['name', 'url', 'backend', 'type']:
        if field not in job:
            raise ConfigError(f'Missing field in job: {field}')
