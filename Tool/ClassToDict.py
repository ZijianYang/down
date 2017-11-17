"""class转为字典"""

def todict(obj):
    """把对象(支持单个对象、list、set)转换成字典"""
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__
    if is_list or is_set:
        obj_arr = []
        for obj in obj:
            #把Object对象转换成Dict对象
            dictobj = {}
            dictobj.update(obj.__dict__)
            obj_arr.append(dictobj)
        return obj_arr
    else:
        dictobj = {}
        dictobj.update(obj.__dict__)
        return dictobj
