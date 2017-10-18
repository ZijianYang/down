"""时间处理"""
import time
from datetime import datetime

def timestr():
    """输出当前时间字符串"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def timeobj():
    """输出当前时间"""
    return datetime.now()
