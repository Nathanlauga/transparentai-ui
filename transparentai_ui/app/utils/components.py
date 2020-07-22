from ..utils.db import select_from_db, add_in_db, update_in_db
from ..models import Dataset


def format_str_strip(form_data, key):
    """
    """
    if key not in form_data:
        return ''

    return form_data[key].strip()


def format_bool(form_data, key):
    """
    """
    if key not in form_data:
        return None

    try:
        res = bool(int(form_data[key]))
    except:
        return None

    return res


def format_int(form_data, key):
    """
    """
    if key not in form_data:
        return None

    try:
        res = int(form_data[key])
    except:
        return None

    return res


def clean_errors(errors):
    """
    """
    new_errors = dict()
    for k, v in errors.items():
        if v is not None:
            new_errors[k] = v
    return new_errors


def update_dataset_module_db(ModuleModel, dataset, status='init'):
    """
    """
    module = select_from_db(ModuleModel,
                            'dataset_id', dataset.id)
    update_in_db(module, {'status': 'loading'})


def init_model_module_db(ModuleModel, model):
    """
    """
    module = ModuleModel(
        model_id=model.id,
        model=model,
        status='init'
    )
    add_in_db(module)
