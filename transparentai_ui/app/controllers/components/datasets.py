import inspect
from flask import render_template, request, redirect, url_for
from flask import current_app as app
from flask_babel import _

from ...models.components.datasets import Dataset
from ... import db


def add_in_db(obj):
    """
    """
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as exception:
        db.session.rollback()
        return exception
    return 'added'


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


def get_all_datasets():
    """
    """
    datasets = Dataset.query.all()
    return datasets


def index():
    """Get the datasets
    """
    create_test_dataset()
    datasets = get_all_datasets()

    return render_template("components/datasets/index.html", datasets=datasets)


def get_request_attribute(form_data, key, default=''):
    """
    """
    if key not in form_data:
        return ''
    return form_data[key]


def create():
    """Create a dataset based on POST args
    """
    data = request.form
    dataset_attr = ['name', 'path', 'target', 'score', 'protected_attr']
    dataset_args = dict()

    # Retrieve Dataset Attributes from request.form
    for attr in dataset_attr:
        dataset_args[attr] = get_request_attribute(data, attr)

    # Create Dataset object
    dataset = Dataset(**dataset_args)

    # Add Dataset object in database
    res = add_in_db(dataset)

    datasets = get_all_datasets()

    if res == 'added':
        return render_template("components/datasets/index.html", datasets=datasets, valid=res)

    print(res)
    return render_template("components/datasets/index.html", datasets=datasets, error=res)


def update():
    """Update a dataset based on PUT args
    """
    return redirect(url_for('datasets.index'))


def delete():
    """Drop a dataset based on DELETE args
    """
    return redirect(url_for('datasets.index'))
