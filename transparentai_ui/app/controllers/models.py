from flask import request

from ..models import Model
from .services.models import format_model, control_model, load_model_modules_in_background
from .controller_class import Controller

from ..utils.db import add_in_db


def create_test_model():
    """
    """
    test = {
        'name': 'Adult',
        'path': '/home/lauga/Documents/workspace/transparentai-ui/tmp/clf.pkl',
        'file_type': 'pickle'
    }
    data = Model(
        name=test['name'],
        path=test['path'],
        file_type=test['file_type']
    )
    add_in_db(data)


model_controller = Controller(name='model',
                              component=Model,
                              route='models',
                              format_fn=format_model,
                              control_fn=control_model,
                              module_fn=load_model_modules_in_background)


def index():
    create_test_model()
    return model_controller.index()


def create():
    return model_controller.create()


def get_instance(name):
    return model_controller.get_instance(name)


def post_instance(name):
    return model_controller.post_instance(name)


def update(name):
    return model_controller.update(name)


def delete(name):
    return model_controller.delete()
