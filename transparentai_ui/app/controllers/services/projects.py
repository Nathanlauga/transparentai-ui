from ...models import Project
from ...models import Dataset
from ...models.modules import ModuleSustainable
from ...src import get_questions

import json

from ...utils.db import exists_in_db, select_from_db, update_in_db

from ...utils.errors import get_errors
from ...utils import key_in_dict_not_empty, is_empty

from ...utils.components import format_str_strip, clean_errors, init_project_module_db


def init_anwsers(project):
    """
    """
    questions = get_questions()
    ids = [(elem['id'], len(elem['questions'])) for k, section in questions.items() for elem in section]

    answers = {}
    for id, n_questions in ids:
        answers[str(id)] = ['None' for i in range(n_questions)]

    data = {
        "answers": answers
    }

    res = update_in_db(project, data)

# ======= FORMAT MODEL FUNCTIONS ======= #


def format_answers(project, form_data):
    """
    """
    if project is None:
        return {}

    answers = project.answers

    keys = [k for k, v in form_data.items() if 'answers' in k]

    if len(keys) == 0:
        return answers

    for k in keys:
        splt = k.split('_')
        aspect_id = splt[1]
        order = splt[2]

        if order == "None":
            answers[aspect_id][0] = form_data[k]
        else:
            answers[aspect_id][int(order)] = form_data[k]

    return answers


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

    print(form_data)
    if create:
        data['name'] = format_project_name(form_data)

    data['desc'] = format_project_desc(form_data)
    data['members'] = format_project_members(form_data)
    data['answers'] = format_answers(obj, form_data)

    if key_in_dict_not_empty('dataset_name', form_data):
        dataset = get_model_dataset_from_name(form_data)

        if dataset is not None:
            data['dataset'] = dataset

    return data

# ============================ #

def load_modules(project, data):
    """
    """
    # init sustainable module
    if project.module_sustainable is None:
        init_project_module_db(ModuleSustainable, project=project)