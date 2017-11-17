"""接口"""
from flask import Flask
from flask_script import Manager
import Store
import Store.Entity

APP = Flask(__name__)
MANAGER = Manager(APP)




@APP.route('/')
def index():
    """首页"""
    return '<h1>Hello World!</h1>'


@APP.route('/user/<name>')
def user(name):
    """aaa"""
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    MANAGER.run()
    