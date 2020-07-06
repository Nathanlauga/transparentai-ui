from flask import request
import os.path
import pandas as pd

from ..models import Project
from .services.projects import format_project, control_project
from .controller_class import Controller

from ..utils import add_in_db, exists_in_db

project_controller = Controller(name='project',
                                component=Project,
                                route='projects',
                                format_fn=format_project,
                                control_fn=control_project,
                                module_fn=None)


def index():
    return project_controller.index()


def create():
    return project_controller.create()


def get_instance(name):
    return project_controller.get_instance(name)


def post_instance(name):
    return project_controller.post_instance(name)


def update(name):
    return project_controller.update(name)


def delete(name):
    return project_controller.delete()
