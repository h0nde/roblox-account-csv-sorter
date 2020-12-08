from .base import BaseTask

class Task(BaseTask):
    name = "pin"

    def complete(self):
        with self.session.request(
            "GET",
            "https://auth.roblox.com/v1/account/pin"
        ) as resp:
            data = resp.json()
            self.cache.pin_enabled = data["isEnabled"]
        self.cache.complete(self.name)