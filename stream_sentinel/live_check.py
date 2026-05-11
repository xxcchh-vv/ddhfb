import json
import subprocess

from adapters.bilibili import BilibiliLiveAdapter
from platforms import Platform, detect_platform


class LiveCheckError(RuntimeError):
    pass


class LiveChecker:
    @staticmethod
    def is_live(url: str) -> bool:
        platform = detect_platform(url)

        if platform == Platform.BILIBILI:
            try:
                room = BilibiliLiveAdapter.get_room_info(url)
                return bool(room.get('is_live'))
            except Exception:
                pass

        command = [
            'yt-dlp',
            '--dump-json',
            '--skip-download',
            url,
        ]

        process = subprocess.run(command, capture_output=True, text=True)

        if process.returncode != 0:
            return False

        try:
            data = json.loads(process.stdout.splitlines()[0])
        except Exception:
            return False

        live_status = data.get('live_status')
        is_live = data.get('is_live', False)

        return bool(is_live or live_status == 'is_live')
