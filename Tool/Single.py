"""单例修饰器"""

def singleton(cls, *args, **kwargs):
    """单例修饰器"""
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton
