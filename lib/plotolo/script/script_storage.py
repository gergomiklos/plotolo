import os.path
import re
import subprocess
import sys

import nbformat

from plotolo.script.script_info import ScriptCell, ScriptInfo
from plotolo.util.util import hash_string
from plotolo.util.logging import logger
from plotolo.util.filesystem_watcher import DirectoryWatcher
from plotolo.config import ROOT_SCRIPT_DIR


class ScriptStorage:
    _singleton: 'ScriptStorage' = None


    @classmethod
    def get_current(cls) -> 'ScriptStorage':
        if ScriptStorage._singleton is None:
            ScriptStorage._singleton = ScriptStorage()
        return ScriptStorage._singleton


    def __init__(self):
        if ScriptStorage._singleton is not None:
            raise RuntimeError("Singleton already initialized. Call 'get_current' instead")
        ScriptStorage._singleton = self

        self._scripts: dict[str, ScriptInfo] = {}
        self.script_listener: DirectoryWatcher = DirectoryWatcher(
            path=ROOT_SCRIPT_DIR,
            on_created=self.on_script_uploaded,
            on_deleted=self.on_script_deleted,
        )


    def load_scripts(self):
        for dir in os.listdir(ROOT_SCRIPT_DIR):
            if os.path.isdir(os.path.join(ROOT_SCRIPT_DIR, dir)):
                self.on_script_uploaded(dir)


    def listen(self):
        self.load_scripts()
        if not self.script_listener.observer.is_alive():
            self.script_listener.start()


    def stop(self):
        if self.script_listener.observer.is_alive():
            self.script_listener.stop()


    def get(self, script_id: str) -> ScriptInfo:
        return self._scripts.get(script_id)


    def all(self):
        return self._scripts.values()


    def on_script_deleted(self, script_id):
        logger.debug(f'Deleting script: {script_id}')

        if script_id in self._scripts:
            del self._scripts[script_id]


    def find_notebook_file(self, directory):
        for file in os.listdir(directory):
            if file.endswith('.ipynb'):
                return os.path.join(directory, file)
        return None


    def on_script_uploaded(self, script_id):
        """
        Called when a new script is uploaded to the script directory.
        Loads the script, installs its requirements, pre-compiles its cells, and stores it in the script storage.
        """
        logger.debug(f'Uploading script: {script_id}')

        # find notebook file
        script_directory = os.path.join(ROOT_SCRIPT_DIR, script_id)
        script_path = self.find_notebook_file(script_directory)
        if not script_path:
            logger.error(f'No notebook file found in: {script_id}')
            return

        # install requirements
        if not self.install_requirements(script_directory):
            logger.error(f'Failed to install requirements for: {script_id}')
            return

        # specify script name
        filename = os.path.basename(script_path)
        name = self._read_first_title(script_path)
        if not name:
            name = filename.replace('.ipynb', '').replace('_', '').title()

        # precompile script
        compiled_cells = self._precompile_script(script_path)

        # store script
        script_info = ScriptInfo(
            id=script_id,
            name=name,
            filename=filename,
            n_cells=len(compiled_cells),
            compiled_cells=compiled_cells,
        )
        self._scripts[script_id] = script_info


    def _read_first_title(self, script_path):
        """
        Reads the first markdown cell of a notebook and returns the title.
        """
        with open(script_path, "r", encoding="utf-8") as file:
            notebook = nbformat.read(file, 4)

        for cell in notebook.cells[:2]:  # reading the first two cells only
            if cell.cell_type == 'markdown':
                for line in cell.source.split('\n'):
                    match = re.match(r'^#+\s', line)  # Use regex to match any number of '# ' at the start of the line
                    if match:
                        return line[match.end():]  # Return title without '# ' prefix
                return None  # If no title found in first markdown cell, stop searching

        return None  # If no markdown cells found in the first to cells, stop searching


    def _precompile_script(self, script_path):
        """
        Pre-compiles a notebook script into a list of ScriptCell objects.
        """
        logger.debug(f'Pre-compiling script: {script_path}')

        with open(script_path, "r", encoding="utf-8") as file:
            notebook = nbformat.read(file, 4)


        def _remove_ipython_magic(cell_source):
            """
            Removes IPython magic commands from a cell source.
            """
            if cell_source.startswith('%%'):
                return ''
            return '\n'.join(
                [line for line in cell_source.split('\n') if not (line.startswith('%') or line.startswith('!'))])


        cell_index = 0
        compiled_cells = []
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                cleaned_source = _remove_ipython_magic(cell.source)
                cell_code = compile(
                    cleaned_source,
                    # Pass the notebook file's name, so it can show up in exceptions.
                    os.path.basename(script_path),
                    # We're compiling entire blocks of Python, so we need "exec" mode
                    mode="exec",
                    # Don't inherit any flags or "future" statements.
                    flags=0,
                    dont_inherit=1,
                    # Use the default optimization options.
                    optimize=-1,
                )
                compiled_cells.append(
                    ScriptCell(
                        cell_id=hash_string(cell.source),
                        cell_index=cell_index,
                        cell_code=cell_code
                    )
                )
                cell_index += 1

        return compiled_cells


    def install_requirements(self, script_directory):
        """
        Installs requirements from a requirements.txt file in the script directory if exists.
        """
        requirements_path = None
        for file in os.listdir(script_directory):
            if file.endswith('requirements.txt'):
                requirements_path = os.path.join(script_directory, file)

        if requirements_path:
            try:
                logger.info(f'Installing requirements from {os.path.basename(requirements_path)}')
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])

            except subprocess.CalledProcessError as e:
                logger.error(f'Failed to install requirements from {os.path.basename(requirements_path)}')
                logger.error(repr(e))
                return False

        return True
