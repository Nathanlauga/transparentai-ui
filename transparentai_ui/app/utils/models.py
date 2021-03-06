import json
from ..utils import drop_dupplicates_values
import numpy as np


def get_request_attribute(form_data, key, default=''):
    """
    """
    if key not in form_data:
        return ''
    return form_data[key]


def get_component_args(data, attributes):
    """
    """
    args = dict()

    # Retrieve Attributes from request.form
    for attr in attributes:
        args[attr] = get_request_attribute(data, attr)

    return args


def list_property(attr, unique=False):
    format_list = [
        str(x).replace('//,', ';') for x in attr.split(';') if str(x) != ''
    ]
    if unique:
        return drop_dupplicates_values(format_list)
    return format_list


def list_property_setter(attr, values):
    if attr is None:
        attr = ''

    attr = ''
    if type(values) == list:
        for v in values:
            v = v.replace(';', '//,')
            attr += ';%s' % str(v)
    else:
        value = values.replace(';', '//,')
        attr += ';%s' % str(value)

    return attr


def dict_property(attr):
    if (str(attr) == ''):
        return {}

    try:
        json_str = str(attr).replace("'", '"')
        # Handle numpy array string
        json_str = json_str.replace('array(', '').replace('])', ']')
        res = json.loads(json_str)
    except:
        return str(attr).replace("'", '"')

    return res


def dict_property_setter(new_dict):
    """Formats a dictionary into a string that can 
    be reused as a dict using `json.loads()` function.

    Parameters
    ----------
    new_dict: dict
        Dictionary to format

    Returns
    -------
    dict:
        Formated dictionary 
    """
    if new_dict is None:
        return '{}'

    formated_dict = new_dict

    for k, v in new_dict.items():
        if type(v) == np.ndarray:
            formated_dict[k] = v.tolist()

    return str(formated_dict).replace("'", '"')