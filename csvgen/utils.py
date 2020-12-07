import re
import time
import ctypes
import json
from managers import ConnectionManager
from queue import Queue

_CMT = r"\_\|WARNING:?-DO-NOT-SHARE-THIS\.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items\.\|\_"
C_RE = re.compile(r"^(?:" + _CMT + r")?([A-F0-9]{300,})$")
UPC_RE = re.compile(r"^(?:[A-z0-9]{2,50}):([^:]{3,}):(?:" + _CMT + r")?([A-F0-9]{300,})$")

set_title = ctypes.windll.kernel32.SetConsoleTitleW

def line_to_combo(line: str) -> tuple:
    if m := UPC_RE.match(line):
        return (m.group(2), m.group(1))
    
    elif m := C_RE.match(line):
        return (m.group(1), None)

def load_combos(path: str) -> Queue:
    with open(path, encoding="UTF-8", errors="ignore") as f:
        q = Queue()
        lines = f.read().splitlines()
        lines = list(set(lines))
        for line in lines:
            if (combo := line_to_combo(line)):
                q.put(combo)
        return q

def format_collectibles(collectibles: list, values: dict = None):
    collectibles.sort(
        key=lambda i: i.get("recentAveragePrice", 0),
        reverse=True
    )
    return ", ".join([
        "%s (%d RAP%s)" % (
            i["name"],
            i.get("recentAveragePrice", 0),
            ", %d VAL%s" % (
                values[i["assetId"]]["value"],
                " [PROJ]" if values[i["assetId"]]["projected"] else ""
            ) if values and i["assetId"] in values else ""
        )
        for i in collectibles
    ])

def get_rolimons():
    with ConnectionManager() as cm:
        resp = cm.request("GET", "https://www.rolimons.com/catalog", headers={"User-Agent": "CSVGen"})
        data = resp.text.split("item_details = ")[1].split("\n")[0].rstrip(";")
        data = json.loads(data)
        data = {
            int(aid): {
                "value": d[-1],
                "projected": d[19] == 1
            }
            for aid, d in data.items()
        }
        return data

class Counter:
    def __init__(self):
        self.timeframe = 60
        self._points = []
        self.total = 0
    
    def add(self):
        self.total += 1
        self._points.append(time.time())
    
    def _filter_points(self):
        self._points = list(filter(
            lambda p: (time.time()-p)<=60,
            self._points))
           
    def cpm(self) -> int:
        self._filter_points()
        return len(self._points)
