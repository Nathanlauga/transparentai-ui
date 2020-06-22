from flask import current_app as app

__all__ = [
    'index',
    'errors',
    'dev',
    'components'
]

# Error handling
from .errors.error_404 import not_found

# Routes
from .index import index
from .components import datasets


app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])

# Datasets
app.add_url_rule('/datasets', endpoint='datasets.index',
                 view_func=datasets.index, methods=['GET'])
app.add_url_rule('/datasets', endpoint='datasets.create',
                 view_func=datasets.create, methods=['POST'])
app.add_url_rule('/datasets', endpoint='datasets.update',
                 view_func=datasets.update, methods=['PUT'])
app.add_url_rule('/datasets', endpoint='datasets.delete',
                 view_func=datasets.delete, methods=['DELETE'])
