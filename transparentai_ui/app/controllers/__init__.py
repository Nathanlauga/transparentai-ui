from flask import current_app as app

__all__ = [
    'index',
    'errors'
]

# Error handling
from .errors.error_404 import not_found

# Routes
from .index import index, temp
from . import datasets
from . import models
from . import projects


app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])

app.add_url_rule('/temp', view_func=temp, methods=['GET', 'POST'])


# Projects
app.add_url_rule('/projects', endpoint='projects.index',
                 view_func=projects.index, methods=['GET'])
app.add_url_rule('/projects', endpoint='projects.create',
                 view_func=projects.create, methods=['POST'])
app.add_url_rule('/projects/<name>', endpoint='projects.get_instance',
                 view_func=projects.get_instance, methods=['GET'])
app.add_url_rule('/projects/<name>', endpoint='projects.post_instance',
                 view_func=projects.post_instance, methods=['POST'])
app.add_url_rule('/projects/<name>', endpoint='projects.update',
                 view_func=projects.update, methods=['PUT'])
app.add_url_rule('/projects/<name>', endpoint='projects.delete',
                 view_func=projects.delete, methods=['DELETE'])

# API
app.add_url_rule('/api/projects', endpoint='api.projects',
                 view_func=projects.get_all_instances_json, methods=['GET'])
app.add_url_rule('/api/projects/<name>', endpoint='api.projects.get_instance',
                 view_func=projects.get_instance_json, methods=['GET'])

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
# API
app.add_url_rule('/api/datasets', endpoint='api.datasets',
                 view_func=datasets.get_all_instances_json, methods=['GET'])
app.add_url_rule('/api/datasets/<name>', endpoint='api.datasets.get_instance',
                 view_func=datasets.get_instance_json, methods=['GET'])

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

# API
app.add_url_rule('/api/models', endpoint='api.models',
                 view_func=models.get_all_instances_json, methods=['GET'])
app.add_url_rule('/api/models/<name>', endpoint='api.models.get_instance',
                 view_func=models.get_instance_json, methods=['GET'])
