from flask import request, render_template, redirect, url_for, session, jsonify
from flask_babel import _

from ..models import Model, Project
from .services.models import format_model, control_model, load_model_modules_in_background
from .services.commons import get_header_attributes
from .controller_class import Controller

from ..utils.db import add_in_db, select_from_db

model_controller = Controller(component=Model,
                              format_fn=format_model,
                              control_fn=control_model,
                              module_fn=load_model_modules_in_background)


def index():
    title = _('Models')
    header = get_header_attributes()
    models = model_controller.index()
    return render_template("models/index.html", session=session, models=models, header=header)


def get_all_instances_json():
    models = model_controller.index()
    models = [elem.to_dict() for elem in models]
    return jsonify(models)


def new():
    title = _('Create a new model')
    header = get_header_attributes()
    previous = request.form

    if request.method == 'POST':
        model = model_controller.create()
        if model is not None:
            return redirect(url_for('models.get_instance', name=model.name))

    return render_template("models/new.html", title=title, session=session, header=header, previous=previous)


def new_from_project(project_name):
    title = _('Create a new model')
    header = get_header_attributes()
    header['current_project'] = project_name
    previous = request.form
    dataset_name = None

    project = select_from_db(Project, 'name', project_name)
    if project.dataset is not None: 
        dataset_name = project.dataset.name

    if request.method == 'POST':
        model = model_controller.create()
        if model is not None:
            return redirect(url_for('projects.get_instance', name=project_name))

    return render_template("projects/new-model.html", title=title, session=session, header=header, previous=previous, dataset_name=dataset_name, project_name=project_name)


def edit(name):
    title = _('Edit ') + name
    header = get_header_attributes()
    previous = None

    model = model_controller.get_instance(name)
    if model is not None:
        previous = model.to_dict()

    if request.method == 'POST':
        previous = request.form
        model = model_controller.update(name)
        if model is not None:
            return redirect(url_for('models.get_instance', name=model.name))

    return render_template("models/edit.html", title=title, session=session, header=header, previous=previous, model=model)


def get_instance(name):
    model = model_controller.get_instance(name)
    if model is None:
        return redirect(url_for('models.index'))

    title = name
    header = get_header_attributes()
    if model.dataset is not None:
        if model.dataset.project is not None:
            header['current_project'] = model.dataset.project.name

    return render_template("models/instance.html", session=session, model=model, header=header, title=title)


def get_instance_json(name):
    model = model_controller.get_instance(name)
    return jsonify(model.to_dict())


def create():
    model_controller.create()
    return redirect(url_for('models.index'))


def update(name):
    model_controller.update(name)
    return redirect(url_for('models.get_instance', name=name))


def delete(name):
    model = model_controller.get_instance(name)

    redirect_project = False
    if model.dataset is not None:
        redirect_project = True if model.dataset.project is not None else False

    model_controller.delete(name)

    if redirect_project:
        return redirect(
            url_for('projects.get_instance', name=model.dataset.project.name))

    return redirect(url_for('models.index'))


def post_instance(name):
    form_data = request.form
    if '_method' not in form_data:
        return redirect(url_for('models.get_instance', name=name))

    method = form_data['_method']

    if method == 'POST':
        return create()
    elif method == 'PUT':
        return update(name)
    elif method == 'DELETE':
        return delete(name)

    return redirect(url_for('models.get_instance', name=name))


def explain_global(name):
    model = model_controller.get_instance(name)
    if model is None:
        return redirect(url_for('models.index'))

    title = _('Analyse global behavior: ') + name
    header = get_header_attributes()
    if model.dataset is not None:
        if model.dataset.project is not None:
            header['current_project'] = model.dataset.project.name

    return render_template("modules/explain-global.html", session=session, model=model, header=header, title=title)