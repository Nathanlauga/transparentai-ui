from flask import request
import os.path
import pandas as pd

from ..models import Dataset
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
        'protected_attr': ['gender', 'race']
    }
    data = Dataset(
        name=test['name'],
        path=test['path'],
        target=test['target'],
        score=test['score'],
        protected_attr=test['protected_attr']
    )
    add_in_db(data)


dataset_controller = Controller(name='dataset')


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
