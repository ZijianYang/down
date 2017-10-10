# -*- coding: utf-8 -*-
"""应用配置信息"""
import json
import Tool.Single
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative


@Tool.Single.singleton
class AppConfig(object):
    """
    应用配置信息
    """
    IsDeBug = False  ##是否为测试状态

    def __init__(self, configPath="./App.config"):
        """
        初始化
        """
        with open(configPath) as filestream:
            configcontent = filestream.read()
            config = json.loads(configcontent)
        dblink = DbLink(config["DbLink"])
        self.__class__.DbLink = dblink
        isdebug = config["IsDeBug"] == "True"
        self.__class__.IsDeBug = isdebug
        # 利用数据库字符串构造engine, echo为True将打印所有的sql语句, 其他数据库的链接方式可自行百度
        # engine = sqlalchemy.create_engine("mysql+pymysql://username:password@hostname/dbname",
        # encoding="utf8", echo=True)
        # 利用Session对象连接数据库
        #engine = sqlalchemy.create_engine(dblink.linkstr(), encoding=dblink.charset, echo=isdebug)
        engine = sqlalchemy.create_engine(dblink.linkstr(), echo=isdebug)
        self.engine = engine # 引擎
        dbsessinon = sqlalchemy.orm.sessionmaker(bind=engine)   # 创建会话类
        self.session = dbsessinon()  # 创建会话对象


class DbLink(object):
    """数据库连接"""

    def __init__(self, dblink):
        """初始化"""
        self.path = dblink["Path"]
        """
        self.host = dblink["Host"]
        self.port = dblink["Port"]
        self.user = dblink["User"]
        self.password = dblink["Password"]
        self.dbname = dblink["DbName"]
        self.charset = dblink["Charset"]
        """

    def linkstr(self):
        """sqlalchemy链接字"""
        return "sqlite:///%s" % (self.path)
        """
        return "mysql+pymysql://%s:%s@%s:%s/%s" % (self.user, self.password,
                                                   self.host, self.port,
                                                   self.dbname)
        """
