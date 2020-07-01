from ...utils.db import init_component_module
from ...models.modules import ModulePandasProfiling
import pandas as pd
import os.path

from ...models import Dataset
from ...utils import exists_in_db

from ...utils.errors import get_errors

from ...utils.components import format_str_strip, clean_errors
from ...utils.file import get_file_extension, read_dataset_file

from .modules import generate_pandas_prof_report

from threading import Thread
import concurrent.futures


def is_dataset_extension_valid(path):
    """
    """
    ext = get_file_extension(path)

    return (ext == 'csv') | (ext.startswith('xls'))


def is_dataset_file_readable(path):
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


# ======= FORMAT DATASET FUNCTIONS ======= #


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
            return list(set([e for e in tmp if e.strip() not in ['', ',']]))
    else:
        col_names = list(set(col_names))

    return col_names


# ======= CONTROL DATASET FUNCTIONS ======= #


def control_dataset_name(form_data):
    """
    """
    errors_dict = get_errors()

    if 'name' not in form_data:
        return errors_dict['DatasetNameNotSet']

    name = format_dataset_name(form_data)

    if exists_in_db(Dataset.name, name):
        return errors_dict['DatasetNameAlreadyUsed']
    return None


def control_dataset_path(form_data):
    """
    """
    errors_dict = get_errors()

    if 'path' not in form_data:
        return None

    path = format_dataset_path(form_data)

    if path == '':
        return None

    # Check if path is valid
    if not os.path.exists(path):
        return errors_dict['DatasetPathNotExists']

    # Check if extension is valid
    if not is_dataset_extension_valid(path):
        return errors_dict['DatasetPathExtension']

    # Check if we can read the file
    if not is_dataset_file_readable(path):
        return errors_dict['DatasetPathCantOpen']

    return None


def control_dataset_columns(form_data, key, columns):
    """
    """
    errors_dict = get_errors()

    if key not in form_data:
        return None
    if form_data[key] == '':
        return None

    col_names = format_dataset_columns(form_data, key)

    if type(col_names) == str:
        col_names = [col_names]

    for col_name in col_names:
        if col_name not in columns:
            return col_name + errors_dict['DatasetColumnNotFound']
    return None


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

        errors['target'] = control_dataset_columns(
            form_data, 'target', columns)
        errors['score'] = control_dataset_columns(form_data, 'score', columns)
        errors['protected_attr'] = control_dataset_columns(
            form_data, 'protected_attr', columns)
        errors['model_columns'] = control_dataset_columns(
            form_data, 'model_columns', columns)

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
    data['protected_attr'] = format_dataset_columns(
        form_data, key='protected_attr')
    data['model_columns'] = format_dataset_columns(
        form_data, key='model_columns')

    return data


# ====== Modules init ====== #

def load_pandas_profiling_module(df, title, explorative, dataset):
    """
    """
    thread = Thread(target=generate_pandas_prof_report,
                    args=(df, title, explorative, dataset,))
    thread.start()


def load_dataset_modules_in_background(dataset, data):
    """
    """
    if 'path' in data:
        if data['path'] != '':
            with concurrent.futures.ThreadPoolExecutor() as executor:
                print('load_dataset_modules : launch read_dataset_file thread')
                future = executor.submit(read_dataset_file, data['path'])
                df = future.result()

            if dataset.module_pandas_profiling is None:
                # init pandas profiling module
                init_component_module(
                    ModulePandasProfiling, dataset)#, module_attr='module_pandas_profiling')

            print('load_dataset_modules : launch load_pandas_profiling_module thread')
            load_pandas_profiling_module(
                df, title=dataset.name, explorative=False, dataset=dataset)
