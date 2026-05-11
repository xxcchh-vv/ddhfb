import subprocess
import time
from datetime import datetime
from pathlib import Path


MAX_RECONNECTS = 10
RECONNECT_DELAY = 15


class HLSRecorder:
    @staticmethod
    def record(url: str, output_dir: str, stream_name: str):
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        reconnects = 0

        while reconnects < MAX_RECONNECTS:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            output_template = (
                f'{output_dir}/{stream_name}_{timestamp}_%03d.ts'
            )

            playlist = f'{output_dir}/{stream_name}_{timestamp}.m3u8'

            command = [
                'ffmpeg',
                '-y',
                '-i',
                url,
                '-c',
                'copy',
                '-f',
                'segment',
                '-segment_time',
                '300',
                '-reset_timestamps',
                '1',
                '-segment_list',
                playlist,
                output_template,
            ]

            process = subprocess.run(command)

            if process.returncode == 0:
                return

            reconnects += 1
            time.sleep(RECONNECT_DELAY)

        raise RuntimeError('HLS recorder exceeded reconnect limit')
