from .base import BaseTask

class Task(BaseTask):
    name = "inventory"
    asset_types = [
        "Head",
        "Hat",
        "HairAccessory",
        "FaceAccessory",
        "NeckAccessory",
        "ShoulderAccessory",
        "FrontAccessory",
        "BackAccessory",
        "WaistAccessory",
        "Gear",
        "Face"
    ]

    def complete(self):
        inventory = []
        cursor = None
        while 1:
            q = f"assetTypes={','.join(self.asset_types)}&sortOrder=Asc&limit=100"
            if cursor:
                q += f"&cursor={cursor}"
            with self.session.request(
                "GET",
                f"https://inventory.roblox.com/v2/users/{self.session.id}/inventory?{q}"
            ) as resp:
                data = resp.json()
                for item in data.get("data", []):
                    inventory.append(item)
                cursor = data.get("nextPageCursor")
                if not cursor:
                    break
        self.cache.inventory = inventory
        self.cache.complete(self.name)
