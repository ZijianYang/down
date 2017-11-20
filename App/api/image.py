from flask import jsonify, request
from . import api
import Store

@api.route('/images/<int:pageindex>', methods=['GET', 'POST'])
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


@api.route('/image/<int:imageid>', methods=['GET', 'POST'])
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
