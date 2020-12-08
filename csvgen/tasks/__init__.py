from . import robux
from . import premium
from . import collectibles
from . import settings

TASK_MAP = {
    "robux": robux.Task,
    "premium": premium.Task,
    "collectibles": collectibles.Task,
    "settings": settings.Task
}