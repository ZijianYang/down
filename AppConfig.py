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
    DownConfigPath = "./FileStore/downconfig"
    DatabasePath = "./FileStore/downdatabase.db"
    DownPath = "./DownFile"
    def __init__(self, configPath="./App.config"):
        """
        初始化
        """
        with open(configPath) as filestream:
            configcontent = filestream.read()
            config = json.loads(configcontent)
        isdebug = config["IsDeBug"] == "True"
        self.__class__.IsDeBug = isdebug
        self.__class__.DownConfigPath = config["DownConfigPath"]
        databasepath = config["DatabasePath"]
        self.__class__.DatabasePath = databasepath
        self.__class__.DownPath = config["DownPath"]
        # 利用数据库字符串构造engine, echo为True将打印所有的sql语句, 其他数据库的链接方式可自行百度
        # engine = sqlalchemy.create_engine("mysql+pymysql://username:password@hostname/dbname",
        # encoding="utf8", echo=True)
        # 利用Session对象连接数据库
        #engine = sqlalchemy.create_engine(dblink.linkstr(), encoding=dblink.charset, echo=isdebug)
        engine = sqlalchemy.create_engine("sqlite:///%s" % (databasepath), echo=isdebug)
        self.engine = engine # 引擎
        dbsessinon = sqlalchemy.orm.sessionmaker(bind=engine)   # 创建会话类
        self.session = dbsessinon()  # 创建会话对象
