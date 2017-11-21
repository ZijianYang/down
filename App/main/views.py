from flask import render_template, request
from . import main



@main.route('/')
def index():
    """首页"""
    return render_template('index.html', name='test')

@main.route('/fix')
def indexfixcolumn():
    """首页"""
    return render_template('indexfix.html', name='test')

@main.route('/computed')
def indexfixcolumn():
    """首页"""
    return render_template('indexcomputed.html', name='test')


@main.route('/detail')
def detail():
    """首页"""
    return render_template('detail.html')
