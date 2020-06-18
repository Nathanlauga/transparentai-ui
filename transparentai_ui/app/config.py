
import sys
import os 
path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# Main
ENV='development'
SECRET_KEY='this_is_the_scret_key'
DEBUG=True

# Babel
ACCEPTED_LANG=['en','fr']
DEFAULT_LANG='en'
LANGUAGES = ['en', 'fr'] 

# Database
SQLALCHEMY_DATABASE_URI='sqlite:///%s/src/transparentai.db'%(path.replace('\\','/'))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False