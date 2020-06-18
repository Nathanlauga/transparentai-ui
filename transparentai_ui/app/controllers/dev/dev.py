from flask import render_template
from flask import current_app as app
from flask_babel import _


def dev():
    title = _('Dev')
    return render_template("dev/index.html", title=title)
