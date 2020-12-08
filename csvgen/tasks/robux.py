from .base import BaseTask

class Task(BaseTask):
    name = "robux"

    def complete(self):
        with self.session.request(
            "GET",
            f"https://economy.roblox.com/v1/users/{self.session.id}/currency"
        ) as resp:
            self.cache.robux = resp.json()["robux"]
        self.cache.complete(self.name)