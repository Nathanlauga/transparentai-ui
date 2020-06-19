from flask import current_app as app

__all__ = [
    'dev'
]


# Development
from .dev import dev, load_csv

app.add_url_rule('/dev', endpoint='dev', view_func=dev, methods=['GET'])

app.add_url_rule('/dev/load', endpoint='load_csv', view_func=load_csv, methods=['GET','POST'])