"""接口"""
from flask import Flask, jsonify, request
from flask_script import Manager
from Tool import ClassToDict
import Store
import Store.Entity

APP = Flask(__name__,static_folder='', static_url_path='')
MANAGER = Manager(APP)


@APP.route('/')
def index():
    """首页"""
    return '<h1>Hello World!</h1>'


@APP.route('/images/<pageindex>')
def images(pageindex):
    """查询"""
    args = request.args
    tag = args.get("tag")
    pageindex = int(pageindex)
    pagesize = int(args.get("pagesize")) if args.get("pagesize") else 10
    score = int(args.get("score")) if args.get("score") else 0
    print('1：%s;2：%s;3：%s;4：%s;' % (score, tag, pagesize, pageindex))
    data = Store.FileHistoryRepository().getspage(score, tag, pageindex,
                                                  pagesize)
    #print(ClassToDict.todict(data["list"][0]))
    return jsonify({
        'list': [{
            'filepath': item.filepath.replace("\\","/"),
            'md5': item.md5,
            'score': item.remark1,
            'tags': item.remark2
        } for item in data["list"]],
        'count':
        data["total"]
    })


if __name__ == '__main__':
    MANAGER.run()
