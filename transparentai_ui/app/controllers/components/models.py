from flask import request

from ...models.components.models import Model
from .base_controller import BaseController

from ...utils import add_in_db
from ...utils import get_component_args


def create_test_model():
    """
    """
    test = {
        'name': 'Adult',
        'path': '/home/lauga/Documents/workspace/transparentai-ui/tmp/',
        'file_type': 'pkl'
    }
    data = Model(
        name=test['name'],
        path=test['path'],
        file_type=test['file_type']
    )
    add_in_db(data)


model_controller = BaseController(
    name='models',
    model=Model

)

def get_model_form_data(form_data):
    """
    """
    columns = ['name', 'path', 'file_type']
    data = get_component_args(form_data, columns)

    return data


def index():
    create_test_model()
    return model_controller.index()


def create():
    # ID CHECK : Check if name is already used

    # Other attr CHECK
    # Valid file type
    # Try to read model file
    data = get_model_form_data(request.form)

    return model_controller.create(data)


def get_instance(name):
    return model_controller.get_instance(name)


def post_instance(name):
    data = get_model_form_data(request.form)
    data['name'] = name

    return model_controller.post_instance(name, data)


def update(name):
    # Other attr CHECK
    # Valid file type
    # Try to read model file
    data = get_model_form_data(request.form)
    data['name'] = name

    return model_controller.update(name, data)


def delete(name):
    return model_controller.delete()
