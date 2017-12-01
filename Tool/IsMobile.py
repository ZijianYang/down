"""判断是否为移动端"""
from flask import request

def get():
    """获取"""
    useragent = request.headers.get('User-Agent')
    print(useragent)