from flask import render_template, session
from flask_babel import _
from .services.commons import get_header_attributes, get_all_projects
from ..utils.session import check_if_session_var_exists


def index():
    title = _('Home')
    header = get_header_attributes()
    projects = get_all_projects()

    check_if_session_var_exists('errors')
    check_if_session_var_exists('success')

    return render_template("index.html", title=title, header=header, session=session, projects=projects)


def temp():
    return render_template("test.html", session=session)
