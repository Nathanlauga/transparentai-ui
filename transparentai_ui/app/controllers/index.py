from flask import render_template
from flask_babel import _


def index():
    title = _('Home')
    return render_template("index.html", title=title)
