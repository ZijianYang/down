from flask import render_template, request
from . import mobile



@mobile.route('/')
def index():
    """首页"""
    return render_template('/mobile/index.mobile.html')
