
from .. import db
from .errors import get_errors

from .. import db_session


def select_from_db(Model, col, value):
    """
    """
    kwargs = {col: value}
    try:
        instance = Model.query.filter_by(**kwargs).first()

    except Exception as exception:
        db.session.rollback()
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
        # obj.update(args)

        # db.session.commit()

    except Exception as exception:
        db.session.rollback()
        print(exception)
        
        return exception #errors_dict['UpdateInDB']

    return 'updated'


def exists_in_db(key, value):
    """
    """
    return db.session.query(db.exists().where(key == value)).scalar()
