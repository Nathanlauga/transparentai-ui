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


def format_dtype(form_data, key, dtype):
    """
    """
    if key not in form_data:
        return None

    try:
        res = dtype(form_data[key])
    except:
        return None

    return res


def format_int(form_data, key):
    """
    """
    return format_dtype(form_data, key, int)


def format_float(form_data, key):
    """
    """
    return format_dtype(form_data, key, float)

def format_str(form_data, key):
    """
    """
    return format_dtype(form_data, key, str)


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
    res = update_in_db(module, {'status': 'loading'})


def init_dataset_module_db(ModuleDataset, dataset):
    """
    """
    module = ModuleDataset(
        dataset_id=dataset.id,
        dataset=dataset,
        status='init'
    )
    add_in_db(module)

def init_project_module_db(ModuleProject, project):
    """
    """
    module = ModuleProject(
        project_id=project.id,
        project=project,
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
