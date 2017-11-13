# -*- coding: utf-8 -*-
"""抓取数据"""
from Store.ConfigRepository import ConfigRepository
from Store.UrlRepository import UrlRepository
from Store.UrlDetailRepository import UrlDetailRepository
from Core.Model import ConfigModel
import sys
import os
import shutil
import datetime
from Core.RuleHandle import RuleHandle
from AppConfig import AppConfig


def new(key):
    """开始"""
    print("key值：%s开始" % (key))
    config = ConfigRepository().getbykey(key)
    if not config:
        print("未找到配置信息")
        sys.exit(0)
    configmodel = ConfigModel(config)
    rulehandle = RuleHandle(key)
    rulehandle.handlerooturl(configmodel)
    print("根地址%s;规则数量%s;" % (configmodel.rooturl, len(configmodel.rules)))
    noendurls = UrlRepository().getsnoendbynorulenokey(key, "End")
    while noendurls.count() != 0:
        for item in noendurls:
            rulehandle.handlerule(configmodel, item)
        noendurls = UrlRepository().getsnoendbynorulenokey(key, "End")
    print("全部完成")


def newpardon(key, pagecount=4):
    """开始新建文件，重新重复一定数量"""
    print("key值：%s开始" % (key))
    datetimestr = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    filepath = os.path.join(AppConfig().DownPath, key, datetimestr)
    config = ConfigRepository().getbykey(key)
    if not config:
        print("未找到配置信息")
        sys.exit(0)
    configmodel = ConfigModel(config)
    rulepage = [f for f in configmodel.rules if f["Type"] == "page"][0]
    rulepage["PageEnd"] = pagecount
    rulehandle = RuleHandle(key, filepath)
    rulehandle.handlerooturl(configmodel, False)
    print("根地址%s;规则数量%s;" % (configmodel.rooturl, len(configmodel.rules)))
    noendurls = UrlRepository().getsnoendbynorulenokey(key, "End")
    while noendurls.count() != 0:
        for item in noendurls:
            rulehandle.handlerule(configmodel, item, False)
        noendurls = UrlRepository().getsnoendbynorulenokey(key, "End")
    print("全部完成")


def clear(key, isall=None):
    """清理"""
    if isall:
        filedirpath = os.path.join(AppConfig().DownPath, key)
        if os.path.exists(filedirpath):
            shutil.rmtree(filedirpath)
        print("清理文件成功，Path:%s" % (filedirpath))
    resulturldetail = UrlDetailRepository().deletebykey(key)
    resulturl = UrlRepository().deletebykey(key)
    print("清理url，共%s条;清理urldetail，共%s条;" % (resulturl, resulturldetail))


# def clearnew(key, count=1):
#     """清理最开始的页面和文件，为了获取新更新内容"""
#     config = ConfigRepository().getbykey(key)
#     if not config:
#         print("未找到配置信息")
#         sys.exit(0)
#     configmodel = ConfigModel(config)
#     rooturl = configmodel.rooturl
#     pagerule = configmodel.rule('RootUrl')
#     UrlRepository().endbyrequesturl(rooturl, False)
#     i = 1
#     successremovefilecount = 0
#     successremovedatacount = 0
#     while i <= count:
#         siteurl = rooturl[0:rooturl.index("/", 8)]
#         requesturl = pagerule["UrlFormat"].replace("{SiteUrl}", siteurl)
#         requesturl = requesturl.replace("{Number}", str(i))
#         pageurl = UrlRepository().getsbykeyresultturl(configmodel.key,
#                                                       requesturl).first()
#         if pageurl:
#             if UrlRepository().deletebyid(pageurl.id):
#                 successremovedatacount = successremovedatacount + 1
#             if os.path.exists(pageurl.filepath):
#                 os.remove(pageurl.filepath)
#                 successremovefilecount = successremovefilecount + 1
#         i = i + 1
#     print("清理成功文件数量：%s;删除数据数量%s" % (successremovefilecount,
#                                     successremovedatacount))
