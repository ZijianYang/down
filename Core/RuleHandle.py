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
        #while i <= 1:
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
        urlstrs = urlpattern.findall(html)
        nameregex = rule["NameRegex"]
        namepattern = re.compile(nameregex)
        names = namepattern.findall(html)
        md5regex = rule["Md5Regex"]
        md5pattern = re.compile(md5regex)
        md5s = md5pattern.findall(html)
        totalcount = len(urlstrs) #总处理数量
        print("源%s共产生%s条" % (sourceurl, totalcount))
        i = 0 #循环用计数器
        successcount = 0  #成功数量
        urls = [] # 数据库url集合
        for requesturl in urlstrs:
            Tool.Time.currenttimeprint(end="") #输出当前时间
            requesturlinfo = Store.UrlRepository().getsbykeyrequesturl(
                self.key, requesturl).first() #检查数据是否已经存在
            if not requesturlinfo:
                name = names[i] + os.path.splitext(requesturl)[1] #计算文件名
                filehistory = Store.FileHistoryRepository().getbymd5(md5s[i])
                if filehistory:  #已存在不用下载，可减少下载
                    url = Store.Entity.Url(rule["NextNo"],
                                           filehistory.filepath, sourceurl,
                                           requesturl, filehistory.md5)
                    Store.UrlRepository().add(self.key, url)
                    urls.append(url)
                    successcount = successcount + 1
                    print("%s已经存在历史数据" % (requesturl))
                else:
                    filepath = Tool.DownHelper.star(self.filedirpath, requesturl, name)
                    if filepath:
                        url = Store.Entity.Url(rule["NextNo"], filepath, sourceurl, requesturl)
                        Store.UrlRepository().add(self.key, url)
                        urls.append(url)
                        successcount = successcount + 1
                print("处理完毕")
            else:
                urls.append(requesturlinfo)
                print("%s已经存在数据，继续" % (requesturl))
            i = i + 1
            print("进度：%s/%s;成功%s" % (i, totalcount, successcount))
        if 'Detail' in rule.keys():
            self.urldetail(html, rule["Detail"], urls)
        if successcount == totalcount:# 全部下载成功
            Store.UrlRepository().endbyrequesturl(sourceurl)


    def urldetail(self, html, ruledetails, urls):
        """处理详情信息"""
        values = {}
        for ruledetail in ruledetails:
            if ruledetail["Type"] == "Fix":
                values["Fix"] = ruledetail["Value"]
            elif ruledetail["Type"] == "Regex":
                regex = ruledetail["Regex"]
                pattern = re.compile(regex)
                regexvalues = pattern.findall(html)
                values["Regex"] = regexvalues
        i = 0 # 循环计数
        for url in urls:
            urldetails = []
            for (key, value) in values.items():
                if key == "Fix":
                    detailkey = [f for f in ruledetails if f["Type"] == "Fix"][0]["Key"]
                    urldetail = Store.Entity.UrlDetail(detailkey, value, url.id)
                elif key == "Regex":
                    detailkey = [f for f in ruledetails if f["Type"] == "Regex"][0]["Key"]
                    urldetail = Store.Entity.UrlDetail(detailkey, value[i], url.id)
                urldetails.append(urldetail)
            Store.UrlDetailRepository().adds(url.resulturl, urldetails)
            i = i + 1
