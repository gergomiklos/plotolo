

class ScriptCell:
    """
    Information about a Python Notebook cell
    """


    def __init__(self, cell_id, cell_index, cell_code):
        self.id = cell_id
        self.index = cell_index
        self.code = cell_code


class ScriptInfo:
    """
    Information about the Python Notebook script (files and cells)
    """


    def __init__(self, id: str = None, name: str = None, filename: str = None, n_cells=None, compiled_cells: [ScriptCell] = None):
        self.id = id
        self.name = name
        self.filename = filename
        self.n_cells = n_cells
        self.compiled_cells: [ScriptCell] = compiled_cells
