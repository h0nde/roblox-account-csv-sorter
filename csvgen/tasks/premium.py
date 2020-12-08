from .base import BaseTask

class Task(BaseTask):
    name = "premium"

    def complete(self):
        with self.session.request(
            "GET",
            f"https://premiumfeatures.roblox.com/v1/users/{self.session.id}/subscriptions"
        ) as resp:
            data = resp.json().get("subscriptionProductModel")
            if data:
                self.cache.premium_stipend = data["robuxStipendAmount"]
                self.cache.premium_expiry_date = data["expiration"]
        self.cache.complete(self.name)