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
from .components import models


app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])

# Datasets
app.add_url_rule('/datasets', endpoint='datasets.index',
                 view_func=datasets.index, methods=['GET'])
app.add_url_rule('/datasets', endpoint='datasets.create',
                 view_func=datasets.create, methods=['POST'])
app.add_url_rule('/datasets/<name>', endpoint='datasets.get_instance',
                 view_func=datasets.get_instance, methods=['GET'])
app.add_url_rule('/datasets/<name>', endpoint='datasets.post_instance',
                 view_func=datasets.post_instance, methods=['POST'])
app.add_url_rule('/datasets/<name>', endpoint='datasets.update',
                 view_func=datasets.update, methods=['PUT'])
app.add_url_rule('/datasets/<name>', endpoint='datasets.delete',
                 view_func=datasets.delete, methods=['DELETE'])

# Models
app.add_url_rule('/models', endpoint='models.index',
                 view_func=models.index, methods=['GET'])
app.add_url_rule('/models', endpoint='models.create',
                 view_func=models.create, methods=['POST'])
app.add_url_rule('/models/<name>', endpoint='models.get_instance',
                 view_func=models.get_instance, methods=['GET'])
app.add_url_rule('/models/<name>', endpoint='models.post_instance',
                 view_func=models.post_instance, methods=['POST'])
app.add_url_rule('/models/<name>', endpoint='models.update',
                 view_func=models.update, methods=['PUT'])
app.add_url_rule('/models/<name>', endpoint='models.delete',
                 view_func=models.delete, methods=['DELETE'])
