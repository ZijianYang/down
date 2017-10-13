"""规则具体处理"""
import os
import re
import time
import Store
from Store.UrlRepository import UrlRepository
from AppConfig import AppConfig
from Tool.DownHelper import DownHelper


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
        print("处理RootUrl:", end="")
        rooturl = downconfig.rooturl
        rooturlinfo = UrlRepository().getsbykeyrequesturl(self.key,
                                                          rooturl).first()
        if not rooturlinfo:
            filepath = DownHelper(self.filedirpath, rooturl).Star()
            rootrule = [
                f for f in downconfig.rules if f["RuleNo"] == "RootUrl"
            ][0]
            UrlRepository().add(self.key, rootrule["RuleNo"], filepath,
                                rooturl, rooturl)  #根处理特殊源和结果是一个
            print("处理完毕")
        else:
            print("已处理,继续")

    def handlerule(self, downconfig, urlinfo):
        """按照规则处理:下载配置,数据url"""
        rule = [f for f in downconfig.rules
                if f["RuleNo"] == urlinfo.ruleno][0]  #查找处理规则
        ruletype = rule["Type"]
        requesturl = urlinfo.resulturl  # 处理过后地址的结果地址，即为下一次请求地址和源地址
        print("请求地址：%s；规则类型%s" % (requesturl, ruletype))  #
        if ruletype == Store.Enum.ERuleType.page.name:
            self.handlepage(requesturl, rule)
        elif ruletype == Store.Enum.ERuleType.regex.name:
            self.handleregex(requesturl, rule)

    def handlepage(self, sourceurl, rule):
        """按照规则处理"""
        temppath = DownHelper.UrlToPath(self.filedirpath, sourceurl)
        with open(temppath, "rb") as filestream:
            html = filestream.read().decode('utf-8')
        regex = rule["PageEndRegex"]
        pattern = re.compile(regex)
        match = pattern.search(html)
        total = int(match.group("total"))
        i = int(rule["PageStart"])
        print("源%s共产生%s条" % (sourceurl, total))
        while i <= total:
            #while i <= 1:
            print(
                "当前时间：%s；" % (time.strftime('%Y-%m-%d  %H:%M:%S',
                                            time.localtime(time.time()))),
                end="")
            siteurl = sourceurl[0:sourceurl.index("/", 8)]
            requesturl = rule["UrlFormat"].replace("{SiteUrl}", siteurl)
            requesturl = requesturl.replace("{Number}", str(i))
            requesturlinfoes = UrlRepository().getsbykeyrequesturl(
                self.key, requesturl)
            i = i + 1
            if requesturlinfoes.count() == 0:
                filepath = DownHelper(self.filedirpath, requesturl).Star()
                UrlRepository().add(self.key, rule["NextNo"], filepath,
                                    sourceurl, requesturl)
                print("处理完毕")
            else:
                print("%s已经处理" % (requesturl))
        UrlRepository().endbyrequesturl(sourceurl)

    def handleregex(self, sourceurl, rule):
        """按照规则处理"""
        temppath = DownHelper.UrlToPath(self.filedirpath, sourceurl)
        with open(temppath, "rb") as filestream:
            html = filestream.read().decode('utf-8')
        urlregex = rule["UrlRegex"]
        urlpattern = re.compile(urlregex)
        urls = urlpattern.findall(html)
        nameregex = rule["NameRegex"]
        namepattern = re.compile(nameregex)
        names = namepattern.findall(html)
        print("源%s共产生%s条" % (sourceurl, len(urls)))
        i = 0
        for item in urls:
            print(
                "当前时间：%s；" % (time.strftime('%Y-%m-%d  %H:%M:%S',
                                            time.localtime(time.time()))),
                end="")
            requesturl = item
            requesturlinfoes = UrlRepository().getsbykeyrequesturl(
                self.key, requesturl)
            if requesturlinfoes.count() == 0:
                DownHelper(self.filedirpath, requesturl,
                           names[i] + os.path.splitext(requesturl)[1]).Star()
                UrlRepository().add(self.key, rule["NextNo"], self.filedirpath,
                                    sourceurl, requesturl)
                print("处理完毕")
            else:
                print("%s已经处理" % (requesturl))
            i = i + 1
        UrlRepository().endbyrequesturl(sourceurl)
