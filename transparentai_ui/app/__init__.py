import os

from flask import Flask, request
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy

config_filename = os.path.abspath(os.path.dirname(__file__)) + "/config.py"

app = Flask(__name__, instance_relative_config=True, template_folder='views')
app.config.from_pyfile(config_filename)

babel = Babel(app)
db = SQLAlchemy(app)
# app.config.from_object("config")


@babel.localeselector
def get_locale():
    print(request.accept_languages.best_match(app.config['LANGUAGES']))
    return request.accept_languages.best_match(app.config['LANGUAGES'])


with app.app_context():
    from .controllers import *
    db.create_all()
