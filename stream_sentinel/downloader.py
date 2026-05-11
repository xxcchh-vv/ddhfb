import subprocess
from pathlib import Path


def run_command(command):
    process = subprocess.run(command, shell=True)
    return process.returncode



def download_job(job, output_dir):
    backend = job.get('backend', 'yt-dlp')
    url = job['url']
    name = job['name']

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if backend == 'yt-dlp':
        command = (
            f'yt-dlp "{url}" '
            f'-P "{output_dir}/{name}" '
            '--download-archive archive.txt '
            '--merge-output-format mp4'
        )

    elif backend == 'streamlink':
        command = (
            f'streamlink "{url}" best '
            f'-o "{output_dir}/{name}.ts"'
        )

    else:
        raise ValueError(f'Unsupported backend: {backend}')

    print(command)
    return run_command(command)
