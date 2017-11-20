#!/usr/bin/env python
import os
#from App import create_app
from flask_script import Manager, Shell
from flask import Flask

def create_app():
    app = Flask(__name__, static_folder='', static_url_path='', template_folder='App/templates')

    #解决Jinja2与Vue.js的模板冲突 解决思路也比较简单，就是在需要Jinja2渲染的时候添加一个空格，而vue.js渲染的时候则不需要空格，python脚本如下
    app.jinja_env.variable_start_string = '{{ '
    app.jinja_env.variable_end_string = ' }}'

    from App.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from App.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


APP = create_app()
MANAGER = Manager(APP)

def make_shell_context():
    return dict(app=APP)

MANAGER.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    MANAGER.run()
