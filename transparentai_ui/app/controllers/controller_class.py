from flask import render_template, request, redirect, url_for, session
from flask_babel import _

from ..utils import set_session_var, check_if_session_var_exists
from ..utils.db import add_in_db, update_in_db, delete_in_db, select_from_db

from threading import Thread


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

    def __init__(self, component, format_fn, control_fn, module_fn=None):
        """
        """
        self.Component = component
        self.format_fn = format_fn
        self.control_fn = control_fn
        self.module_fn = module_fn

    def format_and_control(self, form_data, create=False, obj=None):
        """
        """
        errors = self.control_fn(form_data, create, obj=obj)

        if len(errors) > 0:
            return errors, None

        data = self.format_fn(form_data, create, obj=obj)

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

        return all_instances

    def get_instance(self, name):
        """
        """
        instance = self.get_one_instance('name', name)

        if type(instance) != self.Component:
            set_session_var('errors', str(instance))
            return None

        check_if_session_var_exists('errors')
        check_if_session_var_exists('success')

        args = {
            'session': session,
            'instance': instance
        }

        return instance

    def create(self):
        """Create a dataset based on POST args
        """
        errors, data = self.format_and_control(request.form, create=True)

        if len(errors) > 0:
            set_session_var('errors', dict(errors))
            return None

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

        return instance

    def update(self, id, id_col='name'):
        """Update a dataset based on PUT args
        """
        instance = self.get_one_instance(id_col, id)

        if type(instance) != self.Component:
            set_session_var('errors', str(instance))
            return None

        errors, data = self.format_and_control(request.form, obj=instance)

        if len(errors) > 0:
            set_session_var('errors', dict(errors))
            return None

        data = get_only_updated_values(instance, data)

        if len(data) == 0:
            return None

        res = update_in_db(instance, data)

        if res != 'updated':
            set_session_var('errors', str(res))
            return None
        else:
            set_session_var('success', res)

        if self.module_fn is not None:
            self.module_fn(instance, data)

        return instance

    def delete(self, name):
        """Drop a dataset based on DELETE args
        """
        instance = self.get_one_instance('name', name)

        if type(instance) != self.Component:
            set_session_var('errors', str(instance))
            return None

        res = delete_in_db(instance)

        if res != 'deleted':
            set_session_var('errors', str(res))
        else:
            set_session_var('success', res)

        return True
