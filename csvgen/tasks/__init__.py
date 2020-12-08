from . import robux
from . import premium
from . import collectibles
from . import settings
from . import pin
from . import groups
from . import credit
from . import inventory

TASK_MAP = {
    "robux": robux.Task,
    "premium": premium.Task,
    "collectibles": collectibles.Task,
    "settings": settings.Task,
    "pin": pin.Task,
    "groups": groups.Task,
    "credit": credit.Task,
    "inventory": inventory.Task
}