from plotolo.session.widget_state import WidgetState
from plotolo.script.script_status import ScriptState, ScriptStatus


# ----------- INPUT ------------


class RequestMessage:
    """
    Batched request for
        script rerun with new states and/or
        data lookup from hashes
    """


    def __init__(self, input_requests: dict[dict[str, any], any] = None, data_requests: [str] = None):
        if data_requests is None:
            data_requests = []
        if input_requests is None:
            input_requests = {}
        self.input_requests: dict[dict[str, any], any] = input_requests
        self.data_requests: [str] = data_requests


    @classmethod
    def from_dict(cls, json_dict: dict[str, any]):
        input_requests = json_dict.get('input_requests', {})
        data_requests = json_dict.get('data_requests', [])
        return cls(input_requests=input_requests, data_requests=data_requests)


# ----------- OUTPUT ------------


class WidgetResponse:
    """
    Response with a widget with its hashes
    """


    def __init__(self, id, type, status, hash_state: dict[str, str]):
        self.id = id
        self.type = type
        self.status = status
        self.hash_state: dict[str, str] = hash_state  # [key: hash] state of the widget


    @classmethod
    def from_widget(cls, widget: WidgetState):
        return cls(
            id=widget.id,
            type=widget.type,
            status=widget.status,
            hash_state=widget.hash_state,
        )


class ScriptStateResponse:
    """
    Response with a script status and errors
    """


    def __init__(self, status: ScriptStatus, errors):
        self.status: ScriptStatus = status
        self.errors = errors


    @classmethod
    def from_script_state(cls, script_state: ScriptState):
        errors = script_state.errors
        script_state.errors = []
        return cls(
            status=script_state.status,
            errors=errors,
        )


class ResponseMessage:
    """
    Batched response with widgets states, widget data and script state
    """


    def __init__(self, script_state: ScriptState, widget_states: [WidgetState] = None,
                 widget_data: dict[str, any] = None):
        if widget_states is None:
            widget_states = []
        if widget_data is None:
            widget_data = []
        self.widget_states = widget_states
        self.widget_data = widget_data
        self.script_state = script_state
