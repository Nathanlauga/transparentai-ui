from ..utils.db import select_from_db, add_in_db
from ..models import Dataset


def format_str_strip(form_data, key):
    """
    """
    if key not in form_data:
        return ''

    return form_data[key].strip()


def clean_errors(errors):
    """
    """
    new_errors = dict()
    for k, v in errors.items():
        if v is not None:
            new_errors[k] = v
    return new_errors

def init_dataset_module_db(ModuleModel, dataset):
    """
    """
    module = ModuleModel(
        dataset_id=dataset.id,
        dataset=dataset,
        status='init'
    )
    add_in_db(module)


def init_model_module_db(ModuleModel, model):
    """
    """
    module = ModuleModel(
        model_id=model.id,
        model=model,
        status='init'
    )
    add_in_db(module)
