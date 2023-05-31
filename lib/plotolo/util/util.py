import os
import hashlib
import json
from enum import Enum
from uuid import uuid4


def generate_id():
    return str(uuid4())


def to_json(object):
    def obj_handler(obj):
        if isinstance(obj, Enum):
            return obj.value
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            raise TypeError(f'Object of type {type(obj)} with value of {repr(obj)} is not JSON serializable')

    return json.dumps(object, default=obj_handler)


def from_json(json_str: str) -> dict[str, any]:
    return json.loads(json_str)


def get_filename(path, with_extension=False) -> str:
    filename = path.split('/')[-1].split('\\')[-1]
    if with_extension:
        return filename
    else:
        return filename.split('.')[0]  # todo use os.path.splitext


def get_absolute_path(relative_path, from_file=__file__) -> str:
    current_dir = os.path.dirname(from_file)
    return os.path.join(current_dir, relative_path)  # todo use os.path.abspath


def hash_string(string):
    return str(hashlib.sha1(str(string).encode("utf-8")).hexdigest())


def hash_object(object):
    return hash_string(to_json(object))


def pprint_module(module):
    # only for debug purposes
    import pprint
    pp = pprint.PrettyPrinter(depth=4)
    builtins = ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__', '__builtins__']
    user_data = {key: module.__dict__[key] for key in module.__dict__ if key not in builtins}
    pp.pprint(f"{user_data=}")


def pprint_file_structure(directory, indent=''):
    # only for debug purposes
    for entry in os.scandir(directory):
        if entry.is_file():
            print(indent + entry.name)
        elif entry.is_dir():
            print(indent + entry.name + '/')
            pprint_file_structure(entry.path, indent + '  ')


