from flask import request, render_template, redirect, url_for, session, jsonify

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


model_controller = Controller(component=Model,
                              format_fn=format_model,
                              control_fn=control_model,
                              module_fn=load_model_modules_in_background)


def index():
    create_test_model()
    models = model_controller.index()
    return render_template("components/models/index.html", session=session, instances=models)


def get_all_instances_json():
    models = model_controller.index()
    models = [elem.to_dict() for elem in models]
    return jsonify(models)


def get_instance(name):
    model = model_controller.get_instance(name)
    if model is None:
        return redirect(url_for('models.index'))
    return render_template("components/models/instance.html", session=session, instance=model)


def get_instance_json(name):
    model = model_controller.get_instance(name)
    return jsonify(model.to_dict())


def create():
    model_controller.create()
    return redirect(url_for('models.index'))


def update(name):
    model_controller.update(name)
    return redirect(url_for('models.get_instance', name=name))


def delete(name):
    model_controller.delete(name)
    return redirect(url_for('models.index'))


def post_instance(name):
    form_data = request.form
    if '_method' not in form_data:
        return redirect(url_for('models.get_instance', name=name))

    method = form_data['_method']

    if method == 'POST':
        return create()
    elif method == 'PUT':
        return update(name)
    elif method == 'DELETE':
        return delete(name)
    
    return redirect(url_for('models.get_instance', name=name))
