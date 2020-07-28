from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from flask_restplus import Api
from flask_babel import _
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask import Flask, Blueprint, request, session
import os
import matplotlib
matplotlib.use('Agg')


config_filename = os.path.abspath(os.path.dirname(__file__)) + "/config.py"

app = Flask(__name__, instance_relative_config=True, template_folder='views')
app.config.from_pyfile(config_filename)

# Initialize babel
babel = Babel(app)

# Initiliaze SQLAlchemy
db = SQLAlchemy(app)

# app.config.from_object("config")


db_session = scoped_session(sessionmaker(bind=db.engine))


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

    from .api import initialize_routes

# api_blueprint = Blueprint('api', __name__)

# Register Blueprints
# app.register_blueprint(api_blueprint, url_prefix='/api')



    api = Api(app, version='1.0', title='TransparentAI UI',
        description='REST API behind the structure of the TransparentAI-UI Python package.',
    )
    initialize_routes(api)