from enum import Enum


class JobState(str, Enum):
    IDLE = 'idle'
    CHECKING = 'checking'
    OFFLINE = 'offline'
    RECORDING = 'recording'
    DOWNLOADING = 'downloading'
    RECONNECTING = 'reconnecting'
    TRANSCODING = 'transcoding'
    SUCCESS = 'success'
    FAILED = 'failed'
    SKIPPED = 'skipped'
