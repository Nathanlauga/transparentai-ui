from flask import render_template, session
from flask_babel import _
from .services.commons import get_header_attributes


def index():
    title = _('Home')
    header = get_header_attributes()

    return render_template("index.html", title=title, header=header, session=session)


def temp():
    return render_template("test.html", session=session)
