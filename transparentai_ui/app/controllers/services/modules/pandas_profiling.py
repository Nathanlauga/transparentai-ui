from pandas_profiling import ProfileReport
from os.path import dirname, abspath

from ....utils.db import update_in_db, select_from_db
from ....utils.errors import get_errors
from ....utils import key_in_dict_not_empty
from ....utils.components import clean_errors, format_bool, format_int

from ....models import Dataset
from ....models.modules import ModulePandasProfiling


# ======= FORMAT MODULE FUNCTIONS ======= #

def format_module_minimal(form_data):
    """
    """
    return format_bool(form_data, key='minimal')


# def format_module_explorative(form_data):
#     """
#     """
#     return format_bool(form_data, key='explorative')


def format_module_nrows(form_data):
    """
    """
    return format_int(form_data, key='nrows')


# ======= CONTROL MODULE FUNCTIONS ======= #


def control_module_minimal(form_data):
    """
    """
    errors_dict = get_errors()

    if not key_in_dict_not_empty('minimal', form_data):
        return errors_dict['PandasProfMinimalNotSet']

    minimal = format_module_minimal(form_data)

    if minimal is None:
        return errors_dict['PandasProfMinimalNotValid']

    return None


# def control_module_explorative(form_data):
#     """
#     """
#     errors_dict = get_errors()

#     if not key_in_dict_not_empty('explorative', form_data):
#         return errors_dict['PandasProfExplorativeNotSet']

#     explorative = format_module_explorative(form_data)

#     if explorative is None:
#         return errors_dict['PandasProfExplorativeNotValid']

#     return None


def control_module_nrows(form_data, max_nrows=None):
    """
    """
    errors_dict = get_errors()

    if not key_in_dict_not_empty('nrows', form_data):
        return None

    nrows = format_module_nrows(form_data)

    if nrows is None:
        return errors_dict['PandasProfNrowsNotValid']

    if max_nrows is not None:
        if nrows > max_nrows:
            return errors_dict['PandasProfNrowsOverLimit']

    return None


def control_module(form_data, create=False, obj=None):
    """
    """
    errors = dict()

    errors['minimal'] = control_module_minimal(form_data)
    # errors['explorative'] = control_module_explorative(form_data)
    errors['nrows'] = control_module_nrows(
        form_data, max_nrows=obj.dataset.length)

    errors = clean_errors(errors)

    return errors


def format_module(form_data, create=False, obj=None):
    """
    """
    data = dict()

    data['minimal'] = format_module_minimal(form_data)
    # data['explorative'] = format_module_explorative(form_data)
    data['nrows'] = format_module_nrows(form_data)

    return data

# LOAD MODULE FUNCTIONS


def get_save_path():
    """
    """
    return dirname(dirname(dirname(dirname(abspath(__file__))))) + \
        '/views/modules/pandas_profiling_reports/'


def generate_pandas_prof_report(df, title, explorative=True, dataset=None, minimal=True):
    """
    """
    if dataset is not None:
        module = select_from_db(ModulePandasProfiling,
                                'dataset_id', dataset.id)
        update_in_db(module, {'status': 'loading'})

    try:
        profile = ProfileReport(
            df, title=title, minimal=minimal, explorative=True)

        output_path = get_save_path()
        output_path = output_path + title + '.html'

        profile.to_file(output_path)

        if dataset is not None:
            data = {'status': 'loaded', 'path': output_path}
            res = update_in_db(module, data)

            if res != 'updated':
                update_in_db(module, {'status': 'failed'})

    except:
        if dataset is not None:
            update_in_db(module, {'status': 'failed'})

