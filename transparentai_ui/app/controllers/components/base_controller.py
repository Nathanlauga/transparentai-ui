from flask import render_template, request, redirect, url_for, session
from flask_babel import _

from ...utils import set_session_var, check_if_session_var_exists
from ...utils import add_in_db, update_in_db, delete_in_db


class BaseController():
    """
    """

    def __init__(self, name, model):
        """
        """
        self.name = name
        self.Component = model

    def get_one_instance(self, col, value):
        """
        """
        kwargs = {col: value}
        try:
            instance = self.Component.query.filter_by(**kwargs).first()
        except Exception as exception:
            return exception
        return instance

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
            self.name: all_instances
        }

        return render_template("components/%s/index.html" % self.name, **args)

    def create(self, data):
        """Create a dataset based on POST args
        """
        # Create Dataset object
        instance = self.Component(**data)

        # Add Dataset object in database
        res = add_in_db(instance)

        if res != 'added':
            set_session_var('errors', str(res))
            return redirect(url_for('%s.index' % self.name))

        set_session_var('success', res)
        return redirect(url_for('%s.index' % self.name))

    def get_instance(self, name):
        """
        """
        instance = self.get_one_instance('name', name)

        if type(instance) != self.Component:
            set_session_var('errors', str(instance))
            return redirect(url_for('%s.index' % self.name))

        check_if_session_var_exists('errors')
        check_if_session_var_exists('success')

        args = {
            'session': session,
            'instance': instance
        }

        return render_template("components/%s/instance.html" % self.name, **args)

    def post_instance(self, name, data):
        """
        """
        form_data = request.form
        if '_method' not in form_data:
            return redirect(url_for('%s.get_instance' % self.name))

        method = form_data['_method']

        if method == 'PUT':
            return self.update(name, data)
        elif method == 'DELETE':
            return self.delete(name)
        else:
            return redirect(url_for('%s.get_instance' % self.name, name=name))

    def update(self, name, data):
        """Update a dataset based on PUT args
        """
        instance = self.get_one_instance('name', name)

        if type(instance) != self.Component:
            set_session_var('errors', str(instance))
            return redirect(url_for('%s.index' % self.name))

        res = update_in_db(instance, data)

        if res != 'updated':
            set_session_var('errors', str(res))
            return redirect(url_for('%s.get_instance' % self.name, name=name))

        set_session_var('success', res)
        return redirect(url_for('%s.get_instance' % self.name, name=name))

    def delete(self, name):
        """Drop a dataset based on DELETE args
        """
        instance = self.get_one_instance('name', name)

        if type(instance) != self.Component:
            set_session_var('errors', str(instance))
            return redirect(url_for('%s.index' % self.name))

        res = delete_in_db(instance)

        if res != 'deleted':
            set_session_var('errors', str(res))
            return redirect(url_for('%s.index' % self.name))

        set_session_var('success', res)
        return redirect(url_for('%s.index' % self.name))
