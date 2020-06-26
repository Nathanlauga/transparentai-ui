from ...models.components.models import Model
from .base_controller import BaseController

from ...utils import add_in_db

def create_test_model():
    """
    """
    test = {
        'name': 'Adult',
        'path': '/home/lauga/Documents/workspace/transparentai-ui/tmp/',
        'file_type':'pkl'
    }
    data = Model(
        name=test['name'],
        path=test['path'],
        file_type=test['file_type']
    )
    add_in_db(data)


model_controller = BaseController(
    name='models',
    model=Model,
    id_col='name',
    columns=['path', 'file_type']
)

def index():
    create_test_model()
    return model_controller.index()

def create():
    # ID CHECK : Check if name is already used

    # Other attr CHECK
    # Valid file type
    # Try to read model file  

    return model_controller.create()

def get_instance(name):
    return model_controller.get_instance(name)

def post_instance(name):
    return model_controller.post_instance(name)

def update(name):
    # Other attr CHECK
    # Valid file type
    # Try to read model file  
    return model_controller.update()

def delete(name):
    return model_controller.delete()

