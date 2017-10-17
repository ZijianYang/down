# -*- coding: utf-8 -*-
"""文件处理"""
import urllib.request
import os


class DownHelper(object):
    """下载处理"""
    def __init__(self, dirpath, url, name=None):
        self.url = url
        self.dirpath = dirpath
        self.name = name

    def star(self):
        """开始"""
        if not os.path.exists(self.dirpath):
            os.mkdir(self.dirpath)
        isfile = False
        if not self.name:
            self.name = self.urltoname(self.url)
        path = os.path.join(self.dirpath, self.name)
        isfile = os.path.splitext(self.url)[1] != ""
        if os.path.exists(path):
            print(path+"已经存在", end="")
        else:
            if isfile:
                self.downfile(path)
            else:
                self.downhtml(path)
        return path

    def downfile(self, path):
        """下载文件"""
        print("下载文件" + self.url, end="")
        request = urllib.request.urlopen(self.url, data=None, timeout=60)
        if request.getcode() == 200:
            data = request.read()
            with open(path, 'wb') as filestream:
                filestream.write(data)
            print("下载完成", end="")
        else:
            print(path+"下载失败", end="")


    def downhtml(self, path):
        """下载网页"""
        print("下载网页" + self.url, end="")
        page = urllib.request.urlopen(self.url, data=None, timeout=60)
        html = page.read()
        with open(path, "wb+") as filestream:
            filestream.write(html)
        print("下载完成", end="")

    def urltoname(self, url):
        """urltoname"""
        filename = url.replace(':', '~').replace('/', '—').replace('?', '？')
        return filename

    def urltopath(dirpath, url):
        """urltopath"""
        filename = url.replace(':', '~').replace('/', '—').replace('?', '？')
        temppath = os.path.join(dirpath, "%s" % (filename))
        return temppath
