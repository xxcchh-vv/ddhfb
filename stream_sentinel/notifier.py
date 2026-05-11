import os
import requests


class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

    def enabled(self) -> bool:
        return bool(self.token and self.chat_id)

    def send(self, message: str) -> None:
        if not self.enabled():
            return

        url = f'https://api.telegram.org/bot{self.token}/sendMessage'

        requests.post(
            url,
            json={
                'chat_id': self.chat_id,
                'text': message,
            },
            timeout=20,
        )
