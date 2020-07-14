from flask import render_template, session
from flask_babel import _


def index():
    title = _('Home')
    return render_template("index.html", title=title)


def temp():
    return render_template("test.html", session=session)
