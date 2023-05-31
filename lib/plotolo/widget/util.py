import os
import base64
import imghdr

import numpy as np
import pandas as pd


def convert_data_to_list_of_lists(data: any):
    """
    Converts any data to a list of lists (table of rows), if possible, otherwise raises an error
    """
    error_message = "Unsupported data type. Supported types are: tuple, list, set, list of lists, \
                        list of tuples, list of dicts, dict of lists,  \
                        pandas DataFrame, 2D numpy array, 2D numpy matrix."
    if isinstance(data, list):
        if isinstance(data[0], list):
            # list of lists
            return data
        elif isinstance(data[0], dict):
            # list of dicts
            return [list(d.values()) for d in data]
        elif isinstance(data[0], tuple):
            # list of tuples
            return [list(t) for t in data]
        else:
            raise ValueError("Unsupported list type. List items must all be either lists, tuples, or dictionaries.")
    elif isinstance(data, dict):
        if isinstance(list(data.values())[0], list):
            # dict of lists
            return list(zip(*data.values()))
        else:
            raise ValueError("Unsupported dictionary type. Dictionary values must all be lists.")
    elif isinstance(data, pd.DataFrame):
        # pandas dataframe
        return data.values.tolist()
    elif isinstance(data, np.ndarray) or isinstance(data, np.matrix):
        if len(data.shape) == 2:
            # numpy 2D array or 2D matrix
            return data.tolist()
        else:
            raise ValueError("Only 2D numpy arrays and 2D numpy matrices are supported.")
    elif isinstance(data, (tuple, list, set)):
        # tuple, list, or set
        return [list(data)]
    else:
        raise ValueError(error_message)


def get_columns_from_data(data):
    """
    Returns the column names from the data
    if it is a pandas DataFrame or a list of dicts or a dict of lists
    """
    if isinstance(data, pd.DataFrame):
        return list(data.columns)
    elif isinstance(data, dict):
        # keys in dict are ordered in python 3.6+
        return list(data.keys())
    elif isinstance(data, list):
        if isinstance(data[0], dict):
            return list(data[0].keys())


def insert_columns_before_data(data: [[any]], columns: [str]):
    """
    Inserts the column names before each column in the data.
    """
    if len(data[0]) != len(columns):
        raise ValueError("The number of column names must match the number of columns in the data.")

    return [columns] + data


def transpose_data(data: [[any]]):
    """
    Transposes the data (table of rows to table of columns).
    """
    return list(map(list, zip(*data)))


def load_base64_image(img: str | bytes) -> (str, str):
    """
    Load image from base64 string or file path and return base64 string and image type.
    """
    if isinstance(img, bytes):
        return base64.b64encode(img).decode('utf-8'), imghdr.what(None, img)

    with open(img, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8'), os.path.splitext(img)[1][1:]