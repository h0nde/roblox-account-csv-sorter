from managers import ConnectionManager
from urllib.parse import urlencode, urlparse
import json
import time

def raise_errors(response):
    if response.headers.get("content-type", "").startswith("application/json"):
        for err in response.json().get("errors", []):
            raise APIError(err["code"], err["message"], response)

class APIError(Exception):
    code: int
    message: str
    response: "Response"

    def __init__(self, code, message, response):
        self.code = code
        self.message = message
        self.response = response

class PunishmentRedirect(Exception):
    pass

class PunishmentDeactivationFailed(Exception):
    pass

class RobloxSession:
    def __init__(self, cookie, user_agent=None, manager=None, **kw):
        self.cookies = {
            ".ROBLOSECURITY": cookie
        }
        self.headers = {
            "User-Agent": user_agent,
            "Origin": "https://www.roblox.com",
            "Referer": "https://www.roblox.com/"
        }
        self.xsrf_token = None
        self.id = None
        self.name = None
        self.display_name = None
        self.above_13 = True
        self._manager = manager or ConnectionManager(**kw)

    def close(self):
        self._manager.clear()

    def _cookie_header(self):
        headers = {}
        if self.cookies:
            headers["Cookie"] = "; ".join(
                f"{k}={v}"
                for k,v in self.cookies.items()
            )
        return headers

    def request(self, method, url, data=None, json=None, headers={}):
        if not self.above_13:
            url = url.replace("www.", "web.")

        headers = {**self.headers, **self._cookie_header(), **headers}

        if json:
            data = json.dumps(json, seperators=(",", ":"))
            headers["Content-Type"] = "application/json"
        elif type(data) == dict:
            data = urlencode(data)
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        if self.xsrf_token and method in ["POST", "PUT", "PATCH", "DELETE"]:
            headers["X-CSRF-TOKEN"] = self.xsrf_token

        resp = self._manager.request(method, url, data, headers)

        if "location" in resp.headers:
            if resp.headers["location"].startswith("https://web.") and self.above_13:
                self.above_13 = False
                if "/not-approved" in resp.headers["location"]:
                    raise PunishmentRedirect
                return self.request(method, resp.headers["location"], data, json, headers)
            elif "/not-approved" in resp.headers["location"]:
                raise PunishmentRedirect
        
        if (new_xsrf := resp.headers.get("x-csrf-token")):
            self.xsrf_token = new_xsrf
            return self.request(method, url, data, json, headers)

        raise_errors(resp)
        return resp
    
    def setup(self):
        self.request("HEAD", "https://www.roblox.com/home")
        with self.request(
            "GET",
            "https://users.roblox.com/v1/users/authenticated"
        ) as resp:
            data = resp.json()
            self.id = data["id"]
            self.name = data["name"]
            self.display_name = data["displayName"]

    def reactivate(self):
        print(self.cookies)