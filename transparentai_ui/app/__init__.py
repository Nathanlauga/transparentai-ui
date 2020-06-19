import os

from flask import Flask, request, session
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_babel import _

config_filename = os.path.abspath(os.path.dirname(__file__)) + "/config.py"

app = Flask(__name__, instance_relative_config=True, template_folder='views')
app.config.from_pyfile(config_filename)

babel = Babel(app)
db = SQLAlchemy(app)
# app.config.from_object("config")


@babel.localeselector
def get_locale():
    best_match = request.accept_languages.best_match(app.config['LANGUAGES'])

    if request.args.get('lang'):
        lang = request.args.get('lang')
        print(request.args)
        print('get :', lang)

        if lang not in app.config['ACCEPTED_LANG']:
            session['lang'] = best_match
        else:
            session['lang'] = lang

    elif 'lang' not in session:
        session['lang'] = best_match

    print('res :', session['lang'])
    return session['lang']


with app.app_context():
    from .controllers import *
    db.create_all()
