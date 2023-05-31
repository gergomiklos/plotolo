import gc
import sys
from threading import Thread
import traceback
from types import ModuleType
from copy import copy

import nbformat

from plotolo.script.script_context import set_run_context, RunContext, get_run_context, SessionContext
from plotolo.script.script_storage import ScriptStorage
from plotolo.util.constant import PLOTOLO_SCRIPT_THREAD_PREFIX
from plotolo.util.logging import SessionLogger
from plotolo.script.script_info import ScriptInfo
from plotolo.script.script_status import ScriptStatus, ScriptState
from plotolo.session.widget_state import CellInfo
from plotolo.util.util import to_json
from plotolo.widget.common import StopExecutionException


class ScriptRunner:
    """
    Executes the Notebook's cells on low-level and in a separate thread and in a persistent namespace.
    Sends events to the SessionHandler.
    """
    def __init__(self, script_id: str, session_context: SessionContext, on_script_error, on_script_started,
                 on_script_finished, on_script_stopped, on_cell_started, on_cell_finished):
        self.session_context: SessionContext = session_context
        self.script_info: ScriptInfo = ScriptStorage.get_current().get(script_id)
        self.script_state: ScriptState = ScriptState()

        self.script_module: ModuleType | None = None
        self.script_thread: Thread | None = None

        self.on_script_error = on_script_error
        self.on_script_started = on_script_started
        self.on_script_stopped = on_script_stopped
        self.on_script_finished = on_script_finished
        self.on_cell_started = on_cell_started
        self.on_cell_finished = on_cell_finished

        self.script_run_index = -1

        self.logger = SessionLogger.getLogger(session_context.session_id)


    def get_run_context(self):
        return get_run_context(self.script_thread)


    def _setup_script_module(self):
        """
        Creates a new module for the script and sets it as the main module.
        Used for a persistent namespace between reruns.
        Should be called from the script thread.
        """
        self.logger.debug('Setting up script module:', self.script_info.id)

        module = ModuleType("__main__")
        module.__file__ = self.script_info.filename
        module.__loader__ = self
        sys.modules["__main__"] = module
        self.script_module = module


    def _should_rerun(self, cell_indexes_to_rerun=None):
        """
        Checks if the script should be rerun or it can be skipped.
        If the current script execution covers to new request, it can be skipped,
        otherwise it should be rerun.
        """
        if cell_indexes_to_rerun is None:
            return True

        if not self.script_thread or not self.script_thread.is_alive():
            return True

        if self.script_state.status == ScriptStatus.STOPPED:
            return True

        if self.get_run_context().cell_info.cell_index >= min(cell_indexes_to_rerun):
            self.get_run_context().rerun = True
            return True

        return False


    def run(self, cell_indexes_to_rerun: [int] = None):
        """
        Runs the script in a separate thread and with its context.
        """
        if not self._should_rerun(cell_indexes_to_rerun):
            self.logger.debug('Rerun skipped')
            return

        self.logger.debug('Starting thread...')
        self.script_run_index += 1
        thread_run_context = self.init_run_context()

        self.script_thread = Thread(
            target=self._execute_script_thread,
            name=f"{PLOTOLO_SCRIPT_THREAD_PREFIX}:{self.script_info.name}:{self.session_context.session_id}:{self.script_run_index}",
            args=[thread_run_context, cell_indexes_to_rerun]
        )
        self.script_thread.start()
        setattr(self.script_thread, RunContext.RUN_CONTEXT_ATTR, thread_run_context)

        # self.script_thread.join()  # only for debug purposes!
        # print_module(self.script_module)  # only for debug purposes!


    def init_run_context(self):
        return RunContext(self.session_context, CellInfo(script_run_index=self.script_run_index))


    def before_cell_exec(self, cell):
        """
        Sets the cell info in the run context.
        """
        context = self.get_run_context()
        context.cell_info.cell_index = cell.index
        context.cell_info.cell_id = cell.id
        context.cell_info.widget_index = 0
        context.cell_info.script_run_index = self.script_run_index

        if self.on_cell_started:
            self.on_cell_started(context.cell_info)


    def after_cell_exec(self):
        gc.collect()
        if self.on_cell_finished:
            self.on_cell_finished(copy(self.get_run_context().cell_info))


    def script_started(self, cell_indexes_to_rerun: [int]):
        self.script_state.status = ScriptStatus.RUNNING
        if self.on_script_started:
            self.on_script_started(cell_indexes_to_rerun)


    def script_finished(self):
        if not self.get_run_context().rerun:
            self.script_state.status = ScriptStatus.STOPPED
            if self.on_script_finished:
                self.on_script_finished()


    def script_error(self, error_msg):
        self.script_state.errors.append(error_msg)
        self.logger.error('Error:', error_msg, '- Cell info:', to_json(self.get_run_context().cell_info))
        if self.on_script_error:
            self.on_script_error()


    def _execute_script_thread(self, thread_run_context: RunContext, cell_indexes_to_rerun: [int] = None):
        """
        Executes the Notebook's cells in a loop and sends events.
        """
        if not self.script_module:
            self._setup_script_module()

        if not cell_indexes_to_rerun:
            # if not set, run all cells
            cell_indexes_to_rerun = list(range(self.script_info.n_cells))

        set_run_context(thread_run_context)

        self.script_started(cell_indexes_to_rerun)

        self.logger.debug('Running cells :', ', '.join(str(idx) for idx in cell_indexes_to_rerun))
        try:
            for cell_index in cell_indexes_to_rerun:
                cell = self.script_info.compiled_cells[cell_index]

                self.logger.debug(f'Executing cell: {cell.index}')
                self.before_cell_exec(cell)

                exec(cell.code, self.script_module.__dict__)

                if thread_run_context.rerun:
                    self.logger.debug('Script stopped for rerun')
                    return

                self.after_cell_exec()

        except StopExecutionException as e:
            self.logger.debug('Script ran and stopped successfully')
            self.on_script_stopped(e.clear_all_outputs_bellow)
        except Exception as e:
            self.logger.error('Script error occurred:', traceback.format_exc())
            self.script_error(repr(e)),
        else:
            self.logger.debug('Script ran successfully')
        finally:
            self.script_finished()



# Investigate:
#   nbclient: https://nbclient.readthedocs.io/en/latest/reference/nbclient.html
#   IPython InteractiveShell: https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.interactiveshell.html

