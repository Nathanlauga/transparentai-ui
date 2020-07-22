from ...models import Project
from ...models import Dataset

from ...utils.db import exists_in_db, select_from_db

from ...utils.errors import get_errors
from ...utils import key_in_dict_not_empty, is_empty

from ...utils.components import format_str_strip, clean_errors


# ======= FORMAT MODEL FUNCTIONS ======= #


def format_project_name(form_data):
    """
    """
    return format_str_strip(form_data, key='name')


def format_project_dataset_name(form_data):
    """
    """
    return format_str_strip(form_data, key='dataset_name')

def format_project_desc(form_data):
    """
    """
    return format_str_strip(form_data, key='desc')


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


def format_project_members(form_data):
    """
    """
    if 'members' not in form_data:
        return ''

    members = form_data['members']

    if type(members) == str:
        if members.startswith('[') & members.endswith(']'):
            tmp = members[1:-1]
            tmp = tmp.split("'")
            return list(set([e for e in tmp if e.strip() not in ['', ',']]))
    else:
        members = list(set(members))

    return members


# ======= CONTROL MODEL FUNCTIONS ======= #


def control_project_name(form_data):
    """
    """
    errors_dict = get_errors()

    if 'name' not in form_data:
        return errors_dict['ProjectNameNotSet']

    name = format_project_name(form_data)

    if exists_in_db(Project.name, name):
        return errors_dict['ProjectNameAlreadyUsed']
    return None


def control_project_dataset(form_data):
    """
    """
    errors_dict = get_errors()

    if 'dataset_name' not in form_data:
        return None

    dataset_name = format_project_dataset_name(form_data)

    if dataset_name == '':
        return None

    if not exists_in_db(Dataset.name, dataset_name):
        return errors_dict['ProjectDatasetNameNotValid']

    return None


def control_project(form_data, create=False, obj=None):
    """
    """
    errors = dict()

    if create:
        errors['name'] = control_project_name(form_data)

    errors['dataset_name'] = control_project_dataset(form_data)

    errors = clean_errors(errors)

    return errors


def format_project(form_data, create=False, obj=None):
    """
    """
    data = dict()

    if create:
        data['name'] = format_project_name(form_data)

    data['desc'] = format_project_desc(form_data)
    data['members'] = format_project_members(form_data)

    if key_in_dict_not_empty('dataset_name', form_data):
        dataset = get_model_dataset_from_name(form_data)

        if dataset is not None:
            data['dataset'] = dataset

    return data
