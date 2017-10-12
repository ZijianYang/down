"""文件帮助"""
import os

def filesfromdir(configpath, extstr=".json"):
    """从文件夹路径查询某个扩展名的文件列表"""
    configpaths = []
    for parent, dirnames, filenames in os.walk(configpath):
        for filename in filenames:
            if filename.find(extstr) > 0:
                configpaths.append(os.path.join(parent, filename))
    return configpaths

def filesfrompath(configpath='', extstr=".json"):
    """从路径获取固定扩展名文件列表:传入目录路径则遍历，文件路径则放入列表"""
    configpaths = []
    if os.path.isdir(configpath):
        configpaths = filesfromdir(configpath, extstr)
    elif os.path.isfile(configpath):
        if configpath.find(extstr) > 0:
            configpaths.append(configpath)
        else:
            raise Exception("路径不正确:%s" % (configpath))
    else:
        raise Exception("路径不正确:%s" % (configpath))
    return configpaths
