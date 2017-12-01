"""判断是否为移动端"""
from flask import request

def get():
    """获取"""
    useragent = request.headers.get('User-Agent').lower()
    print(useragent)
    devices = ["android", "mac os", "windows phone"]
    for item in devices:
        if useragent.find(item) > -1:
            return True
    return False
