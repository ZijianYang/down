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
    def __init__(self, key, fileDirPath=None):
        """构造函数"""
        self.key = key
        if not fileDirPath:
            self.filedirpath = os.path.join(AppConfig().DownPath, self.key)
        else:
            self.filedirpath = fileDirPath

    def HandleRootUrl(self, downconfig):
        """处理RootUrl"""
        print("处理RootUrl:", end="")
        url = downconfig.rooturl
        rooturlinfo = UrlRepository().getsbykeyrequesturl(url, self.key).first()
        if not rooturlinfo:
            filepath = DownHelper(self.filedirpath, url).Star()
            rootrule = [
                f for f in downconfig.rules if f["RuleNo"] == "RootUrl"
            ][0]
            UrlRepository().add(
                self.key, rootrule["RuleNo"], filepath, "RootUrl", url)
            print("处理完毕")
        else:
            print("已处理,继续")

    # 按照规则处理
    def HandleRule(self, downConfig, urlItem):
        rule = [
            f for f in downConfig.rules if f["RuleNo"] == urlItem.ruleno
        ][0]
        ruleType = rule["Type"]
        print("地址：%s；规则类型%s" % (urlItem["ResultUrl"], ruleType))
        if ruleType == Store.Enum.RuleType.page.name:
            self.HandlePage(urlItem, rule)
        elif ruleType == Store.Enum.RuleType.regex.name:
            self.HandleRegex(urlItem, rule)

    # 按照规则处理
    def HandlePage(self, urlItem, rule):
        sourceUrl = urlItem["ResultUrl"]
        tempPath = DownHelper.UrlToPath(self.filedirpath, sourceUrl)
        with open(tempPath, "rb") as f:
            html = f.read().decode('utf-8')
        regex = rule["PageEndRegex"]
        pattern = re.compile(regex)
        match = pattern.search(html)
        total = int(match.group("total"))
        i = int(rule["PageStart"])
        print("源%s共产生%s条" % (sourceUrl, total))
        while i <= total:
        # while i <= 1:
            print("当前时间：%s；" % (time.strftime('%Y-%m-%d  %H:%M:%S',time.localtime(time.time()))) , end="")        
            siteUrl = sourceUrl[0:sourceUrl.index("/", 8)]
            requestUrl = rule["UrlFormat"].replace("{SiteUrl}", siteUrl)
            requestUrl = requestUrl.replace("{Number}", str(i))
            rootUrlInfo = UrlRepository().getsbykeyrequesturl(requestUrl, self.key)
            i = i + 1
            if len(rootUrlInfo) == 0:
                filePath = DownHelper(self.filedirpath, requestUrl).Star()
                UrlRepository().add(
                    self.key, rule["NextNo"], filePath, sourceUrl, requestUrl)
                print("处理完毕")
            else:
                print("%s已经处理" % (requestUrl))
        UrlRepository().endbyrequesturl(sourceUrl)

    # 按照规则处理
    def HandleRegex(self, urlItem, rule):
        sourceUrl = urlItem["ResultUrl"]
        tempPath = DownHelper.UrlToPath(self.filedirpath, sourceUrl)
        with open(tempPath, "rb") as f:
            html = f.read().decode('utf-8')
        urlRegex = rule["UrlRegex"]
        urlPattern = re.compile(urlRegex)
        urls = urlPattern.findall(html)
        nameRegex = rule["NameRegex"]
        namePattern = re.compile(nameRegex)
        names = namePattern.findall(html)
        print("源%s共产生%s条" % (sourceUrl, len(urls)))
        i = 0
        for item in urls:
            print("当前时间：%s；" % (time.strftime('%Y-%m-%d  %H:%M:%S',time.localtime(time.time()))) , end="")                    
            requestUrl = item
            rootUrlInfo = UrlRepository().getsbykeyrequesturl(requestUrl, self.key)
            if len(rootUrlInfo) == 0:
                DownHelper(self.filedirpath, requestUrl,
                           names[i] + os.path.splitext(requestUrl)[1]).Star()
                UrlRepository().add(self.key, rule["NextNo"], self.filedirpath,sourceUrl,requestUrl)
                print("处理完毕")
            else:
                print("%s已经处理" % (requestUrl))
            i = i + 1
        UrlRepository().endbyrequesturl(sourceUrl)

