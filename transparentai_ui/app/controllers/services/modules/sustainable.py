from transparentai import sustainable
from os.path import dirname, abspath

from ....utils.db import update_in_db, select_from_db
from ....utils.errors import get_errors
from ....utils import key_in_dict_not_empty, is_empty
from ....utils.components import clean_errors, format_str, format_float

from ....models import Project
from ....models.modules import ModuleSustainable


# ======= FORMAT MODULE FUNCTIONS ======= #

def format_module_time(form_data):
    """
    """
    return format_float(form_data, key='time')


def format_module_location(form_data):
    """
    """
    return format_str(form_data, key='location')


def format_module_watts(form_data):
    """
    """
    return format_float(form_data, key='watts')


# ======= CONTROL MODULE FUNCTIONS ======= #


def control_module_time(form_data):
    """
    """
    # TODO : create a function with not set and not valid error
    errors_dict = get_errors()

    if not key_in_dict_not_empty('time', form_data):
        return errors_dict['SustainableTimeNotSet']

    time = format_module_time(form_data)

    if time is None:
        return errors_dict['SustainableTimeNotValid']

    if time <= 0:
        return errors_dict['SustainableTimeNotPositive']

    return None


def control_module_location(form_data):
    """
    """
    # TODO : create a function with not set and not valid error
    errors_dict = get_errors()

    if not key_in_dict_not_empty('location', form_data):
        return errors_dict['SustainableLocationNotSet']

    location = format_module_location(form_data)

    if location is None:
        return errors_dict['SustainableLocationNotValid']

    valid_locations = list(sustainable.get_energy_data().keys())

    if location not in valid_locations:
        return errors_dict['SustainableLocationNotInList']

    return None


def control_module_watts(form_data):
    """
    """
    # TODO : create a function with not set and not valid error
    errors_dict = get_errors()

    if not key_in_dict_not_empty('watts', form_data):
        return errors_dict['SustainableWattsNotSet']

    watts = format_module_watts(form_data)

    if watts is None:
        return errors_dict['SustainableWattsNotValid']

    if watts <= 0:
        return errors_dict['SustainableWattsNotPositive']

    return None


def control_module(form_data, create=False, obj=None):
    """
    """
    errors = dict()

    errors['time'] = control_module_time(form_data)
    errors['location'] = control_module_location(form_data)
    errors['watts'] = control_module_watts(form_data)

    errors = clean_errors(errors)

    return errors


def format_module(form_data, create=False, obj=None):
    """
    """
    data = dict()

    data['time'] = format_module_time(form_data)
    data['location'] = format_module_location(form_data)
    data['watts'] = format_module_watts(form_data)

    return data

# LOAD MODULE FUNCTIONS


def compute_co2_estimation(project):
    """
    """
    module = select_from_db(ModuleSustainable, 'project_id', project.id)
    update_in_db(module, {'status': 'loading'})
    print('===================')

    if is_empty(module.time) | is_empty(module.location) | is_empty(module.watts):
        update_in_db(module, {'status': 'failed'})
        return

    print('===================')

    co2_emited = sustainable.estimate_co2(
        hours=module.time, location=module.location, watts=module.watts)

    data = {'status': 'loaded', 'result': co2_emited}

    print(data)

    try:
        res = update_in_db(module, data)

        if res != 'updated':
            update_in_db(module, {'status': 'failed'})

    except:
        update_in_db(module, {'status': 'failed'})
