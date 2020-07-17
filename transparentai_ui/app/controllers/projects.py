from flask import request, render_template, redirect, url_for, session, jsonify
from flask_babel import _
import os.path
import pandas as pd

from ..models import Project
from .services.projects import format_project, control_project
from .services.commons import get_header_attributes
from .controller_class import Controller

from ..utils import add_in_db, exists_in_db
from ..src import get_questions

project_controller = Controller(component=Project,
                                format_fn=format_project,
                                control_fn=control_project,
                                module_fn=None)


def index():
    title = _('Projects')
    header = get_header_attributes()
    projects = project_controller.index()

    return render_template("projects/index.html", title=title, session=session, projects=projects, header=header)


def get_all_instances_json():
    projects = project_controller.index()
    projects = [elem.to_dict() for elem in projects]
    return jsonify(projects)


def new():
    title = _('Create a new project')
    header = get_header_attributes()
    previous = request.form

    if request.method == 'POST':
        project = project_controller.create()
        if project is not None:
            return redirect(url_for('projects.get_instance', name=project.name))

    return render_template("projects/new.html", title=title, session=session, header=header, previous=previous)


def edit(name):
    title = _('Edit ') + name
    header = get_header_attributes()

    project = project_controller.get_instance(name)
    previous = project.to_dict()

    # Temporary until handle list in form
    previous['members'] = ', '.join(previous['members'])

    if request.method == 'POST':
        previous = request.form
        project = project_controller.update(name)
        if project is not None:
            return redirect(url_for('projects.get_instance', name=project.name))

    return render_template("projects/edit.html", title=title, session=session, header=header, previous=previous, project=project)


def get_instance(name):
    project = project_controller.get_instance(name)
    if project is None:
        return redirect(url_for('projects.index'))

    title = name
    header = get_header_attributes()
    header['current_project'] = name

    questions = get_questions()

    return render_template("projects/instance.html", session=session, project=project, header=header, title=title, questions=questions)


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
