import multiprocessing as mp
import os.path
from transparentai.models import explainers

from ...models import Model
from ...models import Dataset
from ...models.modules import ModuleInterpretability
from ...utils.db import exists_in_db, select_from_db
from ...utils.file import read_dataset_file
from ...utils.errors import get_errors
from ...utils import key_in_dict_not_empty, is_empty

from ...utils.components import format_str_strip, clean_errors, init_model_module_db
from .modules.interpretability import compute_global_influence

from threading import Thread
import concurrent.futures

import gc
import joblib
import pickle


def read_with_pickle(path):
    """
    """
    with open(path, 'rb') as file:
        obj = pickle.load(file)
    file.close()

    return obj


def read_with_joblib(path):
    """
    """
    obj = joblib.load(path)

    return obj


def read_model(path, file_type):
    """
    """
    valid_types = ['pickle', 'joblib']
    if file_type not in valid_types:
        raise ValueError('file_type has to be in %s' % str(valid_types))

    if file_type == 'pickle':
        read_fn = read_with_pickle
    elif file_type == 'joblib':
        read_fn = read_with_joblib

    return read_fn(path)


def is_model_file_readable(path, file_type):
    """
    """
    try:
        read_model(path, file_type)
    except:
        return False

    return True


def model_has_predict_function(model):
    """
    """
    return hasattr(model, 'predict')


def is_model_columns_valid(dataset, model):
    """
    """
    columns = dataset.model_columns
    df = read_dataset_file(dataset.path, nrows=1)

    X = df[columns]
    try:
        model.predict(X)
    except:
        return False

    return True


# ======= FORMAT MODEL FUNCTIONS ======= #


def format_model_name(form_data):
    """
    """
    return format_str_strip(form_data, key='name')


def format_model_path(form_data):
    """
    """
    return format_str_strip(form_data, key='path')


def format_model_dataset_name(form_data):
    """
    """
    return format_str_strip(form_data, key='dataset_name')


def format_model_file_type(form_data):
    """
    """
    return format_str_strip(form_data, key='file_type')


def get_model_dataset_from_name(form_data):
    """
    """
    if not key_in_dict_not_empty('dataset_name', form_data):
        return None

    dataset_name = form_data['dataset_name']

    dataset = select_from_db(Dataset, 'name', dataset_name)
    if type(dataset) == Dataset:
        return dataset

    return None


# ======= CONTROL MODEL FUNCTIONS ======= #


def control_model_name(form_data):
    """
    """
    errors_dict = get_errors()

    if 'name' not in form_data:
        return errors_dict['ModelNameNotSet']

    name = format_model_name(form_data)

    if exists_in_db(Model.name, name):
        return errors_dict['ModelNameAlreadyUsed']
    return None


def control_model_path(form_data, file_type):
    """
    """
    errors_dict = get_errors()

    if 'path' not in form_data:
        return None, None

    path = format_model_path(form_data)

    if path == '':
        return None, None
    if file_type == '':
        return errors_dict['ModelPathNoType'], None

    # Check if path is valid
    if not os.path.exists(path):
        return errors_dict['ModelPathNotExists'], None

    # Check if we can read the file
    if not is_model_file_readable(path, file_type):
        return errors_dict['ModelPathCantOpen'], None

    model = read_model(path, file_type)

    if not model_has_predict_function(model):
        return errors_dict['ModelPathNoPredictFunction']

    return None, model


def control_model_file_type(form_data):
    """
    """
    errors_dict = get_errors()

    if 'file_type' not in form_data:
        return None

    file_type = format_model_file_type(form_data)

    if file_type == '':
        return None

    valid_types = ['pickle', 'joblib']

    if file_type not in valid_types:
        return errors_dict['ModelFileTypeNotValid']

    return None


def control_model_dataset(form_data, model):
    """
    """
    errors_dict = get_errors()

    if 'dataset_name' not in form_data:
        return None

    dataset_name = format_model_dataset_name(form_data)

    if dataset_name == '':
        return None

    if model is None:
        return errors_dict['ModelDatasetNoModel']

    if not exists_in_db(Dataset.name, dataset_name):
        return errors_dict['ModelDatasetNameNotValid']

    dataset = get_model_dataset_from_name(form_data)

    # Check if dataset has model_columns
    if is_empty(dataset.model_columns):
        return errors_dict['ModelDatasetNoModelColumns']

    # Check if model_columns can be put in model.predict()
    if not is_model_columns_valid(dataset, model):
        return errors_dict['ModelDatasetModelColumnsNotValid']

    return None


def control_model(form_data, create=False, obj=None):
    """
    """
    errors = dict()

    if create:
        errors['name'] = control_model_name(form_data)

    errors['file_type'] = control_model_file_type(form_data)
    file_type = format_model_file_type(form_data)

    model = None
    if errors['file_type'] is None:
        errors['path'], model = control_model_path(form_data, file_type)

    errors['dataset_name'] = control_model_dataset(form_data, model)

    errors = clean_errors(errors)

    return errors


def format_model(form_data, create=False, obj=None):
    """
    """
    data = dict()

    if create:
        data['name'] = format_model_name(form_data)

    data['path'] = format_model_path(form_data)
    data['file_type'] = format_model_file_type(form_data)

    if key_in_dict_not_empty('dataset_name', form_data):
        dataset = get_model_dataset_from_name(form_data)

        if dataset is not None:
            data['dataset'] = dataset
            data['dataset_id'] = dataset.id

    return data


# ====== Modules init ====== #


def load_model_explainer(model):
    """
    """
    nrows = 1000
    nrows = model.dataset.length if nrows > model.dataset.length else nrows

    df = read_dataset_file(model.dataset.path, nrows=nrows)
    df = df[model.dataset.model_columns]

    model_obj = read_model(model.path, model.file_type)

    return load_model_explainer_from_obj(model_obj, df)


def load_model_explainer_from_obj(model_obj, df):
    """
    """
    # Check if model is from xgboost
    if 'xgboost' in str(type(model_obj)):
        model_type = 'tree'
    else:
        model_type = None

    explainer = explainers.ModelExplainer(model_obj, df, model_type=model_type)
    explainer.model = None
    gc.collect()

    return explainer


def load_dataset_sample(dataset, nrows=None):
    """
    """
    if (nrows is not None) & (dataset.length is not None):
        nrows = dataset.length if nrows > dataset.length else nrows

    with concurrent.futures.ThreadPoolExecutor() as executor:
        print('Launch model module thread : load_dataset_sample')
        future = executor.submit(read_dataset_file, dataset.path, nrows)
        df = future.result()

    return df


def load_model_thread(model):
    """
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print('Launch module module thread : load_model_thread')
        future = executor.submit(read_model, model.path, model.file_type)
        model = future.result()

    return model


def load_interpretability_module(model, model_obj, df):
    """
    """
    print('Launch model module thread : compute_global_influence')
    df = df[model.dataset.model_columns]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        print('Launch model module thread : load_dataset_sample')
        future = executor.submit(load_model_explainer_from_obj, model_obj, df)
        explainer = future.result()

    thread = Thread(target=compute_global_influence,
                    args=(
                        model,
                        explainer,
                        df,
                    ))
    thread.start()


def init_model_modules(model):
    """
    """
    # init interpretability module
    if model.module_interpretability is None:
        init_model_module_db(ModuleInterpretability, model=model)


def load_model_modules_in_background(model, data):
    """
    """
    init_model_modules(model)
    gc.collect()

    print(data)

    if key_in_dict_not_empty('dataset', data):
        df = load_dataset_sample(data['dataset'], nrows=1000)
        gc.collect()

        model_obj = load_model_thread(model)
        gc.collect()

        load_interpretability_module(model, model_obj, df)
        gc.collect()
