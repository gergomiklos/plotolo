import threading
from plotolo.session.widget_state import CellInfo


class SessionContext:
    """
    Communication bridge between the ScriptRunner and the SessionHandler
    """
    def __init__(self, session_id, script_id, send_widget, get_data, set_data):
        self.session_id = session_id
        self.script_id = script_id
        self.send_widget = send_widget
        self.get_data = get_data
        self.set_data = set_data


class RunContext:
    """
    Script execution scope (per websocket message):
    Necessary elements for the running script on its own thread,
    to be able to get user's input and send output
    """
    RUN_CONTEXT_ATTR = 'RUN_CONTEXT_ATTR'

    def __init__(self, session_context: SessionContext, cell_info: CellInfo):
        self.session_context: SessionContext = session_context
        self.cell_info: CellInfo = cell_info  # the up-to-date script/cell/widget indexes
        self.rerun = False  # if it is set to True, a new script execution already started on a different thread


def set_run_context(ctx: RunContext, thread: threading.Thread | None = None):
    if thread is None:
        thread = threading.current_thread()

    setattr(thread, RunContext.RUN_CONTEXT_ATTR, ctx)


def get_run_context(thread: threading.Thread | None = None) -> RunContext:
    if thread is None:
        thread = threading.current_thread()

    return getattr(thread, RunContext.RUN_CONTEXT_ATTR)
