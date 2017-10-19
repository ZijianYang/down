# -*- coding: utf-8 -*-
"""文件处理"""
import urllib.request
import os


def star(dirpath, url, name=None):
    """开始"""
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    isfile = False
    if not name:
        name = urltoname(url)
    path = os.path.join(dirpath, name)
    isfile = os.path.splitext(url)[1] != ""
    if not os.path.exists(path):
        try:
            if isfile:
                downfile(url, path)
            else:
                downhtml(url, path)            
        except:
            return None
    return path

def downfile(url, path):
    """下载文件"""
    request = urllib.request.urlopen(url, data=None, timeout=60)
    if request.getcode() == 200:
        data = request.read()
        with open(path, 'wb') as filestream:
            filestream.write(data)

def downhtml(url, path):
    """下载网页"""
    page = urllib.request.urlopen(url, data=None, timeout=60)
    html = page.read()
    with open(path, "wb+") as filestream:
        filestream.write(html)

def urltoname(url):
    """urltoname"""
    filename = url.replace(':', '~').replace('/', '—').replace('?', '？')
    return filename

def urltopath(dirpath, url):
    """urltopath"""
    filename = url.replace(':', '~').replace('/', '—').replace('?', '？')
    temppath = os.path.join(dirpath, "%s" % (filename))
    return temppath
