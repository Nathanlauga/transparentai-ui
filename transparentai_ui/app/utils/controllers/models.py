import os.path

from ...models.components import Model
from ...utils import exists_in_db
from ...utils.errors import get_errors 

from .common import format_str_strip, clean_errors

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


def is_model_file_readable(path, file_type):
    """
    """
    read_fn = None

    if file_type == 'pickle':
        read_fn = read_with_pickle
    elif file_type == 'joblib':
        read_fn = read_with_joblib 

    if read_fn is None:
        return False
    try:
        read_fn(path)
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


def format_model_file_type(form_data):
    """
    """
    return format_str_strip(form_data, key='file_type')

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
        return None

    path = format_model_path(form_data)

    if path == '':
        return None
    if file_type == '':
        return errors_dict['ModelPathNoType'] 

    # Check if path is valid
    if not os.path.exists(path):
        return errors_dict['ModelPathNotExists']

    # Check if we can read the file
    if not is_model_file_readable(path, file_type):
        return errors_dict['ModelPathCantOpen']

    return None


def control_model_file_type(form_data):
    """
    """
    errors_dict = get_errors()

    if 'file_type' not in form_data:
        return None

    file_type = form_data['file_type']

    if file_type == '':
        return None

    valid_types = ['pickle', 'joblib']

    if file_type not in valid_types:
        return errors_dict['ModelFileTypeNotValid']
    
    return None


def control_model(form_data, create=False):
    """
    """
    errors = dict()

    if create:
        errors['name'] = control_model_name(form_data)

    errors['file_type'] = control_model_file_type(form_data)
    file_type = format_model_file_type(form_data)

    if errors['file_type'] is None:
        errors['path'] = control_model_path(form_data, file_type)

    errors = clean_errors(errors)

    return errors


def format_model(form_data, create=False):
    """
    """
    data = dict()

    if create:
        data['name'] = format_model_name(form_data)

    data['path'] = format_model_path(form_data)
    data['file_type'] = format_model_file_type(form_data)

    return data
