import os
from flask import current_app as app

__all__ = [
    'index',
    'errors',
    'dev'
]

# Error handling
from .errors.error_404 import not_found

# Routes
from .index import index
from .dev.dev import dev


app.add_url_rule('/', endpoint='index', view_func=index,
                 methods=['GET', 'POST'])
app.add_url_rule('/dev', endpoint='dev', view_func=dev, methods=['GET'])
