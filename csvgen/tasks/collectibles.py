from .base import BaseTask

class Task(BaseTask):
    name = "collectibles"

    def complete(self):
        collectibles = []
        cursor = None
        while 1:
            q = "assetType=All&sortOrder=Asc&limit=100"
            if cursor:
                q += f"&cursor={cursor}"
            with self.session.request(
                "GET",
                f"https://inventory.roblox.com/v1/users/{self.session.id}/assets/collectibles?{q}"
            ) as resp:
                data = resp.json()
                for item in data.get("data", []):
                    collectibles.append(item)
                cursor = data.get("nextPageCursor")
                if not cursor:
                    break
        self.cache.collectibles = collectibles
        self.cache.complete(self.name)