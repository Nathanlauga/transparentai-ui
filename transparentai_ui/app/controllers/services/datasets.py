import pandas as pd
import os.path
from encodings.aliases import aliases

from ...models import Project, Dataset
from ...utils import key_in_dict_not_empty, is_empty

from ...utils.errors import get_errors

from ...utils import drop_dupplicates_values
from ...utils.components import format_str_strip, clean_errors, update_dataset_module_db, init_dataset_module_db
from ...utils.file import get_file_extension, read_dataset_file, get_file_length
from ...utils.db import select_from_db, exists_in_db, update_in_db

from .modules import generate_pandas_prof_report
from .modules import compute_performance_metrics
from .modules import bias

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


def is_dataset_file_readable(path, sep=',', encoding='utf_8'):
    """
    """
    ext = get_file_extension(path)

    if ext == 'csv':
        try:
            pd.read_csv(path, sep=sep, encoding=encoding, nrows=1)
        except:
            return False
    elif ext.startswith('xls'):
        try:
            pd.read_excel(path, encoding=encoding, nrows=1)
        except:
            return False
    else:
        return False
    return True


def get_columns_from_file(path, sep=',', encoding='utf_8'):
    """
    """
    ext = get_file_extension(path)

    if ext == 'csv':
        try:
            data = pd.read_csv(path, sep=sep, encoding=encoding, nrows=0)
        except:
            return None
    elif ext.startswith('xls'):
        try:
            data = pd.read_excel(path, encoding=encoding, nrows=0)
        except:
            return None
    else:
        return None
    return list(data.columns.values)


def get_project_from_name(form_data):
    """
    """
    if not key_in_dict_not_empty('project_name', form_data):
        return None

    project_name = form_data['project_name']

    project = select_from_db(Project, 'name', project_name)
    if type(project) == Project:
        return project

    return None


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

    col_names = form_data.getlist(key)
    if len(col_names) == 1:
        col_names = col_names[0]

    if type(col_names) == str:
        if col_names.startswith('[') & col_names.endswith(']'):
            tmp = col_names[1:-1]
            tmp = tmp.split("'")
            return drop_dupplicates_values([e for e in tmp if e.strip() not in ['', ',']])
    else:
        col_names = drop_dupplicates_values(col_names)

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


def control_dataset_sep(form_data):
    """
    """
    errors_dict = get_errors()

    if not key_in_dict_not_empty('sep', form_data):
        return errors_dict['DatasetSepNotSet']

    return None


def control_dataset_encoding(form_data):
    """
    """
    errors_dict = get_errors()

    if not key_in_dict_not_empty('encoding', form_data):
        return errors_dict['DatasetEncodingNotSet']

    encoding = form_data['encoding']

    if encoding not in list(set([v for k, v in aliases.items()])):
        return errors_dict['DatasetEncodingNotValid']

    return None


def control_dataset_path(form_data):
    """
    """
    errors_dict = get_errors()

    if 'path' not in form_data:
        return None

    path = format_dataset_path(form_data)

    if path == '':
        return errors_dict['DatasetPathNotExists']

    # Check if path is valid
    if not os.path.exists(path):
        return errors_dict['DatasetPathNotExists']

    # Check if extension is valid
    if not is_dataset_extension_valid(path):
        return errors_dict['DatasetPathExtension']

    check_sep = control_dataset_sep(form_data)
    if check_sep is not None:
        return errors_dict['DatasetPathSepNotValid']

    check_encoding = control_dataset_encoding(form_data)
    if check_encoding is not None:
        return errors_dict['DatasetPathEncodingNotValid']

        # Check if we can read the file
    if not is_dataset_file_readable(path, sep=form_data['sep'], encoding=form_data['encoding']):
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


def control_dataset(form_data, create=False, obj=None):
    """
    """
    errors = dict()

    if create:
        errors['name'] = control_dataset_name(form_data)

    if key_in_dict_not_empty('path', form_data):
        errors['path'] = control_dataset_path(form_data)
        path = format_dataset_path(form_data)
    else:
        path = obj.path

    sep = form_data['sep'] if key_in_dict_not_empty(
        'sep', form_data) else obj.sep
    encoding = form_data['encoding'] if key_in_dict_not_empty(
        'encoding', form_data) else obj.encoding

    if path != '':
        columns = get_columns_from_file(
            path, sep=sep, encoding=encoding)

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


def format_dataset(form_data, create=False, obj=None):
    """
    """
    data = dict()

    if create:
        data['name'] = format_dataset_name(form_data)

    # Advanced params
    sep = form_data['sep'] if key_in_dict_not_empty(
        'sep', form_data) else obj.sep
    encoding = form_data['encoding'] if key_in_dict_not_empty(
        'encoding', form_data) else obj.encoding

    data['sep'] = sep
    data['encoding'] = encoding

    if key_in_dict_not_empty('path', form_data):
        data['path'] = format_dataset_path(form_data)
        data['columns'] = get_columns_from_file(
            form_data['path'], sep=sep, encoding=encoding)

    data['target'] = format_dataset_columns(form_data, key='target')
    data['score'] = format_dataset_columns(form_data, key='score')
    data['model_type'] = format_dataset_model_type(form_data)
    data['protected_attr'] = format_dataset_columns(
        form_data, key='protected_attr')
    data['model_columns'] = format_dataset_columns(
        form_data, key='model_columns')

    if key_in_dict_not_empty('project_name', form_data):
        project = get_project_from_name(form_data)

        if project is not None:
            data['project'] = project
            data['project_id'] = project.id

    return data


# ====== Modules init ====== #


def load_pandas_profiling_module(df, title, explorative, dataset, minimal):
    """
    """
    print('Launch dataset module thread : load_pandas_profiling_module')
    thread = Thread(target=generate_pandas_prof_report,
                    args=(df, title, explorative, dataset, minimal,))
    thread.start()


def init_bias_module(df, dataset):
    """
    """
    if (is_empty(dataset.path)) | (is_empty(dataset.score)) | (is_empty(dataset.model_type)) | (
            is_empty(dataset.target)) | (is_empty(dataset.protected_attr)):
        return

    print('Launch dataset module thread : init_bias_module')
    thread = Thread(target=bias.init_bias_module,
                    args=(df, dataset,))
    thread.start()


def load_bias_module(df, dataset):
    """
    """
    print('Launch dataset module thread : load_bias_module')
    thread = Thread(target=bias.compute_bias_metrics,
                    args=(df, dataset,))
    thread.start()


def load_bias_module_without_df(dataset):
    """
    """
    update_dataset_module_db(
        ModuleBias, dataset=dataset, status='loading')
    try:
        df = load_dataset_from_path(
            dataset.path, sep=dataset.sep, encoding=dataset.encoding)
    except:
        update_dataset_module_db(
            ModuleBias, dataset=dataset, status='failed')
        return

    load_bias_module(df, dataset)


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



def load_dataset_from_path(path, sep=',', encoding='utf_8', nrows=None):
    """
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print('Launch dataset module thread : read_dataset_file')
        future = executor.submit(read_dataset_file, path, nrows, sep, encoding)
        df = future.result()

    return df


def load_pandas_prof_report(title, dataset, nrows=None, explorative=False, minimal=True):
    """
    """
    update_dataset_module_db(
        ModulePandasProfiling, dataset=dataset, status='loading')
    try:
        df = load_dataset_from_path(
            dataset.path, sep=dataset.sep, encoding=dataset.encoding, nrows=nrows)
    except:
        update_dataset_module_db(
            ModulePandasProfiling, dataset=dataset, status='failed')
        return

    load_pandas_profiling_module(
        df, title=dataset.name, explorative=explorative, dataset=dataset, minimal=minimal)


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


def set_dataset_length(dataset):
    """
    """
    nrows = get_file_length(dataset.path)

    data = {'length': nrows}
    update_in_db(dataset, data)


def load_dataset_modules(dataset, data):
    """Loads the Dataset modules in background using Thread.

    It applies the following rules:

    If the path is refer in the data dictionnary (it means it has been updated) then:

    - Load the full dataset and generate pandas profiling report
    - If the score, target and model_type are set : Load the performance module
    - If the score, target, model_type and protected_attr are set : Load the bias module

    Else if the path is set:

    - Load the full dataset but do not generate a new pandas profiling report
    - If the score, target and model_type are set : Load the performance module
    - If the score, target, model_type and protected_attr are set : Load the bias module

    """
    df = None

    if key_in_dict_not_empty('path', data):
        df = load_dataset_from_path(
            data['path'], sep=dataset.sep, encoding=dataset.encoding)

        load_pandas_profiling_module(
            df, title=dataset.name, explorative=False, dataset=dataset, minimal=True)

    elif dataset.path != '':
        df = load_dataset_from_path(
            dataset.path, sep=dataset.sep, encoding=dataset.encoding)

        if key_in_dict_not_empty('sep', data) | key_in_dict_not_empty('encoding', data):
            load_pandas_profiling_module(
                df, title=dataset.name, explorative=False, dataset=dataset, minimal=True)

    if df is not None:
        load_performance_module(df, dataset=dataset)
        init_bias_module(df, dataset=dataset)


def load_dataset_modules_in_background(dataset, data):
    """
    """
    init_dataset_modules(dataset)

    if key_in_dict_not_empty('path', data):
        set_dataset_length(dataset)
        update_dataset_module_db(
            ModulePandasProfiling, dataset=dataset, status='loading')

    thread = Thread(target=load_dataset_modules, args=(dataset, data,))
    thread.start()
