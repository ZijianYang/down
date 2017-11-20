"""接口"""
from flask import Flask, render_template, jsonify, request
from flask_script import Manager
from Tool import ClassToDict
import Store
import Store.Entity

APP = Flask(__name__, static_folder='', static_url_path='')

#解决Jinja2与Vue.js的模板冲突 解决思路也比较简单，就是在需要Jinja2渲染的时候添加一个空格，而vue.js渲染的时候则不需要空格，python脚本如下
APP.jinja_env.variable_start_string = '{{ '
APP.jinja_env.variable_end_string = ' }}'
MANAGER = Manager(APP)


@APP.route('/')
def index():
    """首页"""
    return render_template('index.html', name='test')


@APP.route('/detail')
def detail():
    """首页"""
    return render_template('detail.html')


@APP.route('/images/<int:pageindex>', methods=['GET', 'POST'])
def images(pageindex):
    """查询"""
    args = request.args
    tag = args.get("tag", None, type=str)
    pagesize = args.get("pagesize", 10, type=int)
    score = args.get("score", 0, type=int)
    print('1：%s;2：%s;3：%s;4：%s;' % (score, tag, pagesize, pageindex))
    data = Store.FileHistoryRepository().getspage(score, tag, pageindex,
                                                  pagesize)
    #print(ClassToDict.todict(data["list"][0]))
    return jsonify({
        'list': [{
            'id': item.id,
            'url': item.filepath.replace("\\", "/"),
            'md5': item.md5,
            'score': item.remark1,
            'tags': item.remark2
        } for item in data["list"]],
        'count':
        data["total"]
    })


@APP.route('/image/<int:imageid>', methods=['GET', 'POST'])
def image(imageid):
    """查询"""
    data = Store.FileHistoryRepository().getbyid(imageid)
    return jsonify({
        'id': data.id,
        'url': data.filepath.replace("\\", "/"),
        'md5': data.md5,
        'score': data.remark1,
        'tags': data.remark2
    } if data else {})


@APP.errorhandler(404)
def page_not_fount(e):
    return render_template('404.html'), 404


@APP.errorhandler(500)
def page_not_fount(e):
    return render_template('404.html'), 500


if __name__ == '__main__':
    MANAGER.run()
