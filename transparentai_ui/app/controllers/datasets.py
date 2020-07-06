from flask import request
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


dataset_controller = Controller(name='dataset',
                                component=Dataset,
                                route='datasets',
                                format_fn=format_dataset,
                                control_fn=control_dataset,
                                module_fn=load_dataset_modules_in_background)


def index():
    create_test_dataset()
    return dataset_controller.index()


def create():
    return dataset_controller.create()


def get_instance(name):
    return dataset_controller.get_instance(name)


def post_instance(name):
    return dataset_controller.post_instance(name)


def update(name):
    return dataset_controller.update(name)


def delete(name):
    return dataset_controller.delete()
