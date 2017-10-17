"""规则具体处理"""
import os
import re
import time
import Store
import Store.Entity
from AppConfig import AppConfig
import Tool


class RuleHandle(object):
    """规则具体处理"""

    # 每层处理只对上层进行处理，并对本层进行下载和数据保存
    def __init__(self, key, fileDirPath=None):
        """构造函数"""
        self.key = key
        if not fileDirPath:
            self.filedirpath = os.path.join(AppConfig().DownPath, self.key)
        else:
            self.filedirpath = fileDirPath

    def handlerooturl(self, downconfig):
        """处理RootUrl"""
        # 没有上层处理，对rooturl进行下载和数据保存，不做处理
        print("处理RootUrl:", end=" ")
        rooturl = downconfig.rooturl
        rooturlinfo = Store.UrlRepository().getsbykeyrequesturl(
            self.key, rooturl).first()
        if not rooturlinfo:
            filepath = Tool.DownHelper.star(self.filedirpath, rooturl)
            rootrule = downconfig.rule("RootUrl")
            url = Store.Entity.Url(rootrule["RuleNo"], filepath, rooturl,
                                   rooturl)
            Store.UrlRepository().add(self.key, url)  #根处理特殊源和结果是一个
            print("处理完毕")
        else:
            print("已存在数据,继续")

    def handlerule(self, downconfig, urlinfo):
        """按照规则处理:下载配置,数据url"""
        rule = downconfig.rule(urlinfo.ruleno)  #查找处理规则
        ruletype = rule["Type"]
        requesturl = urlinfo.resulturl  # 处理过后地址的结果地址，即为下一次请求地址和源地址
        print("请求地址：%s；规则类型%s" % (requesturl, ruletype))  #
        if ruletype == Store.Enum.ERuleType.page.name:
            self.handlepage(requesturl, rule)
        elif ruletype == Store.Enum.ERuleType.regex.name:
            self.handleregex(requesturl, rule)

    def handlepage(self, sourceurl, rule):
        """按照规则处理"""
        temppath = Tool.DownHelper.urltopath(self.filedirpath, sourceurl)
        with open(temppath, "rb") as filestream:
            html = filestream.read().decode('utf-8')
        regex = rule["PageEndRegex"]
        pattern = re.compile(regex)
        match = pattern.search(html)
        total = int(match.group("total"))
        i = int(rule["PageStart"])
        print("源%s共产生%s条" % (sourceurl, total))
        while i <= total:
            Tool.Time.currenttimeprint(end=" ")
            siteurl = sourceurl[0:sourceurl.index("/", 8)]
            requesturl = rule["UrlFormat"].replace("{SiteUrl}", siteurl)
            requesturl = requesturl.replace("{Number}", str(i))
            requesturlinfoes = Store.UrlRepository().getsbykeyrequesturl(
                self.key, requesturl)
            i = i + 1
            if requesturlinfoes.count() == 0:
                filepath = Tool.DownHelper.star(self.filedirpath, requesturl)
                if filepath:
                    url = Store.Entity.Url(rule["NextNo"], filepath, sourceurl,
                                           requesturl)
                    Store.UrlRepository().add(self.key, url)
                    print("处理完毕")
            else:
                print("%s已经存在数据,继续" % (requesturl))
        Store.UrlRepository().endbyrequesturl(sourceurl)

    def handleregex(self, sourceurl, rule):
        """按照规则处理"""
        temppath = Tool.DownHelper.urltopath(self.filedirpath, sourceurl)
        with open(temppath, "rb") as filestream:
            html = filestream.read().decode('utf-8')
        urlregex = rule["UrlRegex"]
        urlpattern = re.compile(urlregex)
        urls = urlpattern.findall(html)
        nameregex = rule["NameRegex"]
        namepattern = re.compile(nameregex)
        names = namepattern.findall(html)
        md5regex = rule["Md5Regex"]
        md5pattern = re.compile(md5regex)
        md5s = md5pattern.findall(html)
        print("源%s共产生%s条" % (sourceurl, len(urls)))
        i = 0
        successcount = 0  #成功数量
        for item in urls:
            Tool.Time.currenttimeprint(end="")
            requesturl = item
            requesturlinfoes = Store.UrlRepository().getsbykeyrequesturl(
                self.key, requesturl)
            if requesturlinfoes.count() == 0:
                name = names[i] + os.path.splitext(requesturl)[1]
                filehistory = Store.FileHistoryRepository().getbymd5(md5s[i])
                if filehistory:  #已存在不用下载，可减少下载
                    url = Store.Entity.Url(rule["NextNo"],
                                           filehistory.filepath, sourceurl,
                                           requesturl, filehistory.md5)
                    Store.UrlRepository().add(self.key, url)
                    successcount = successcount + 1
                    print("%s已经存在历史数据" % (requesturl))
                else:
                    filepath = Tool.DownHelper.star(self.filedirpath, requesturl, name)
                    if filepath:
                        url = Store.Entity.Url(rule["NextNo"], filepath, sourceurl, requesturl)
                        Store.UrlRepository().add(self.key, url)
                        successcount = successcount + 1
                print("处理完毕")
            else:
                print("%s已经存在数据，继续" % (requesturl))
            i = i + 1
        if successcount == len(urls):# 全部下载成功
            Store.UrlRepository().endbyrequesturl(sourceurl)
