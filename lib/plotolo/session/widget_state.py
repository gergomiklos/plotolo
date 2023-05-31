import time
import threading
from enum import Enum


class WidgetStatus(Enum):
    PENDING = 'PENDING'
    UPDATED = 'UPDATED'
    UNCHANGED = 'UNCHANGED'
    DELETED = 'DELETED'

    def __json__(self):
        return self.value


class WidgetAction(Enum):
    RUN_CELL = 'RUN_CELL'
    RUN_ALL = 'RUN_ALL'
    RUN_ALL_BELOW = 'RUN_ALL_BELOW'
    NONE = 'NONE'

    def __json__(self):
        return self.value


class CellInfo:
    """
    Internal model for storing cell info of widget state
    """
    def __init__(self, cell_id: str = None, cell_index=-1, widget_index=-1, script_run_index=-1):
        self.cell_id = cell_id
        self.cell_index = cell_index
        self.widget_index = widget_index
        self.script_run_index = script_run_index


class WidgetState:
    """
    Internal model for storing widget state (without actual widget data, only hashes)
    """
    def __init__(self, id: str, type: str, status: WidgetStatus, action: WidgetAction, cell_info: CellInfo,
                 hash_state: dict[str, str]):
        self.id = id
        self.type = type
        self.status: WidgetStatus = status
        self.action: WidgetAction = action
        self.cell_info: CellInfo = cell_info
        self.hash_state: dict[str, str] = hash_state  # [key: hash] state of the widget
        self.updated = time.time()
        self.lock = threading.Lock()
