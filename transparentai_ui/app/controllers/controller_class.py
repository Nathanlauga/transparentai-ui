from flask import render_template, request, redirect, url_for, session
from flask_babel import _

from ..utils import set_session_var, check_if_session_var_exists
from ..utils.db import add_in_db, update_in_db, delete_in_db, select_from_db

from .services.datasets import format_dataset, control_dataset, load_dataset_modules_in_background
from .services.models import format_model, control_model, load_model_modules_in_background

from ..models import Dataset
from ..models import Model


def get_only_updated_values(instance, data):
    """
    """
    new_data = dict()

    for key, value in data.items():
        current_value = instance.__getattribute__(key)
        if value != current_value:
            new_data[key] = value

    return new_data


class Controller():
    """
    """

    def __init__(self, name):
        """
        """
        self.controller_name = name
        self.module_fn = None

        if name == 'dataset':
            self.Component = Dataset
            self.route = 'datasets'
            self.format_fn = format_dataset
            self.control_fn = control_dataset
            self.module_fn = load_dataset_modules_in_background
        elif name == 'model':
            self.Component = Model
            self.route = 'models'
            self.format_fn = format_model
            self.control_fn = control_model
            self.module_fn = load_model_modules_in_background

    def format_and_control(self, form_data, create=False):
        """
        """
        errors = self.control_fn(form_data, create)

        if len(errors) > 0:
            return errors, None

        data = self.format_fn(form_data, create)

        return errors, data

    def get_one_instance(self, col, value):
        """
        """
        return select_from_db(self.Component, col, value)

    def get_all_instances(self):
        """
        """
        all_instances = self.Component.query.all()

        return all_instances

    def index(self):
        """Get the datasets
        """
        all_instances = self.get_all_instances()

        check_if_session_var_exists('errors')
        check_if_session_var_exists('success')

        args = {
            'session': session,
            'instances': all_instances
        }

        return render_template("components/%s/index.html" % self.route, **args)

    def create(self):
        """Create a dataset based on POST args
        """
        errors, data = self.format_and_control(request.form, create=True)

        if len(errors) > 0:
            set_session_var('errors', str(errors))
            return redirect(url_for('%s.index' % self.route))

        # Create object
        instance = self.Component(**data)

        # Add object in database
        res = add_in_db(instance)

        if res != 'added':
            set_session_var('errors', str(res))
        else:
            set_session_var('success', res)

        if self.module_fn is not None:
            self.module_fn(instance, data)

        return redirect(url_for('%s.index' % self.route))

    def get_instance(self, name):
        """
        """
        instance = self.get_one_instance('name', name)

        if type(instance) != self.Component:
            set_session_var('errors', str(instance))
            return redirect(url_for('%s.index' % self.route))

        check_if_session_var_exists('errors')
        check_if_session_var_exists('success')

        args = {
            'session': session,
            'instance': instance
        }

        return render_template("components/%s/instance.html" % self.route, **args)

    def post_instance(self, name):
        """
        """
        form_data = request.form
        if '_method' not in form_data:
            return redirect(url_for('%s.get_instance' % self.route))

        method = form_data['_method']

        if method == 'PUT':
            return self.update(name)
        elif method == 'DELETE':
            return self.delete(name)
        else:
            return redirect(url_for('%s.get_instance' % self.route, name=name))

    def update(self, name):
        """Update a dataset based on PUT args
        """
        instance = self.get_one_instance('name', name)

        if type(instance) != self.Component:
            set_session_var('errors', str(instance))
            return redirect(url_for('%s.index' % self.route))

        errors, data = self.format_and_control(request.form)

        if len(errors) > 0:
            set_session_var('errors', str(errors))
            return redirect(url_for('%s.get_instance' % self.route, name=name))

        data = get_only_updated_values(instance, data)

        if len(data) == 0:
            return redirect(url_for('%s.get_instance' % self.route, name=name))

        res = update_in_db(instance, data)

        if res != 'updated':
            set_session_var('errors', str(res))
        else:
            set_session_var('success', res)

        if self.module_fn is not None:
            self.module_fn(instance, data)

        return redirect(url_for('%s.get_instance' % self.route, name=name))

    def delete(self, name):
        """Drop a dataset based on DELETE args
        """
        instance = self.get_one_instance('name', name)

        if type(instance) != self.Component:
            set_session_var('errors', str(instance))
            return redirect(url_for('%s.index' % self.route))

        res = delete_in_db(instance)

        if res != 'deleted':
            set_session_var('errors', str(res))
        else:
            set_session_var('success', res)

        return redirect(url_for('%s.index' % self.route))
