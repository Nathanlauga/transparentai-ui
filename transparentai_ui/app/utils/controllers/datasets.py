import pandas as pd
import os.path

from ...models.components import Dataset
from ...utils import exists_in_db

from .common import format_str_strip


def get_file_extension(fpath):
    """Returns the extension of a given file
    Parameters
    ----------
    fpath: str
        Path of a file
    Returns
    -------
    str:
        extension of the given file
        the text after the last dot
    """
    return str(fpath).split('.')[-1]


def is_path_extension_valid(path):
    """
    """
    ext = get_file_extension(path)

    return (ext == 'csv') | (ext.startswith('xls'))


def is_file_readable(path):
    """
    """
    ext = get_file_extension(path)

    if ext == 'csv':
        try:
            pd.read_csv(path, sep=None, engine='python', nrows=1)
        except:
            return False
    elif ext.startswith('xls'):
        try:
            pd.read_excel(path, nrows=1)
        except:
            return False
    else:
        return False
    return True

def get_columns_from_file(path):
    """
    """
    ext = get_file_extension(path)

    if ext == 'csv':
        try:
            data = pd.read_csv(path, sep=None, engine='python', nrows=0)
        except:
            return None
    elif ext.startswith('xls'):
        try:
            data = pd.read_excel(path, nrows=0)
        except:
            return None
    else:
        return None
    return list(data.columns.values)


def format_dataset_name(form_data):
    """
    """
    return format_str_strip(form_data, key='name')

def format_dataset_path(form_data):
    """
    """
    return format_str_strip(form_data, key='path')


def format_dataset_columns(form_data, key):
    """
    """
    if key not in form_data:
        return ''

    col_names = form_data[key]

    if type(col_names) == str:
        if col_names.startswith('[') & col_names.endswith(']'):
            tmp = col_names[1:-1]
            tmp = tmp.split("'")
            return list(set([e for e in tmp if e.strip() not in ['',',']]))
    else:
        col_names = list(set(col_names))

    return col_names


def control_dataset_name(form_data):
    """
    """
    if 'name' not in form_data:
        return 'The name of the dataset is not set'

    name = format_dataset_name(form_data)

    if exists_in_db(Dataset.name, name):
        return 'The dataset name is already used.'
    return None

def control_dataset_path(form_data):
    """
    """
    if 'path' not in form_data:
        return None

    path = format_dataset_path(form_data)

    if path == '':
        return None

    # Check if path is valid
    if not os.path.exists(path):
        return 'The dataset path is not pointing to a file.'

    # Check if extension is valid
    if not is_path_extension_valid(path):
        return 'The dataset extension path is not valid.'

    # Check if we can read the file
    if not is_file_readable(path):
        return 'Impossible to open the dataset file. Check that you can open your file with an other application.'
        
    return None

def control_dataset_columns(form_data, key, columns):
    """
    """
    if key not in form_data:
        return None

    col_names = format_dataset_columns(form_data, key)

    if type(col_names) == str:
        col_names = [col_names]

    for col_name in col_names:
        if col_name not in columns:
            return '%s column not found in the data.'%col_name
    return None

def clean_errors(errors):
    """
    """
    new_errors = dict()
    for k,v in errors.items():
        if v is not None:
            new_errors[k] = v
    return new_errors


def control_dataset(form_data, create=False):
    """
    """
    errors = dict()

    if create:
        errors['name'] = control_dataset_name(form_data)
    
    errors['path'] = control_dataset_path(form_data)
    path = format_dataset_path(form_data)

    if (path != '') & (errors['path'] is None):
        columns = get_columns_from_file(path)

        errors['target'] = control_dataset_columns(form_data, 'target', columns)
        errors['score'] = control_dataset_columns(form_data, 'score', columns)
        errors['protected_attr'] = control_dataset_columns(form_data, 'protected_attr', columns)
        errors['model_columns'] = control_dataset_columns(form_data, 'model_columns', columns)

    errors = clean_errors(errors)

    return errors

def format_dataset(form_data, create=False):
    """
    """
    data = dict()

    if create:
        data['name'] = format_dataset_name(form_data)
    
    data['path'] = format_dataset_path(form_data)
    data['target'] = format_dataset_columns(form_data, key='target')
    data['score'] = format_dataset_columns(form_data, key='score')
    data['protected_attr'] = format_dataset_columns(form_data, key='protected_attr')
    data['model_columns'] = format_dataset_columns(form_data, key='model_columns')

    return data