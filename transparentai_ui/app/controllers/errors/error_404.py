from flask import render_template
from flask import current_app as app
from flask_babel import _

@app.errorhandler(404)
def not_found(e):
    title = _('404 error')
    return render_template("errors/404.html", title=title)
