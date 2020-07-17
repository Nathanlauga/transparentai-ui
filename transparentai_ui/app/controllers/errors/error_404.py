from flask import render_template
from flask import current_app as app
from flask_babel import _
from ...controllers.services.commons import get_header_attributes


@app.errorhandler(404)
def not_found(e):
    title = _('404 error')
    header = get_header_attributes()
    
    return render_template("errors/404.html", title=title, header=header)
