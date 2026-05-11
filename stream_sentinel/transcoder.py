import shutil
import subprocess
from pathlib import Path


class TranscodeError(RuntimeError):
    pass


class Transcoder:
    @staticmethod
    def transcode_to_mp4(input_file: str):
        if shutil.which('ffmpeg') is None:
            raise TranscodeError('ffmpeg not installed')

        input_path = Path(input_file)

        if not input_path.exists():
            raise TranscodeError('input file missing')

        output_file = input_path.with_suffix('.mp4')

        command = [
            'ffmpeg',
            '-y',
            '-i',
            str(input_path),
            '-c:v',
            'copy',
            '-c:a',
            'aac',
            str(output_file),
        ]

        process = subprocess.run(command)

        if process.returncode != 0:
            raise TranscodeError('ffmpeg transcode failed')

        return str(output_file)
