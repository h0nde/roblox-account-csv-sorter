from .base import BaseTask

class Task(BaseTask):
    name = "settings"

    def complete(self):
        with self.session.request(
            "GET",
            "https://www.roblox.com/my/settings/json"
        ) as resp:
            data = resp.json()
            self.cache.admin = data["IsAdmin"]
            self.cache.email_address = data["UserEmail"]
            self.cache.email_verified = data["IsEmailVerified"]
            self.cache.above_13 = data["UserAbove13"]
            self.cache.previous_names = [x for x in data["PreviousUserNames"].split(", ") if x]
        self.cache.complete(self.name)