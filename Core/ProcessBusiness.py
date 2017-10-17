# -*- coding: utf-8 -*-
"""抓取数据"""
from Store.ConfigRepository import ConfigRepository
from Store.UrlRepository import  UrlRepository
from Store.UrlDetailRepository import  UrlDetailRepository
from Core.Model import ConfigModel
import sys
import os
import shutil
from Core.RuleHandle import RuleHandle
from AppConfig import AppConfig


def new(key):
    """开始"""
    print("key值：%s开始" % (key))
    config = ConfigRepository().getbykey(key)
    if not config:
        print("未找到配置信息")
        sys.exit(0)
    configmodel = ConfigModel(ConfigRepository().getbykey(key))
    rulehandle = RuleHandle(key)
    rulehandle.handlerooturl(configmodel)
    print("根地址%s;规则数量%s;" % (configmodel.rooturl, len(configmodel.rules)))
    noendurls = UrlRepository().getsnoendbynorulenokey(key, "End")
    while noendurls.count() != 0:
        for item in noendurls:
            rulehandle.handlerule(configmodel, item)
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
