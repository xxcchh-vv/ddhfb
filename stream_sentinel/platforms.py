from urllib.parse import urlparse


class Platform:
    BILIBILI = 'bilibili'
    DOUYIN = 'douyin'
    YOUTUBE = 'youtube'
    TWITCH = 'twitch'
    GENERIC = 'generic'


def detect_platform(url: str) -> str:
    host = urlparse(url).netloc.lower()

    if 'bilibili.com' in host or 'live.bilibili.com' in host:
        return Platform.BILIBILI
    if 'douyin.com' in host or 'iesdouyin.com' in host:
        return Platform.DOUYIN
    if 'youtube.com' in host or 'youtu.be' in host:
        return Platform.YOUTUBE
    if 'twitch.tv' in host:
        return Platform.TWITCH
    return Platform.GENERIC


SUPPORTED_PLATFORMS = {
    Platform.BILIBILI: 'Bilibili live and video via yt-dlp/streamlink, dedicated adapter planned',
    Platform.DOUYIN: 'Douyin live requires dedicated adapter or browser-cookie based stream extraction',
    Platform.YOUTUBE: 'YouTube supported through yt-dlp',
    Platform.TWITCH: 'Twitch supported through streamlink',
    Platform.GENERIC: 'Generic URL supported if yt-dlp or streamlink supports it',
}
