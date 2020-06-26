
from .. import db
from .errors import get_errors

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