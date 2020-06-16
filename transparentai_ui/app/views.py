from flask import render_template, request, redirect, url_for
from flask_babel import _
from app import app
import pandas as pd


@app.route('/', methods=['GET', 'POST'])
def index():
    title = _('Home')
    return render_template("index.html", title=title)


@app.errorhandler(404)
def not_found(e):
    title = 'Page not found'
    return render_template("404.html", title=title)
