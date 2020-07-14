from flask import session

from ...models import Project
from ...utils.db import select_from_db


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

    return header_attr
