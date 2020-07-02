import pandas as pd
import os.path

from ...models import Dataset
from ...utils import key_in_dict_not_empty, is_empty

from ...utils.errors import get_errors

from ...utils.components import format_str_strip, clean_errors, init_dataset_module_db
from ...utils.file import get_file_extension, read_dataset_file
from ...utils.db import select_from_db, exists_in_db, update_in_db

from .modules import generate_pandas_prof_report
from .modules import compute_performance_metrics
from .modules import compute_bias_metrics

from ...models.modules import ModulePandasProfiling
from ...models.modules import ModulePerformance
from ...models.modules import ModuleBias

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


def format_dataset_model_type(form_data):
    """
    """
    return format_str_strip(form_data, key='model_type')


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


def control_dataset_model_type(form_data):
    """
    """
    errors_dict = get_errors()

    if 'model_type' not in form_data:
        return None

    model_type = form_data['model_type']

    if model_type == '':
        return None

    valid_models = ['binary-classification',
                    'multiclass-classification', 'regression']
    if model_type not in valid_models:
        return errors_dict['DatasetModelTypeNotValid']

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
        errors['model_type'] = control_dataset_model_type(form_data)
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
    data['model_type'] = format_dataset_model_type(form_data)
    data['protected_attr'] = format_dataset_columns(
        form_data, key='protected_attr')
    data['model_columns'] = format_dataset_columns(
        form_data, key='model_columns')

    return data


# ====== Modules init ====== #


def load_pandas_profiling_module(df, title, explorative, dataset):
    """
    """
    print('Launch dataset module thread : load_pandas_profiling_module')
    thread = Thread(target=generate_pandas_prof_report,
                    args=(df, title, explorative, dataset,))
    thread.start()


def load_performance_module(df, dataset):
    """
    """
    if (is_empty(dataset.path)) | (is_empty(dataset.score)) | (
            is_empty(dataset.model_type)) | (is_empty(dataset.target)):
        return

    print('Launch dataset module thread : compute_performance_metrics')
    thread = Thread(target=compute_performance_metrics,
                    args=(df, dataset, None,))
    thread.start()


def load_bias_module(df, dataset):
    """
    """
    if (is_empty(dataset.path)) | (is_empty(dataset.score)) | (is_empty(dataset.model_type)) | (
            is_empty(dataset.target)) | (is_empty(dataset.protected_attr)):
        return

    print('Launch dataset module thread : compute_bias_metrics')
    thread = Thread(target=compute_bias_metrics,
                    args=(df, dataset,))
    thread.start()


def load_dataset_from_path(path):
    """
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print('Launch dataset module thread : read_dataset_file')
        future = executor.submit(read_dataset_file, path)
        df = future.result()

    return df


def init_dataset_modules(dataset):
    """
    """
    # init pandas profiling module
    if dataset.module_pandas_profiling is None:
        init_dataset_module_db(ModulePandasProfiling, dataset=dataset)

    # init bias module
    if dataset.module_bias is None:
        init_dataset_module_db(ModuleBias, dataset=dataset)

    # init performance module
    if dataset.module_performance is None:
        init_dataset_module_db(ModulePerformance, dataset=dataset)


def set_dataset_length(dataset, df):
    """
    """
    data = {'length': len(df)}
    update_in_db(dataset, data)


def load_dataset_modules_in_background(dataset, data):
    """
    """
    init_dataset_modules(dataset)

    if key_in_dict_not_empty('path', data):
        df = load_dataset_from_path(data['path'])
        set_dataset_length(dataset, df)

        load_pandas_profiling_module(
            df, title=dataset.name, explorative=False, dataset=dataset)
        load_performance_module(df, dataset=dataset)
        load_bias_module(df, dataset=dataset)

    elif dataset.path != '':
        df = load_dataset_from_path(dataset.path)
        set_dataset_length(dataset, df)

        load_performance_module(df, dataset=dataset)
        load_bias_module(df, dataset=dataset)
