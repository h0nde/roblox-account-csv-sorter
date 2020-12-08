from .base import BaseTask

class Task(BaseTask):
    name = "credit"

    def complete(self):
        with self.session.request(
            "GET",
            "https://billing.roblox.com/v1/gamecard/userdata"
        ) as resp:
            self.cache.credit = resp.json()
        self.cache.complete(self.name)