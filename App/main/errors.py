from flask import render_template, request, jsonify
from . import main


@main.errorhandler(404)
def page_not_fount(e):
    return render_template('404.html'), 404


@main.errorhandler(500)
def page_not_fount(e):
    return render_template('404.html'), 500