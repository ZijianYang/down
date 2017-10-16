# -*- coding: utf-8 -*-
"""json解析"""
from Store.Entity.Config import Config
import Tool.Time
import json


class ConfigModel(object):
    """下载配置"""

    def __init__(self, data):
        """从文件获取dict"""
        if type(data) == str:
            with open(data) as filestream:
                configcontent = filestream.read()
                configdict = json.loads(configcontent)
                data = configdict
            self.key = data["Key"]
            self.rooturl = data["RootUrl"]
            self.rules = data["Rules"]
        else:
            self.key = data.key
            self.rooturl = data.rooturl
            self.rules = json.loads(data.content)

    def config(self):
        """返回数据实体"""
        config = Config(
            self.key, self.rooturl, json.dumps(self.rules))
        return config

    def rule(self, ruleno):
        """获取rule规则"""
        rootrule = [f for f in self.rules if f["RuleNo"] == ruleno][0]
        if rootrule:
            return rootrule
        else:
            raise Exception("未发现rule：%s" % (ruleno))
