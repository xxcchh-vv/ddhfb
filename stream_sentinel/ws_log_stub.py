from collections import deque


class RuntimeLogBuffer:
    def __init__(self, max_lines: int = 500):
        self.lines = deque(maxlen=max_lines)

    def push(self, message: str):
        self.lines.append(message)

    def dump(self):
        return list(self.lines)


runtime_logs = RuntimeLogBuffer()
