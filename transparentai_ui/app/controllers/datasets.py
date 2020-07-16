from flask import request, redirect, url_for, render_template, session, jsonify
from flask_babel import _
import os.path
import pandas as pd

from ..models import Dataset
from .services.datasets import format_dataset, control_dataset, load_dataset_modules_in_background
from .services.commons import get_header_attributes
from .controller_class import Controller

from ..utils import add_in_db, exists_in_db

dataset_controller = Controller(component=Dataset,
                                format_fn=format_dataset,
                                control_fn=control_dataset,
                                module_fn=load_dataset_modules_in_background)


def index():
    title = _('Datasets')
    header = get_header_attributes()
    datasets = dataset_controller.index()

    return render_template("datasets/index.html", session=session, datasets=datasets, header=header)


def get_all_instances_json():
    datasets = dataset_controller.index()
    datasets = [elem.to_dict() for elem in datasets]
    return jsonify(datasets)


def new():
    title = _('Create a new dataset')
    header = get_header_attributes()
    previous = request.form

    if request.method == 'POST':
        dataset = dataset_controller.create()
        if dataset is not None:
            return redirect(url_for('datasets.get_instance', name=dataset.name))

    return render_template("datasets/new.html", title=title, session=session, header=header, previous=previous)


def new_from_project(project_name):
    title = _('Create a new dataset')
    header = get_header_attributes()
    header['current_project'] = project_name
    previous = request.form

    if request.method == 'POST':
        dataset = dataset_controller.create()
        if dataset is not None:
            return redirect(url_for('datasets.get_instance', name=dataset.name))

    return render_template("projects/new-dataset.html", title=title, session=session, header=header, previous=previous, project_name=project_name)


def edit(name):
    title = _('Edit ') + name
    header = get_header_attributes()
    previous = None

    dataset = dataset_controller.get_instance(name)
    if dataset is not None:
        previous = dataset.to_dict()

    if request.method == 'POST':
        previous = request.form
        dataset = dataset_controller.update(name)
        if dataset is not None:
            return redirect(url_for('datasets.get_instance', name=dataset.name))

    return render_template("datasets/edit.html", title=title, session=session, header=header, previous=previous, dataset=dataset)


def get_instance(name):
    dataset = dataset_controller.get_instance(name)
    if dataset is None:
        return redirect(url_for('datasets.index'))

    title = name
    header = get_header_attributes()
    if dataset.project is not None:
        header['current_project'] = dataset.project.name

    return render_template("datasets/instance.html", session=session, dataset=dataset, header=header, title=title)


def get_instance_json(name):
    dataset = dataset_controller.get_instance(name)
    return jsonify(dataset.to_dict())


def create():
    dataset_controller.create()
    return redirect(url_for('datasets.index'))


def update(name):
    dataset_controller.update(name)
    return redirect(url_for('datasets.get_instance', name=name))


def delete(name):
    dataset_controller.delete(name)
    return redirect(url_for('index'))


def post_instance(name):
    form_data = request.form
    if '_method' not in form_data:
        return redirect(url_for('datasets.get_instance', name=name))

    method = form_data['_method']

    if method == 'POST':
        return create()
    elif method == 'PUT':
        return update(name)
    elif method == 'DELETE':
        return delete(name)

    return redirect(url_for('datasets.get_instance', name=name))
