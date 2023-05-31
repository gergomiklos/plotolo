from enum import Enum


class ScriptStatus(Enum):
    RUNNING = 'RUNNING'
    STOPPED = 'STOPPED'


    def __json__(self):
        return self.value


class ScriptState:
    """
    Information about the execution status and errors of a Python Notebook script
    """


    def __init__(self):
        self.status = ScriptStatus.STOPPED
        self.errors = []

