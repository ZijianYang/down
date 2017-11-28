from flask import render_template, request
from . import main



@main.route('/')
def index():
    """首页"""
    return render_template('index.html', name='test')

@main.route('/computed')
def indexcomputed():
    """首页"""
    return render_template('indexcomputed.html', name='test')

@main.route('/css')
def indexcss():
    """首页"""
    return render_template('indexcss.html', name='test')

@main.route('/detail')
def detail():
    """首页"""
    return render_template('detail.html')

@main.route('/test')
def test():
    """首页"""
    return render_template('test.html', name='test')

@main.route('/test/')
def testindex():
    """首页"""
    return render_template('testindex.html', name='test')

@main.route('/test/detail')
def testdetail():
    """首页"""
    return render_template('testdetail.html')
