import re
import requests


class BilibiliLiveAdapter:
    API_ROOM_INIT = 'https://api.live.bilibili.com/room/v1/Room/room_init?id={room_id}'
    API_ROOM_INFO = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id={room_id}'

    @staticmethod
    def parse_room_id(url: str) -> str:
        match = re.search(r'live\.bilibili\.com/(\d+)', url)
        if not match:
            raise ValueError('Invalid Bilibili live room URL')
        return match.group(1)

    @classmethod
    def resolve_room_id(cls, room_id: str) -> str:
        resp = requests.get(cls.API_ROOM_INIT.format(room_id=room_id), timeout=10)
        resp.raise_for_status()
        data = resp.json().get('data', {})
        return str(data.get('room_id') or room_id)

    @classmethod
    def get_room_info(cls, url: str) -> dict:
        short_id = cls.parse_room_id(url)
        room_id = cls.resolve_room_id(short_id)

        resp = requests.get(cls.API_ROOM_INFO.format(room_id=room_id), timeout=10)
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
