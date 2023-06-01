import ipyreact

from IPython.core.display import Javascript
from IPython.core.display_functions import display
from traitlets import Unicode, Dict, Bool

from plotolo.session.widget_state import WidgetAction as Action
from plotolo.util.util import hash_object

EmbeddedConfig = {}  # todo singleton class


class EmbeddedDataStorage:
    """
    Singleton class to store data updates and saved objects for inline notebook widgets
    """
    _singleton: 'EmbeddedDataStorage' = None


    @classmethod
    def get_current(cls) -> 'EmbeddedDataStorage':
        if EmbeddedDataStorage._singleton is None:
            EmbeddedDataStorage._singleton = EmbeddedDataStorage()
        return EmbeddedDataStorage._singleton


    def __init__(self):
        if EmbeddedDataStorage._singleton is not None:
            raise RuntimeError("Singleton already initialized. Call 'get_current' instead")
        EmbeddedDataStorage._singleton = self

        self._data: dict[str, dict[str, any]] = {}


    def get(self, widget_id):
        return self._data.get(widget_id, {})


    def set(self, key, data):
        self._data[key] = data


    def remove(self, widget_id):
        self._data.pop(widget_id, None)


    def clear(self):
        self._data = {}


    def merge_update(self, widget_id, data_update: dict[str, any]):
        self._data[widget_id] = {**self.get(widget_id), **data_update}


def rerun_interactive_cells(action: Action):
    """
    Rerun the desired cells in the Notebook using the live Jupyter session.
    """
    if EmbeddedConfig.get('disable_interactive_widgets', False):
        return

    from_index, to_index = "0", "0"  # covers the NONE action by default
    if action == Action.RUN_CELL:
        from_index, to_index = "current_cell_index", "current_cell_index + 1"
    elif action == Action.RUN_ALL:
        from_index, to_index = "0", "n_cells"
    elif action == Action.RUN_ALL_BELOW:
        from_index, to_index = "current_cell_index", "n_cells"

    display(Javascript(f"""
    var output_area = this;
    var cell_element = output_area.element.parents('.cell');
    var current_cell_index = Jupyter.notebook.get_cell_elements().index(cell_element);
    const n_cells = Jupyter.notebook.get_cells().length;

    Jupyter.notebook.execute_cell_range({from_index}, {to_index});
    """))


def embedded_widget(id: str | int, type: str, action: Action, data: dict[str, any], **kwargs) -> dict[str, any]:
    """
    Display an inline Notebook widget in the current cell output,
    and sets up a callback to listen inputs from the widget.
    """
    data_storage = EmbeddedDataStorage.get_current()

    class _InlineNotebookWidget(ipyreact.ReactWidget):
        _esm = """
            import React from "react";
            import {Widget} from "plotolo-widget@0.0.3"

            export default function EmbeddedWidget(props) {
              return  <Widget {...props} />
            }
        """

        id = Unicode().tag(sync=True)
        type = Unicode().tag(sync=True)
        status = Unicode('UNCHANGED').tag(sync=True)
        data = Dict().tag(sync=True)
        embedded = Bool(True).tag(sync=True)

        def on_input(self, data: dict[str, any]):
            # merge the data update into the previous updates
            data_storage.merge_update(data['widget_id'], data['data_update'])
            # rerun the cells on interaction
            rerun_interactive_cells(action)


    # merge the previous updates from the storage
    data = {**data, **data_storage.get(id)}

    display(_InlineNotebookWidget(id=str(id), type=type, data=data))

    return data


def embedded_save(key: str, data: any) -> None:
    try:
        hash_object(data)
    except:
        print('Warning: The data is not serializable, do not use it with widgets!')
    EmbeddedDataStorage.set(key, data)