from flask import Flask

def create_app():
    app = Flask(__name__, static_folder='', static_url_path='')

    #解决Jinja2与Vue.js的模板冲突 解决思路也比较简单，就是在需要Jinja2渲染的时候添加一个空格，而vue.js渲染的时候则不需要空格，python脚本如下
    app.jinja_env.variable_start_string = '{{ '
    app.jinja_env.variable_end_string = ' }}'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/')

    return app
