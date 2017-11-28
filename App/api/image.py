from flask import jsonify, request
from . import api
import Store


@api.route('/images/<int:pagenumber>', methods=['GET', 'POST'])
def images(pagenumber):
    """查询"""
    args = request.args
    tag = args.get("tag", None, type=str)
    tag = tag.split(" ")
    pagesize = args.get("pagesize", 10, type=int)
    score = args.get("score", 0, type=int)
    sort = args.get("sort", "score", type=str)
    pageindex = pagenumber - 1
    print('score：%s;tag：%s;pagesize：%s;pageindex：%s;sort: %s' %
          (score, tag, pagesize, pageindex, sort))
    if sort == "random":
        data = Store.FileHistoryRepository().getsradom(score, tag, pagesize)
    else:
        data = Store.FileHistoryRepository().getspage(score, tag, pageindex,
                                                      pagesize, sort)
    #print(ClassToDict.todict(data["list"][0]))
    return jsonify({
        'items': [{
            'id': item.id,
            'url': item.filepath.replace("\\", "/"),
            'md5': item.md5,
            'score': item.remark1,
            'tags': item.remark2
        } for item in data["list"]],
        'total':
        data["total"]
    })


@api.route('/images/<int:star>/<int:end>', methods=['GET', 'POST'])
def imagesbysection(star, end):
    """查询"""
    args = request.args
    tag = args.get("tag", None, type=str)
    tag = tag.split(" ")
    score = args.get("score", 0, type=int)
    sort = args.get("sort", "score", type=str)
    print('score：%s;tag：%s;star%s;end%s;sort: %s' % (score, tag, star, end,
                                                     sort))
    if sort == "random":
        sectionlength = end - star
        data = Store.FileHistoryRepository().getsradom(score, tag,
                                                       sectionlength)
    else:
        data = Store.FileHistoryRepository().getsbysection(
            score, tag, star, end, sort)
    return jsonify([{
        'id': item.id,
        'url': item.filepath.replace("\\", "/"),
        'md5': item.md5,
        'score': item.remark1,
        'tags': item.remark2
    } for item in data])


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
