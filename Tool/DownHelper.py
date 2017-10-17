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
    if os.path.exists(path):
        print(path+"已经存在", end="")
    else:
        if isfile:
            downfile(url, path)
        else:
            downhtml(url, path)
    return path

def downfile(url, path):
    """下载文件"""
    print("下载文件" + url, end="")
    try:
        request = urllib.request.urlopen(url, data=None, timeout=60)
        if request.getcode() == 200:
            data = request.read()
            with open(path, 'wb') as filestream:
                filestream.write(data)
            print("下载完成", end="")
        else:
            print(path+"下载失败", end="")
    except:
        print("下载异常:")


def downhtml(url, path):
    """下载网页"""
    print("下载网页" + url, end="")
    try:
        page = urllib.request.urlopen(url, data=None, timeout=60)
        html = page.read()
        with open(path, "wb+") as filestream:
            filestream.write(html)
        print("下载完成", end="")
    except:
        print("下载异常")

def urltoname(url):
    """urltoname"""
    filename = url.replace(':', '~').replace('/', '—').replace('?', '？')
    return filename

def urltopath(dirpath, url):
    """urltopath"""
    filename = url.replace(':', '~').replace('/', '—').replace('?', '？')
    temppath = os.path.join(dirpath, "%s" % (filename))
    return temppath
