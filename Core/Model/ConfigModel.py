# -*- coding: utf-8 -*-
"""json解析"""
from Store.Entity.Config import Config
import Tool.Time
import json


class ConfigModel(object):
    """下载配置"""

    def __init__(self, data):
        """从文件获取dict"""
        if type(data)!=dict:
            with open(data) as filestream:
                configcontent = filestream.read()
                configdict = json.loads(configcontent)
                data = configdict
        self.key = data["Key"]
        self.rooturl = data["RootUrl"]
        self.rules = data["Rules"]

    def config(self):
        """返回数据实体"""
        config = Config(
            key=self.key,
            content=json.dumps(self.rules),
            rooturl=self.rooturl,
            adddate=Tool.Time.timeobj())
        return config    
