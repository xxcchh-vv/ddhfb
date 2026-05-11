import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

from transcoder import Transcoder


class DownloadError(RuntimeError):
    pass


MAX_RETRIES = 5
RETRY_DELAY = 30


def require_binary(name: str) -> None:
    if shutil.which(name) is None:
        raise DownloadError(f'Missing required binary: {name}')


def safe_name(name: str) -> str:
    return ''.join(c if c.isalnum() or c in '-_.' else '_' for c in name).strip('_')


def run_command(args: list[str]) -> None:
    process = subprocess.run(args)
    if process.returncode != 0:
        raise DownloadError(f'Command failed with exit code {process.returncode}')


def download_with_ytdlp(job: dict, output_dir: Path) -> None:
    require_binary('yt-dlp')
    require_binary('ffmpeg')

    job_dir = output_dir / safe_name(job['name'])
    job_dir.mkdir(parents=True, exist_ok=True)

    archive = job_dir / 'archive.txt'
    template = str(job_dir / '%(upload_date)s_%(title).120s_%(id)s.%(ext)s')

    args = [
        'yt-dlp',
        job['url'],
        '--download-archive', str(archive),
        '--merge-output-format', 'mp4',
        '-o', template,
        '--no-overwrites',
        '--ignore-errors',
    ]

    run_command(args)


def record_with_streamlink(job: dict, output_dir: Path) -> None:
    require_binary('streamlink')

    job_dir = output_dir / safe_name(job['name'])
    job_dir.mkdir(parents=True, exist_ok=True)

    quality = job.get('quality', 'best')
    retries = 0

    while retries < MAX_RETRIES:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output = job_dir / f'{timestamp}_{safe_name(job["name"])}.ts'

        args = ['streamlink', job['url'], quality, '-o', str(output)]

        process = subprocess.run(args)

        if process.returncode == 0:
            if job.get('auto_transcode', True):
                try:
                    Transcoder.transcode_to_mp4(str(output))
                except Exception:
                    pass
            return

        retries += 1
        time.sleep(RETRY_DELAY)

    raise DownloadError(f'Max retries exceeded for {job["name"]}')


def run_job(job: dict, output_dir: str) -> None:
    backend = job.get('backend', 'yt-dlp')
    base_dir = Path(output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    if backend == 'yt-dlp':
        download_with_ytdlp(job, base_dir)
    elif backend == 'streamlink':
        record_with_streamlink(job, base_dir)
    else:
        raise DownloadError(f'Unsupported backend: {backend}')
