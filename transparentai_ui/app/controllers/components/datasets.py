from ...models.components.datasets import Dataset
from .base_controller import BaseController

from ...utils import add_in_db

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


dataset_controller = BaseController(
    name='datasets',
    model=Dataset,
    id_col='name',
    columns=['path', 'target', 'score', 'protected_attr', 'model_columns']
)

def index():
    create_test_dataset()
    return dataset_controller.index()

def create():
    # ID CHECK : Check if name is already used

    # Other attr CHECK
    # Try to read file csv or excel
    # Check column in DataFrame

    return dataset_controller.create()

def get_instance(name):
    return dataset_controller.get_instance(name)

def post_instance(name):
    return dataset_controller.post_instance(name)

def update(name):
    # Other attr CHECK
    # Try to read file csv or excel
    # Check column in DataFrame
    return dataset_controller.update()

def delete(name):
    return dataset_controller.delete()

