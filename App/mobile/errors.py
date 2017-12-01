from flask import render_template, request, jsonify
from . import mobile


@mobile.errorhandler(404)
def page_not_fount(e):
    return render_template('404.html'), 404


@mobile.errorhandler(500)
def page_not_fount(e):
    return render_template('404.html'), 500