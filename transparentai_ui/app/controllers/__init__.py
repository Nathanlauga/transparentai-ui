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

# Temporary route for development
app.add_url_rule('/temp', view_func=temp, methods=['GET', 'POST'])


# /projects routes
app.add_url_rule('/projects', endpoint='projects.index',
                 view_func=projects.index, methods=['GET'])
app.add_url_rule('/projects/', endpoint='projects.index.bis',
                 view_func=projects.index, methods=['GET'])
app.add_url_rule('/new-project', endpoint='projects.new',
                 view_func=projects.new, methods=['GET', 'POST'])
app.add_url_rule('/edit-project/<name>', endpoint='projects.edit',
                 view_func=projects.edit, methods=['GET', 'POST'])
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


app.add_url_rule('/projects/<project_name>/new-dataset', endpoint='projects.dataset.new',
                 view_func=datasets.new_from_project, methods=['GET', 'POST'])
app.add_url_rule('/projects/<project_name>/new-model', endpoint='projects.model.new',
                 view_func=models.new_from_project, methods=['GET', 'POST'])
app.add_url_rule('/projects/<name>/estimate-co2', endpoint='projects.estimate_co2',
                 view_func=projects.estimate_co2, methods=['GET', 'POST'])


app.add_url_rule('/projects/<name>/analyse-performance', endpoint='projects.analyse_performance',
                 view_func=datasets.analyse_performance, methods=['GET', 'POST'])
app.add_url_rule('/projects/<name>/analyse-dataset', endpoint='projects.analyse_dataset',
                 view_func=datasets.analyse_dataset, methods=['GET', 'POST'])
app.add_url_rule('/projects/<name>/analyse-bias', endpoint='projects.analyse_bias',
                 view_func=datasets.analyse_bias, methods=['GET','POST'])
app.add_url_rule('/projects/<name>/bias-results', endpoint='projects.bias_results',
                 view_func=datasets.bias_results, methods=['GET', 'POST'])


# API
# app.add_url_rule('/api/projects', endpoint='api.projects',
#                  view_func=projects.get_all_instances_json, methods=['GET'])
# app.add_url_rule('/api/projects/<name>', endpoint='api.projects.get_instance',
#                  view_func=projects.get_instance_json, methods=['GET'])

# Datasets
app.add_url_rule('/datasets', endpoint='datasets.index',
                 view_func=datasets.index, methods=['GET'])
app.add_url_rule('/datasets/', endpoint='datasets.index.bis',
                 view_func=datasets.index, methods=['GET'])
app.add_url_rule('/new-dataset', endpoint='datasets.new',
                 view_func=datasets.new, methods=['GET', 'POST'])
app.add_url_rule('/edit-dataset/<name>', endpoint='datasets.edit',
                 view_func=datasets.edit, methods=['GET', 'POST'])
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

# Datasets Modules
app.add_url_rule('/datasets/<name>/analyse-dataset', endpoint='datasets.analyse_dataset',
                 view_func=datasets.analyse_dataset, methods=['GET', 'POST'])
app.add_url_rule(
    '/show-report', view_func=datasets.show_report, methods=['GET'])
app.add_url_rule('/datasets/<name>/analyse-performance', endpoint='datasets.analyse_performance',
                 view_func=datasets.analyse_performance, methods=['GET', 'POST'])


app.add_url_rule('/datasets/<name>/bias-results', endpoint='datasets.bias_results',
                 view_func=datasets.bias_results, methods=['GET', 'POST'])
app.add_url_rule('/datasets/<name>/analyse-bias', endpoint='datasets.analyse_bias',
                 view_func=datasets.analyse_bias, methods=['GET','POST'])

# API
# app.add_url_rule('/api/datasets', endpoint='api.datasets',
#                  view_func=datasets.get_all_instances_json, methods=['GET'])
# app.add_url_rule('/api/datasets/<name>', endpoint='api.datasets.get_instance',
#                  view_func=datasets.get_instance_json, methods=['GET'])

# Models
app.add_url_rule('/models', endpoint='models.index',
                 view_func=models.index, methods=['GET'])
app.add_url_rule('/models/', endpoint='models.index.bis',
                 view_func=models.index, methods=['GET'])
app.add_url_rule('/new-model', endpoint='models.new',
                 view_func=models.new, methods=['GET', 'POST'])
app.add_url_rule('/edit-model/<name>', endpoint='models.edit',
                 view_func=models.edit, methods=['GET', 'POST'])
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


app.add_url_rule('/models/<name>/explain-global', endpoint='models.explain_global',
                 view_func=models.explain_global, methods=['GET', 'POST'])
app.add_url_rule('/models/<name>/explain-local', endpoint='models.explain_local',
                 view_func=models.explain_local, methods=['GET', 'POST'])

# API
# app.add_url_rule('/api/models', endpoint='api.models',
#                  view_func=models.get_all_instances_json, methods=['GET'])
# app.add_url_rule('/api/models/<name>', endpoint='api.models.get_instance',
#                  view_func=models.get_instance_json, methods=['GET'])
