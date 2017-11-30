from flask import jsonify, request
from . import api
import Store


@api.route('/tag/<tag>', methods=['GET', 'POST'])
def tag(tag):
    """查询"""
    data = Store.TagRepository().gets(tag)
    return jsonify([{
        'tag': item.tag,
        'count': item.count,
    } for item in data])
