from .base import BaseTask

class Task(BaseTask):
    name = "groups"

    def complete(self):
        groups = []
        with self.session.request(
            "GET",
            f"https://groups.roblox.com/v2/users/{self.session.id}/groups/roles"
        ) as resp:
            data = resp.json()["data"]
            for item in data:
                item["group"]["owner"] = self.session.request(
                    "GET",
                    f"https://groups.roblox.com/v1/groups/{item['group']['id']}"
                ).json().get("owner")
                item["group"]["robux"] = 0
                if item["role"]["rank"] >= 255:
                    with self.session.request(
                        "GET",
                        f"https://economy.roblox.com/v1/groups/{item['group']['id']}/currency"
                    ) as resp:
                        item["group"]["robux"] = resp.json().get("robux", 0)
                groups.append(item)
        self.cache.groups = groups
        self.cache.complete(self.name)