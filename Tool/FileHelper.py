# -*- coding: utf-8 -*-
"""文件帮助"""
import os
import hashlib

def filesfromdir(path, extstr=".json"):
    """从文件夹路径查询某个扩展名的文件列表,仅一层"""
    filepaths = []
    for parent, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.find(extstr) > 0:
                filepaths.append(os.path.join(parent, filename))
    return filepaths

def filesfrompath(path='', extstr=".json"):
    """从路径获取固定扩展名文件列表，仅一层:传入目录路径则遍历，文件路径则放入列表"""
    filepaths = []
    if os.path.isdir(path):
        filepaths = filesfromdir(path, extstr)
    elif os.path.isfile(path):
        if path.find(extstr) > 0:
            filepaths.append(path)
        else:
            raise Exception("路径不正确:%s" % (path))
    else:
        raise Exception("路径不正确:%s" % (path))
    return filepaths

def allfilefromdir(dirpath, includes=None):
    """遍历文件夹下所有文件，所有层"""
    filelist = os.listdir(dirpath) #列出文件夹下所有的目录与文件
    result = []
    for i in range(0, len(filelist)):
        path = os.path.join(dirpath, filelist[i])
        if os.path.isfile(path):
            if includes:
                ext = os.path.splitext(os.path.split(path)[1])[1]
                if ext in includes:
                    result.append(path)
            else:
                result.append(path)
        else:
            result = result + allfilefromdir(path, includes)
    return result

def noexitcreatdir(configpath):
    """检查路径如果不存在则创建"""
    if not os.path.exists(configpath):
        os.makedirs(configpath)

def md5frompath(filepath):
    """根据filepath计算md5 """
    with open(filepath, 'rb') as filestream:
        md5obj = hashlib.md5()
        md5obj.update(filestream.read())
        hashstr = md5obj.hexdigest()
        return hashstr
