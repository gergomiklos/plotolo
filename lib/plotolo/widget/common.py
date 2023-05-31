import os
import threading
from copy import copy
from enum import Enum

from plotolo.util.constant import PLOTOLO_SCRIPT_THREAD_PREFIX
from plotolo.util.util import hash_string, hash_object
from plotolo.session.widget_state import WidgetAction as Action
from plotolo.script.script_context import get_run_context
from plotolo.config import ROOT_SESSION_DIR, ROOT_SCRIPT_DIR
from plotolo.widget.embedded import embedded_widget, EmbeddedConfig, EmbeddedDataStorage, embedded_save


class StopExecutionException(Exception):
    """
    Exception to stop the execution of the script.
    """
    def __init__(self, clear_all_outputs_bellow: bool = False):
        super().__init__()
        self.clear_all_outputs_bellow = clear_all_outputs_bellow


class Widget:
    """
    Base class for all widget types.
    """
    def __init__(self, id: str | int, type: str, action: Action, data: dict[str, any]):
        self.id = id
        self.type = type
        self.action = action
        self.data = data


def is_server_mode():
    """
    Returns the current app mode (SERVER or INLINE):
     - SERVER: the app is served from a server session, should send/receive updates to/from the frontend.
     - EMBEDDED: the app is served from a live notebook session, should send/receive from ipy widgets.
    """
    return threading.current_thread().name.startswith(PLOTOLO_SCRIPT_THREAD_PREFIX)


def base_widget(_widget: Widget):
    """
    Base widget function, should be used by all widget functions.
    It handles whether to send the widget to the frontend or display inside the Notebook.
    """
    if is_server_mode():
        return server_widget(**_widget.__dict__)
    else:
        return embedded_widget(**_widget.__dict__)


def server_widget(id: str | int, type: str, data: dict[str, any], action: Action | str = Action.RUN_ALL_BELOW) -> dict[
    str, any]:
    """
    Sends a widget update to the frontend and returns the updated data.
    """
    if not isinstance(id, str):
        id = str(id)

    if isinstance(action, str):
        if action.upper() == 'RUN_CELLS_BELOW':
            action = Action.RUN_ALL_BELOW
        action = Action(action.upper())

    run_context = get_run_context()
    # a new script rerun already started, so should not send any updates
    if run_context.rerun:
        return data

    run_context.cell_info.widget_index += 1

    return run_context.session_context.send_widget(
        id=hash_string(id),
        type=type,
        action=action,
        cell_info=copy(run_context.cell_info),
        data=data,
    )


class PathScope(Enum):
    USER = 'USER'
    APP = 'APP'


def path(filepath: str = '', scope: str | PathScope = PathScope.USER):
    """
    Returns the absolute path of a file based on the given scope (USER or APP).
    """

    if not is_server_mode() or is_server_path(filepath):
        return filepath

    if isinstance(scope, str):
        scope = PathScope(scope.upper())

    if filepath.startswith('./'):
        filepath = filepath[2:]

    run_context = get_run_context()
    if scope == PathScope.USER:
        session_id = run_context.session_context.session_id
        directory = os.path.join(ROOT_SESSION_DIR, session_id)
    else:
        script_id = run_context.session_context.script_id
        directory = os.path.join(ROOT_SCRIPT_DIR, script_id)

    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    return os.path.join(directory, filepath)

    # security risk (?):
    # sys.path.append(os.path.join(ROOT_FILE_DIR, session_id))


def repath(path: str) -> str:
    """
    Returns the relative path of a file based on the current session or script.
    Useful for removing the effect of the 'path' function.
    """
    if not is_server_mode() or not is_server_path(path):
        return path

    run_context = get_run_context()
    session_id = run_context.session_context.session_id
    script_id = run_context.session_context.script_id

    if session_id in path:
        filepath = path.split(session_id)[1]
        return os.path.join('./', filepath)

    if script_id in path:
        filepath = path.split(script_id)[1]
        return os.path.join('./', filepath)


def is_server_path(path: str) -> bool:
    """
    Returns whether the given path is a server-only path (session or script id prefixed).
    """
    return path.startswith(ROOT_SCRIPT_DIR) or path.startswith(ROOT_SESSION_DIR)


class StorageScope(Enum):
    USER = 'USER'
    APP = 'APP'
    GLOBAL = 'GLOBAL'


def hash(data: any, scope: StorageScope | str = StorageScope.USER) -> str:
    """
    Saves data in the given scope (USER, APP, GLOBAL) and returns its hash.
    The returned hash can be used as an alias with widget parameters.
    """
    try:
        hash = hash_object(data)
        save(hash, data, scope)
        return hash
    except:
        raise Exception('The data is not serializable!')


def save(key: str, data: any, scope: StorageScope | str = StorageScope.USER) -> None:
    """
    Saves data in the given scope (USER, APP, GLOBAL).
    The data can be retrieved later using the 'load' function with the same key,
    and the key be used as an alias with widget parameters.
    """
    if not is_server_mode():
        embedded_save(key, data)
        return

    if isinstance(scope, str):
        scope = StorageScope(scope.upper())

    session_id = get_run_context().session_context.session_id
    if scope == StorageScope.USER:
        key = key + session_id
    else:
        script_id = get_run_context().session_context.script_id
        if scope == StorageScope.APP:
            key = key + script_id

    get_run_context().session_context.set_data(key, data)



def load(key: str | None = None) -> any:
    """
    Loads data with the key it was saved with by the 'save' function.
    """
    if not is_server_mode():
        return EmbeddedDataStorage.get_current().get(key)

    return get_run_context().session_context.get_data(key)


def config(values: dict[str, any]) -> any:
    if not is_server_mode():
        for key, value in values.items():
            EmbeddedConfig[key] = value
    # todo (not yet) - implement config for server mode (use session context)
    # e.g. for setting the default theme

