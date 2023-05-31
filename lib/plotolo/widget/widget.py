from plotolo.session.widget_state import WidgetAction as Action
from plotolo.widget.util import load_base64_image as _load_base64_image, \
    get_columns_from_data as _get_columns_from_data, \
    convert_data_to_list_of_lists as _convert_data_to_list_of_lists, \
    insert_columns_before_data as _insert_columns_before_data, \
    transpose_data as _transpose_data
from plotolo.widget.common import base_widget as _base_widget, Widget as _Widget, \
    is_server_mode as _is_server_mode, StopExecutionException as _StopExecutionException, \
    repath as _repath, path, PathScope, save, load, hash, StorageScope, config


def custom_base_widget(
        id: str | int,
        type: str,
        action: Action | str = Action.RUN_ALL_BELOW,
        data: dict = None) -> any:
    id = str(id) + type

    widget = _Widget(
        id=id,
        type=type,
        action=action,
        data=data,
    )

    return _base_widget(widget)


def text(
        value: str,
        id: str | int = None) -> None:
    if not id:
        id = str(value) + 'TEXT'

    widget = _Widget(
        id=id,
        type='TEXT',
        action=Action.NONE,
        data={
            'value': value,
        }
    )
    _base_widget(widget)


def title(
        value: str,
        level: int = 3,
        id: str | int = None) -> None:
    if not id:
        id = str(value) + 'TITLE'

    widget = _Widget(
        id=id,
        type='TITLE',
        action=Action.NONE,
        data={
            'value': value,
            'level': level,
        }
    )
    _base_widget(widget)


def latex(
        value: str,
        id: str | int = None) -> None:
    return markdown(value, id=id)


def markdown(
        value: str,
        id: str | int = None) -> None:
    if not id:
        id = str(value) + 'MARKDOWN'

    widget = _Widget(
        id=id,
        type='MARKDOWN',
        action=Action.NONE,
        data={
            'value': value,
        }
    )
    _base_widget(widget)


def text_input(
        label: str = None,
        default_value: str = None,
        place_holder: str = None,
        id: str | int = None,
        action: Action | str = Action.RUN_ALL_BELOW) -> str:
    if not id:
        id = str(label) + str(default_value) + 'TEXT_INPUT'

    widget = _Widget(
        id=id,
        type='TEXT_INPUT',
        action=action,
        data={
            'default_value': default_value,
            'label': label,
            'place_holder': place_holder,
        }
    )

    data = _base_widget(widget)
    return data.get('value', default_value)


def button(
        label: str,
        id: str | int = None,
        action: Action | str = Action.RUN_ALL_BELOW) -> bool:
    if not id:
        id = label + 'BUTTON'

    widget = _Widget(
        id=id,
        type='BUTTON',
        action=action,
        data={
            'label': label,
        }
    )

    data = _base_widget(widget)
    clicked = data.get('clicked', False)

    # Click should be reset after each run
    # todo called twice in embedded mode
    if clicked:
        widget.data['clicked'] = False
        _base_widget(widget)

    return clicked


def file_download(
        label: str,
        filepath: str,
        id: str | int = None,
        action: Action | str = Action.RUN_ALL_BELOW) -> bool:
    if not id:
        id = label + filepath + 'FILE_DOWNLOAD'

    # if the user called with path(filepath), we need to fix it
    filepath = _repath(filepath)

    widget = _Widget(
        id=id,
        type='FILE_DOWNLOAD',
        action=action,
        data={
            'label': label,
            'filepath': filepath,
        }
    )

    # todo handle byte transfer through embedded widget not just server
    data = _base_widget(widget)
    downloaded = data.get('downloaded', False)

    # Click should be reset after each run
    if downloaded:
        widget.data['downloaded'] = False
        _base_widget(widget)

    return downloaded


def file_upload(
        label: str,
        path: str = None,
        id: str | int = None,
        action: Action | str = Action.RUN_ALL_BELOW) -> str:
    if not id:
        id = label + str(path) + 'FILE_UPLOAD'

    # if the user called with path(filepath), we need to fix it
    if path:
        path = _repath(path)
        if path.startswith('./'):
            path = path[2:]
        if path.startswith('/'):
            path = path[1:]

    widget = _Widget(
        id=id,
        type='FILE_UPLOAD',
        action=action,
        data={
            'label': label,
            'path': path,
        }
    )

    # todo handle byte transfer through embedded widget not just server
    data = _base_widget(widget)
    return data.get('uploaded_filename', None)


def stop(
        clear_all_outputs_bellow: bool = False,
        stop: bool = True):
    if stop:
        raise _StopExecutionException(clear_all_outputs_bellow)


def checkbox(
        label: str = None,
        default_value: bool = False,
        id: str | int = None,
        action: Action | str = Action.RUN_ALL_BELOW) -> str:
    if not id:
        id = str(label) + str(default_value) + 'CHECKBOX'

    widget = _Widget(
        id=id,
        type='CHECKBOX',
        action=action,
        data={
            'label': label,
            'default_value': default_value,
        }
    )

    data = _base_widget(widget)
    return data.get('value', default_value)


def select(
        options: [str],
        label: str = None,
        default_value: str = None,
        id: str | int = None,
        action: Action | str = Action.RUN_ALL_BELOW) -> str:
    if not id:
        id = str(label) + str(default_value) + ''.join(options) + 'SELECT'

    if not default_value:
        default_value = options[0]

    widget = _Widget(
        id=id,
        type='SELECT',
        action=action,
        data={
            'label': label,
            'default_value': default_value,
            'options': options,
        }
    )

    data = _base_widget(widget)
    return data.get('value', default_value)


def slider(
        label: str = None,
        default_value: int = None,
        min: int = 0,
        max: int = 100,
        id: str | int = None,
        action: Action | str = Action.RUN_ALL_BELOW) -> str:
    if not id:
        id = str(label) + str(default_value) + str(min) + str(max) + 'SLIDER'

    if default_value is None:
        default_value = (max - min) / 2

    widget = _Widget(
        id=id,
        type='SLIDER',
        action=action,
        data={
            'label': label,
            'default_value': default_value,
            'min': min,
            'max': max,
        }
    )

    data = _base_widget(widget)
    return data.get('value', default_value)


def divider(id: str | int) -> None:
    widget = _Widget(
        id=id,
        type='DIVIDER',
        action=Action.NONE,
        data={}
    )
    _base_widget(widget)


def table(
        data: any,
        columns: [str] = None,
        id: str | int = None) -> None:
    if not columns:
        columns = _get_columns_from_data(data)
    if not columns:
        columns = []

    if not id:
        id = str(''.join(columns)) + 'TABLE'

    data = _convert_data_to_list_of_lists(data)

    widget = _Widget(
        id=id,
        type='TABLE',
        action=Action.NONE,
        data={
            'data': data,
            'columns': columns,
        }
    )
    _base_widget(widget)


def area_chart(
        data: any,
        columns: [str] = None,
        spline: bool = False,
        zoom: bool = False,
        subchart: bool = False,
        legend: bool = True,
        tooltip: bool = True,
        linear_gradient: bool = True,
        id: str | int = None) -> None:
    if not columns:
        columns = _get_columns_from_data(data)
    if not columns:
        columns = []

    if not id:
        id = str(''.join(columns)) + 'AREA_CHART'

    data = _convert_data_to_list_of_lists(data)
    data = _insert_columns_before_data(data, columns)
    data = _transpose_data(data)

    widget = _Widget(
        id=id,
        type='AREA_CHART',
        action=Action.NONE,
        data={
            'data': data,
            'columns': columns,
            'spline': spline,
            'zoom': zoom,
            'subchart': subchart,
            'legend': legend,
            'tooltip': tooltip,
            'linear_gradient': linear_gradient,
        }
    )
    _base_widget(widget)


def image(
        img: str | bytes = None,
        type: str = None,
        filepath: str = None,
        path_scope: PathScope | str = PathScope.USER,
        id: str | int = None) -> None:
    if img:
        if isinstance(img, bytes):
            base64encoded, type = _load_base64_image(img)
        else:
            base64encoded = img
    elif filepath:
        base64encoded, type = _load_base64_image(path(filepath, scope=path_scope))
    else:
        raise ValueError('Either img or filepath must be provided!')
    if not type:
        raise ValueError('Image type format must be provided!')

    if not id:
        id = str(base64encoded) + 'IMAGE'

    widget = _Widget(
        id=id,
        type='IMAGE',
        action=Action.NONE,
        data={
            'base64': base64encoded,
            'type': type,
        }
    )
    _base_widget(widget)
