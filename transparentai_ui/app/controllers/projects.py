from flask import request, render_template, redirect, url_for, session, jsonify
import os.path
import pandas as pd

from ..models import Project
from .services.projects import format_project, control_project
from .controller_class import Controller

from ..utils import add_in_db, exists_in_db

project_controller = Controller(component=Project,
                                format_fn=format_project,
                                control_fn=control_project,
                                module_fn=None)


def index():
    projects = project_controller.index()
    return render_template("components/projects/index.html", session=session, instances=projects)


def get_all_instances_json():
    projects = project_controller.index()
    projects = [elem.to_dict() for elem in projects]
    return jsonify(projects)


def get_instance(name):
    project = project_controller.get_instance(name)
    if project is None:
        return redirect(url_for('projects.index'))
    return render_template("components/projects/instance.html", session=session, instance=project)


def get_instance_json(name):
    project = project_controller.get_instance(name)
    return jsonify(project.to_dict())


def create():
    project_controller.create()
    return redirect(url_for('projects.index'))


def update(name):
    project_controller.update(name)
    return redirect(url_for('projects.get_instance', name=name))


def delete(name):
    project_controller.delete(name)
    return redirect(url_for('projects.index'))


def post_instance(name):
    form_data = request.form
    if '_method' not in form_data:
        return redirect(url_for('projects.get_instance', name=name))

    method = form_data['_method']

    if method == 'POST':
        return create()
    elif method == 'PUT':
        return update(name)
    elif method == 'DELETE':
        return delete(name)
    
    return redirect(url_for('projects.get_instance', name=name))
