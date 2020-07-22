from flask import session

from ...models import Project
from ...utils.db import select_from_db
from ...utils.session import check_if_session_var_exists


def get_all_projects():
    """
    """
    projects = Project.query.all()

    return projects


def get_header_attributes():
    """
    """
    header_attr = {}

    header_attr['projects'] = get_all_projects()

    check_if_session_var_exists('errors')
    check_if_session_var_exists('success')

    return header_attr
