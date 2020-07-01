
from .. import db
from .errors import get_errors


def select_from_db(Model, col, value):
    """
    """
    kwargs = {col: value}
    try:
        instance = Model.query.filter_by(**kwargs).first()
    except Exception as exception:
        return exception

    return instance


def add_in_db(obj):
    """
    """
    errors_dict = get_errors()

    try:
        db.session.add(obj)
        db.session.commit()
    except:
        db.session.rollback()
        return errors_dict['AddInDB']
    return 'added'


def delete_in_db(obj):
    """
    """
    errors_dict = get_errors()

    try:
        db.session.delete(obj)
        db.session.commit()
    except:
        db.session.rollback()
        return errors_dict['DeleteInDB']
    return 'deleted'


def update_in_db(obj, args):
    """
    """
    errors_dict = get_errors()

    try:
        for key, value in args.items():
            setattr(obj, key, value)
        db.session.commit()
    except:
        db.session.rollback()
        return errors_dict['UpdateInDB']
    return 'updated'


def exists_in_db(key, value):
    """
    """
    return db.session.query(db.exists().where(key == value)).scalar()


def init_component_module(ModuleModel, component):  # , module_attr):
    """
    """
    module = ModuleModel(
        dataset_id=component.id,
        dataset=component,
        status='loading'
    )
    add_in_db(module)

    # data = {module_attr:module}
    # update_in_db(component, data)
