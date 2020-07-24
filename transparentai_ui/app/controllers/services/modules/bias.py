from transparentai import fairness
from transparentai import utils
import numpy as np

from ....utils.db import update_in_db, select_from_db
from ....utils.errors import get_errors
from ....utils import is_empty, key_in_dict_not_empty
from ....utils.components import clean_errors, format_bool, format_int

from ....models import Dataset
from ....models.modules import ModuleBias


# ======= FORMAT MODULE FUNCTIONS ======= #


def format_module_group_selection(form_data):
    """
    """
    if not key_in_dict_not_empty('group_selection', form_data):
        return None

    return form_data['group_selection']


def format_module_privileged_group(form_data, key, module, group_selection='majority'):
    """
    """
    # if not key_in_dict_not_empty('privileged_group', form_data):
    #     return None

    privileged_group = module.privileged_group

    if not key_in_dict_not_empty(key, privileged_group):
        return None

    privileged_group[key]['privileged_values'] = [privileged_group[key]['values'][0]]

    if group_selection == 'custom':
        if not key_in_dict_not_empty(key, form_data):
            return None

        if privileged_group[key]['dtype'] == 'object':
            privileged_group[key]['privileged_values'] = form_data.getlist(key)
        else:
            privileged_group[key]['privileged_values'] = [float(form_data[key])]

    return privileged_group[key]


# ======= CONTROL MODULE FUNCTIONS ======= #


def control_module_group_selection(form_data):
    """
    """
    errors_dict = get_errors()

    if not key_in_dict_not_empty('group_selection', form_data):
        # TODO change error message
        return errors_dict['PandasProfMinimalNotSet']

    group_selection = format_module_group_selection(form_data)

    if group_selection is None:
        # TODO change error message
        return errors_dict['PandasProfMinimalNotValid']

    return None


def control_module_privileged_group(form_data, key, module):
    """
    """
    errors_dict = get_errors()

    if not key_in_dict_not_empty('privileged_group', form_data):
        return None

    attr = format_module_privileged_group(form_data, key, module)

    if attr is None:
        # TODO change error message
        return errors_dict['PandasProfNrowsNotValid']

    for val in attr['privileged_values']:
        if val not in attr['values']:
            # TODO change error message
            return errors_dict['PandasProfNrowsNotValid'] + f'({val})'

    return None


def control_module(form_data, create=False, obj=None):
    """
    """
    errors = dict()

    errors['group_selection'] = control_module_group_selection(form_data)

    attributes = list(obj.privileged_group.keys()) #[k for k in form_data.keys() if k.startswith('attr_')]
    for attr in attributes:
        errors[attr] = control_module_privileged_group(
            form_data, key=attr, module=obj)

    errors = clean_errors(errors)

    return errors


def format_module(form_data, create=False, obj=None):
    """
    """
    data = dict()

    data['group_selection'] = format_module_group_selection(form_data)

    attributes = list(obj.privileged_group.keys()) #[k for k in form_data.keys() if k.startswith('attr_')]
    privileged_group = {}

    for attr in attributes:
        res = format_module_privileged_group(
            form_data, key=attr, module=obj, group_selection=data['group_selection'])

        if res is None:
            privileged_group[attr] = obj.privileged_group[attr] 
        else:
            privileged_group[attr] = res
    
    if privileged_group != {}:
        data['privileged_group'] = privileged_group

    return data

# LOAD MODULE FUNCTIONS


def init_bias_module(df, dataset):
    """
    """
    module = select_from_db(ModuleBias, 'dataset_id', dataset.id)
    update_in_db(module, {'status': 'loading'})

    y_true = df[dataset.target]
    y_pred = df[dataset.score]

    privileged_group = {}
    for attr in dataset.protected_attr:
        privileged_group[attr] = {}
        dtype = utils.find_dtype(df[attr], len_sample=1000)
        uniq_values = list(df[attr].value_counts().index)

        if dtype != 'object':
            if len(uniq_values) > 10:
                uniq_values = [round(np.mean(uniq_values),2)]
            else:
                dtype = 'object'
                uniq_values = list(df[attr].value_counts().index)

        privileged_group[attr]['dtype'] = dtype
        privileged_group[attr]['values'] = uniq_values

    data = {'status': 'loaded', 'privileged_group': privileged_group}

    try:
        res = update_in_db(module, data)

        if res != 'updated':
            update_in_db(module, {'status': 'failed'})

    except:
        update_in_db(module, {'status': 'failed'})


def compute_bias_metrics(df, dataset):
    """
    """
    module = select_from_db(ModuleBias, 'dataset_id', dataset.id)
    update_in_db(module, {'status': 'loading'})

    y_true = df[dataset.target]
    y_pred = df[dataset.score]

    if is_empty(module.privileged_group):
        update_in_db(module, {'status': 'failed'})
        return
        
    privileged_group = module.privileged_group
    priv_format = {}
    
    for k, v in privileged_group.items():
        if privileged_group[k]['dtype'] != 'object':
            priv_format[k] = lambda x: x > float(privileged_group[k]['privileged_values'][0])
        else: 
            priv_format[k] = privileged_group[k]['privileged_values']

    results = fairness.model_bias(y_true, y_pred, df, priv_format)

    data = {'status': 'loaded', 'results': results}

    try:
        res = update_in_db(module, data)

        if res != 'updated':
            update_in_db(module, {'status': 'failed'})

    except:
        update_in_db(module, {'status': 'failed'})
