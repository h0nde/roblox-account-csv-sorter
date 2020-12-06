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

        if (new_xsrf := resp.headers.get("x-csrf-token")):
            self.xsrf_token = new_xsrf
            return self.request(method, url, data, json, headers)

        raise_errors(resp)
        return resp
    
    def setup(self):
        with self.request(
            "GET",
            "https://users.roblox.com/v1/users/authenticated"
        ) as resp:
            data = resp.json()
            self.id = data["id"]
            self.name = data["name"]
            self.display_name = data["displayName"]