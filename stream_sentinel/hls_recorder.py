import subprocess
from datetime import datetime
from pathlib import Path


class HLSRecorder:
    @staticmethod
    def record(url: str, output_dir: str, stream_name: str):
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        output_template = (
            f'{output_dir}/{stream_name}_{timestamp}_%03d.ts'
        )

        playlist = f'{output_dir}/{stream_name}_{timestamp}.m3u8'

        command = [
            'ffmpeg',
            '-i',
            url,
            '-c',
            'copy',
            '-f',
            'segment',
            '-segment_time',
            '300',
            '-segment_list',
            playlist,
            output_template,
        ]

        return subprocess.run(command)
