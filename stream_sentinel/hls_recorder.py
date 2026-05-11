import subprocess
import time
from datetime import datetime
from pathlib import Path

from metrics import metrics_registry

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
                '-reconnect', '1',
                '-reconnect_streamed', '1',
                '-reconnect_delay_max', '5',
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
                metrics_registry.increment(stream_name, 'segments')
                return

            reconnects += 1

            metrics_registry.increment(stream_name, 'reconnects')
            metrics_registry.update(
                stream_name,
                last_error=f'ffmpeg exited with code {process.returncode}',
            )

            time.sleep(RECONNECT_DELAY)

        raise RuntimeError('HLS recorder exceeded reconnect limit')
