# -*- coding: utf-8 -*-
"""文件处理"""
import urllib.request
import os


class DownHelper(object):
    def __init__(self, dirPath, url, name=None):
        self.url = url
        self.dirPath = dirPath
        self.name = name

    def Star(self):
        if not os.path.exists(self.dirPath):
            os.mkdir(self.dirPath)
        isFile = False
        if not self.name:
            self.name = self.UrlToName(self.url)
        path = os.path.join(self.dirPath, self.name)
        isFile = os.path.splitext(self.url)[1] != ""
        if os.path.exists(path):
            print(path+"已经存在", end="")
        else:
            if isFile:
                self.DownFile(path)
            else:
                self.DownHtml(path)
        return path

    def DownFile(self, path):
        print("下载文件" + self.url, end="")
        request= urllib.request.urlopen(self.url, data=None, timeout=60)  
        try:
            if request.getcode()==200:        
                data =request.read()
                with open(path, 'wb') as f:
                    f.write(data)            
                print("下载完成", end="")
            else:
                print(path+"下载失败", end="")
        except:
            print("Error: 下载失败")

    def DownHtml(self, path):
        print("下载网页" + self.url, end="")
        page = urllib.request.urlopen(self.url, data=None, timeout=60)        
        html = page.read()
        with open(path, "wb+") as f:
            f.write(html)
        print("下载完成", end="")

    def UrlToName(self, url):
        fileName = url.replace(':', '~').replace('/', '—').replace('?', '？')
        return fileName

    def UrlToPath(dirPath, url):
        fileName = url.replace(':', '~').replace('/', '—').replace('?', '？')
        tempPath = os.path.join(dirPath, "%s" % (fileName))
        return tempPath