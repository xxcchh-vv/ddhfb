import re
import requests


class BilibiliLiveAdapter:
    API_ROOM_INIT = 'https://api.live.bilibili.com/room/v1/Room/room_init?id={room_id}'
    API_ROOM_INFO = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id={room_id}'
    API_PLAY_URL = 'https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo'

    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 StreamSentinel/1.0',
        'Referer': 'https://live.bilibili.com/',
    }

    @staticmethod
    def parse_room_id(url: str) -> str:
        match = re.search(r'live\.bilibili\.com/(\d+)', url)
        if not match:
            raise ValueError('Invalid Bilibili live room URL')
        return match.group(1)

    @classmethod
    def resolve_room_id(cls, room_id: str) -> str:
        resp = requests.get(
            cls.API_ROOM_INIT.format(room_id=room_id),
            headers=cls.DEFAULT_HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json().get('data', {})
        return str(data.get('room_id') or room_id)

    @classmethod
    def get_room_info(cls, url: str) -> dict:
        short_id = cls.parse_room_id(url)
        room_id = cls.resolve_room_id(short_id)

        resp = requests.get(
            cls.API_ROOM_INFO.format(room_id=room_id),
            headers=cls.DEFAULT_HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json().get('data', {})
        room_info = data.get('room_info', {})
        anchor_info = data.get('anchor_info', {}).get('base_info', {})

        return {
            'platform': 'bilibili',
            'short_room_id': short_id,
            'room_id': room_id,
            'title': room_info.get('title'),
            'live_status': room_info.get('live_status'),
            'is_live': room_info.get('live_status') == 1,
            'uname': anchor_info.get('uname'),
        }

    @classmethod
    def get_play_urls(cls, url: str, qn: int = 10000) -> list[dict]:
        room_id = cls.resolve_room_id(cls.parse_room_id(url))
        params = {
            'room_id': room_id,
            'protocol': '0,1',
            'format': '0,1,2',
            'codec': '0,1',
            'qn': qn,
            'platform': 'web',
            'ptype': 8,
        }

        resp = requests.get(
            cls.API_PLAY_URL,
            params=params,
            headers=cls.DEFAULT_HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json().get('data', {})
        streams = data.get('playurl_info', {}).get('playurl', {}).get('stream', [])

        urls = []

        for stream in streams:
            for fmt in stream.get('format', []):
                for codec in fmt.get('codec', []):
                    base_url = codec.get('base_url')
                    for info in codec.get('url_info', []):
                        host = info.get('host')
                        extra = info.get('extra')
                        if host and base_url:
                            urls.append(
                                {
                                    'url': host + base_url + (extra or ''),
                                    'quality': codec.get('current_qn'),
                                    'codec': codec.get('codec_name'),
                                    'format': fmt.get('format_name'),
                                }
                            )

        return urls

    @classmethod
    def get_best_play_url(cls, url: str) -> str | None:
        urls = cls.get_play_urls(url)
        if not urls:
            return None
        return urls[0]['url']
