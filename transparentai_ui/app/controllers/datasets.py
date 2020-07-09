from flask import request, redirect, url_for, render_template, session, jsonify
import os.path
import pandas as pd

from ..models import Dataset
from .services.datasets import format_dataset, control_dataset, load_dataset_modules_in_background
from .controller_class import Controller

from ..utils import add_in_db, exists_in_db


def create_test_dataset():
    """
    """
    test = {
        'name': 'Adult',
        'path': '/home/lauga/Documents/workspace/transparentai-ui/tmp/test_comma_point.csv',
        'target': 'income',
        'score': 'score',
        'model_type': 'binary-classification',
        'protected_attr': ['gender', 'race'],
        'model_columns': ['age', 'fnlwgt', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']
    }
    data = Dataset(
        **test
    )
    add_in_db(data)


dataset_controller = Controller(component=Dataset,
                                format_fn=format_dataset,
                                control_fn=control_dataset,
                                module_fn=load_dataset_modules_in_background)


def index():
    create_test_dataset()
    datasets = dataset_controller.index()
    return render_template("components/datasets/index.html", session=session, instances=datasets)


def get_all_instances_json():
    datasets = dataset_controller.index()
    datasets = [elem.to_dict() for elem in datasets]
    return jsonify(datasets)


def get_instance(name):
    dataset = dataset_controller.get_instance(name)
    if dataset is None:
        return redirect(url_for('datasets.index'))
    return render_template("components/datasets/instance.html", session=session, instance=dataset)


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
    return redirect(url_for('datasets.index'))


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
