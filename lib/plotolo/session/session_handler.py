import json
import time

from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

from plotolo.script.script_context import SessionContext
from plotolo.util.logging import SessionLogger
from plotolo.script.script_runner import ScriptRunner
from plotolo.script.script_info import ScriptInfo
from plotolo.session.data_storage import DataStorage
from plotolo.util.util import to_json, hash_object
from plotolo.util.debouncer import Debouncer
from plotolo.session.widget_state import WidgetState, CellInfo, WidgetStatus, WidgetAction
from plotolo.session.message import WidgetResponse, ScriptStateResponse, ResponseMessage, RequestMessage


class SessionHandler:
    """
    Manages the session state and the websocket communication with the frontend, per client session.
    """


    def __init__(self, session_id: str, script_id: str, ioloop: IOLoop):
        self.session_id: str = session_id

        # Tornado web server is available only from the main thread,
        # which can be reached by executing a callback through the main ioloop.
        # See: https://www.tornadoweb.org/en/stable/web.html#thread-safety-notes
        self.ioloop: IOLoop = ioloop  # main application thread

        self.data_storage: DataStorage = DataStorage.get_current()  # global data store for caching data
        self.widgets: dict[str, WidgetState] = {}  # widget states with hashes
        # debouncer for batching messages to the frontend
        self.debouncer: Debouncer = Debouncer(ioloop, wait_time=.05, max_wait_time=.1)
        self.websocket: WebSocketHandler | None = None  # websocket connection to the frontend

        self.updated_hashes: set[str] = set([])  # new hashes for which the data needs to be sent to the frontend
        self.last_widget_order: [str] = []  # last order of widgets sent to the frontend
        self.saved_data_keys: set[str] = set([])  # keys of saved data by the 'save' widget

        self.script_runner: ScriptRunner = ScriptRunner(  # runs the script and sends widget updates
            script_id=script_id,
            session_context=SessionContext(
                session_id=session_id,
                script_id=script_id,
                send_widget=self.send_widget_update,
                get_data=self.get_saved_data,
                set_data=self.save_data,
            ),
            on_script_error=self.on_script_error,
            on_script_started=self.on_script_started,
            on_script_stopped=self.on_script_stopped,
            on_script_finished=self.on_script_finished,
            on_cell_started=self.on_cell_started,
            on_cell_finished=self.on_cell_finished,
        )

        self.logger: SessionLogger = SessionLogger.getLogger(session_id)


    def save_data(self, key: str, value: any):
        """
        Saves the not widget related data by the given fix key.
        Used by the 'save' widget with 3 scopes: session, script, global.
        """
        self.saved_data_keys.add(key)
        self.data_storage.set(key, value)


    def get_saved_data(self, key: str):
        """
        Loads the data with the given fix key. Used by the 'load' widget in 3 scopes: session, script, global.
        After the data is set by the 'save' widget, it is possible to call other widget by the same key
        instead of the actual data, and this function can be used to find and load that actual data.
        """
        # returns in the order of most specific to least specific
        return self.data_storage.get(key + self.session_id) or \
               self.data_storage.get(key + self.script_runner.script_info.id) or \
               self.data_storage.get(key)


    def connect(self, websocket: WebSocketHandler):
        self.set_websocket(websocket)
        self.script_runner.run()


    def reconnect(self, websocket: WebSocketHandler):
        self.set_websocket(websocket)
        self.send_widgets()


    def set_websocket(self, websocket: WebSocketHandler):
        self.websocket = websocket
        self.websocket.on_message = self._on_input_message


    def send_response_message(self, message: ResponseMessage):
        """
        Sends websocket message to the frontend
        """


        async def _send_message(msg: ResponseMessage):
            if self.websocket:
                await self.websocket.write_message(to_json(msg))


        self.ioloop.add_callback(_send_message, message)


    async def _on_input_message(self, message_str):
        """
        Receives inputs from the client given by its input id.
        If the input value changed, reruns the script with the new value,
        otherwise the response is served from the global cache _data
        """
        message = RequestMessage.from_dict(json.loads(message_str))
        self.handle_widget_input_requests(message.input_requests)
        self.handle_data_requests(message.data_requests)


    def handle_data_requests(self, data_requests: [str] = None):
        """
        Sends the requested data to the frontend by their hashes
        """
        if not data_requests:
            return
        self.logger.debug('New data request(s)')

        for hash in data_requests:
            self.updated_hashes.add(hash)

        self.send_widgets()


    def handle_widget_input_requests(self, widget_input_requests: dict[str, dict[str, any]] = None):
        """
        Updates the widget states with the new input values,
        calculates what cells to rerun based on the widget actions,
        and reruns the script if necessary
        """
        if not widget_input_requests:
            return
        self.logger.debug('New widget input request(s)')

        n_cells = self.script_runner.script_info.n_cells
        cell_indexes_to_rerun = set([])
        # get the cells that need to be rerun by the actions of widgets updates by the input
        for widget_id, data_update in widget_input_requests.items():
            if self.update_widget_data(widget_id, data_update):
                widget = self.widgets[widget_id]
                cell_index = self.widgets[widget_id].cell_info.cell_index
                action = widget.action
                if action == WidgetAction.NONE:
                    pass
                elif action == WidgetAction.RUN_ALL:
                    cell_indexes_to_rerun.update(range(n_cells))
                elif action == WidgetAction.RUN_ALL_BELOW:
                    cell_indexes_to_rerun.update(range(cell_index, n_cells))
                elif action == WidgetAction.RUN_CELL:
                    cell_indexes_to_rerun.add(cell_index)

        if len(cell_indexes_to_rerun) > 0:
            self.logger.debug('Changes detected, rerunning...')
            cell_indexes_to_rerun = sorted(cell_indexes_to_rerun)
            self.script_runner.run(cell_indexes_to_rerun=cell_indexes_to_rerun)
        else:
            self.logger.debug('No changes detected')


    def has_hash(self, hash: str):
        """
        Used by the global storage cleanup to check if the session contains the given hash of a data
        """
        for widget in self.widgets.values():
            if hash in widget.hash_state.values():
                return True
        for key in self.saved_data_keys:
            if hash == key:
                return True
        return False


    def on_script_error(self):
        self.send_widgets()


    def on_script_started(self, cell_indexes_to_rerun: [int]):
        """
        Marks all widgets as pending as they are waiting for a new call from the script
        """
        self.mark_widgets_as_pending(cell_indexes_to_rerun)


    def on_script_finished(self):
        """
        After script finished, marks all pending widgets as deleted as they were not called during the script run
        """
        self.mark_widgets_statuses(mark=WidgetStatus.PENDING, to=WidgetStatus.DELETED)
        self.send_widgets()
        self.delete_widgets_actually()


    def on_script_stopped(self, clear_all_outputs_bellow=False):
        """
        After planned script stop, marks remainig pending widgets as unchanged so that they won't be deleted
        """
        if not clear_all_outputs_bellow:
            # marks all widgets as unchanged so that they won't be deleted
            self.mark_widgets_statuses(mark=WidgetStatus.PENDING, to=WidgetStatus.UNCHANGED)
            self.send_widgets()


    def on_cell_started(self, cell_info: CellInfo):
        pass


    def on_cell_finished(self, cell_info: CellInfo):
        """
        After cell finished, marks all widgets as deleted as they were not called during the cell run
        """
        self.mark_widgets_deleted_after_cell_finish(cell_info)
        self.delete_widgets_actually()


    def update_widget_data(self, widget_id, new_data: dict[str, any]):
        """
        If the widget data changed, updates the widget state with the new hashes,
        saves the new data to the global data _data
        and returns True if the widget was updated
        """
        widget = self.widgets.get(widget_id)
        if not widget:
            return False

        updated = False
        for key, new_value in new_data.items():

            new_hash = None
            if isinstance(new_value, str):
                # If the value is a string, it may be a key to an already saved data
                # by the 'save' widget, so it does a data lookup
                saved_data = self.get_saved_data(new_value)
                if saved_data:
                    new_value = saved_data
                    new_hash = new_value
            if not new_hash:
                new_hash = hash_object(new_value)

            old_hash = widget.hash_state.get(key)

            if old_hash != new_hash:
                self.data_storage.set(new_hash, new_value)
                self.updated_hashes.add(new_hash)
                widget.hash_state[key] = new_hash
                widget.status = WidgetStatus.UPDATED
                widget.updated = time.time()
                self.data_storage.delete(old_hash)
                updated = True

        return updated


    def update_widget(self, id, type, action: WidgetAction, cell_info: CellInfo, data: dict[str, any]):
        """
        Updates the widget state with the new cell info, status, data and hashes
        """
        widget = self.widgets.get(id)

        # Create widget if does not exist
        if not widget:
            widget = WidgetState(
                id=id,
                type=type,
                action=action,
                status=WidgetStatus.UPDATED,
                cell_info=cell_info,
                hash_state={},
            )
            self.widgets[id] = widget

        # Handle changes in widget order -> not an actual data update
        widget.cell_info = cell_info

        # Update the widget data and its hashes
        self.update_widget_data(id, data)
        if widget.status == WidgetStatus.PENDING:
            widget.status = WidgetStatus.UNCHANGED


    def send_widget_update(self, id, type, action: WidgetAction, cell_info: CellInfo, data: dict[str, any]):
        """
        Sends output to the client through the websocket and returns the widget data which may be updated previously.
        Should be called from the script thread.
        """
        self.update_widget(id, type, action, cell_info, data)

        self.send_widgets()

        return self.hash_state_to_data_widget(id)


    def hash_state_to_data_widget(self, id):
        """
        Collects the data for the widget hashes with the given id
        """
        widget = self.widgets.get(id)
        if not widget:
            return {}

        data_widget = {}
        for key, hash in widget.hash_state.items():
            data_widget[key] = self.data_storage.get(hash)
        return data_widget


    @staticmethod
    def widget_sorter(widget: WidgetState):
        """
        Sorts the widgets by their cell index, widget index, script run index, status and updated time
        """
        status_order = {
            WidgetStatus.UNCHANGED: 0,
            WidgetStatus.UPDATED: 1,
            WidgetStatus.PENDING: 2,
            WidgetStatus.DELETED: 3,
        }[widget.status]
        cell_info = widget.cell_info
        return cell_info.cell_index, cell_info.widget_index, -cell_info.script_run_index, status_order, -widget.updated


    def mark_unused_widgets_as_deleted(self, new_widget_order: [str]):
        """
        Marks every pending widget as deleted based on their previous and current order:
        if there is a widget that was behind it last time and is now in front of it,
        because we expect those the widget will not be called anymore.
        """
        if self.last_widget_order:
            for new_index, widget_id in enumerate(new_widget_order):
                if self.widgets[widget_id].status == WidgetStatus.PENDING:
                    last_index = self.last_widget_order.index(widget_id)
                    # If any of the widgets that was behind this widget is now in front of it
                    if set(self.last_widget_order[last_index:]) & set(new_widget_order[:new_index]):
                        self.widgets[widget_id].status = WidgetStatus.DELETED

        self.last_widget_order = new_widget_order


    def collect_updated_data(self):
        """
        Collects the data for the updated hashes and returns it
        """
        widget_data = {hash: self.data_storage.get(hash) for hash in self.updated_hashes}
        self.updated_hashes.clear()
        return widget_data


    def send_widgets(self):
        """
         Sends the widgets to the frontend:
         - sorts the widgets into a list with the corresponding order
         - marks the unused widgets as deleted
         - maps the widgets to WidgetResponse
         - marks the updated widgets as unchanged
         - collects data for the widgets that have been updated
         - send the widget_sates, widget_data and script_state messages to the client with debouncing
        """


        def _send_widgets():
            sorted_widgets = sorted(list(self.widgets.values()), key=self.widget_sorter)

            self.mark_unused_widgets_as_deleted(new_widget_order=[widget.id for widget in sorted_widgets])

            widget_states = [WidgetResponse.from_widget(widget) for widget in sorted_widgets]

            self.mark_widgets_statuses(mark=WidgetStatus.UPDATED, to=WidgetStatus.UNCHANGED)

            widget_data = self.collect_updated_data()

            script_state = ScriptStateResponse.from_script_state(self.script_runner.script_state)

            self.send_response_message(
                ResponseMessage(
                    widget_states=widget_states,
                    widget_data=widget_data,
                    script_state=script_state,
                )
            )


        self.debouncer.call(_send_widgets)


    def mark_widgets_deleted_after_cell_finish(self, cell_info: CellInfo):
        """
        Marks widgets as DELETED which was not updated in the latest script run per cell,
        and sends the updates to the frontend
        """
        deleted = False
        for id, widget in self.widgets.items():
            if widget.cell_info.cell_index == cell_info.cell_index \
                    and widget.status == WidgetStatus.PENDING \
                    and widget.cell_info.script_run_index < cell_info.script_run_index:
                self.widgets[id].status = WidgetStatus.DELETED
                deleted = True

        if deleted:
            self.send_widgets()


    def mark_widgets_as_pending(self, cell_indexes_to_rerun: [int]):
        """
        Marks widgets as PENDING if it was called in-after the given cell
        (as we expect a rerun for these widgets later -> UNCHANGED/UPDATED)
        and sends the updates to the frontend
        """
        for id, widget in self.widgets.items():
            if widget.cell_info.cell_index in cell_indexes_to_rerun:
                if widget.status != WidgetStatus.DELETED:
                    widget.status = WidgetStatus.PENDING

        self.send_widgets()


    def mark_widgets_statuses(self, mark: WidgetStatus, to: WidgetStatus):
        """
        Marks every pending widget as the given status
        """
        for widget in self.widgets.values():
            if widget.status == mark:
                widget.status = to


    def delete_widgets_actually(self):
        """
        Deletes widgets and their data which are marked as deleted
        """
        for id in list(self.widgets.keys()):
            if self.widgets[id].status == WidgetStatus.DELETED:
                del self.widgets[id]

        self.data_storage.cleanup()


    def close(self):
        self.logger.debug('Session closed')
