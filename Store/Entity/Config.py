"""配置(Config)"""
import sqlalchemy
import Tool.Time
from Store.Entity.EntityBase import EntityBase


class Config(EntityBase):
    """配置(Config)"""
    __tablename__ = "Config"  # 表名
    __table_args__ = {
        "mysql_engine": "InnoDB",  # 表的引擎
        "mysql_charset": "utf8",  # 表的编码格式
    }

    id = sqlalchemy.Column(
        "id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    delflag = sqlalchemy.Column("delflag", sqlalchemy.Boolean, default=False)
    # 表结构,具体更多的数据类型自行百度
    key = sqlalchemy.Column("key", sqlalchemy.String(50), nullable=False)
    rooturl = sqlalchemy.Column(
        "rooturl", sqlalchemy.String(500), nullable=False)
    content = sqlalchemy.Column(
        "content", sqlalchemy.String(250), nullable=False)
    adddate = sqlalchemy.Column("adddate", sqlalchemy.DateTime, nullable=False)
    isend = sqlalchemy.Column("isend", sqlalchemy.Boolean, default=False)

    def __init__(self, key, rooturl, content):
        self.key = key
        self.rooturl = rooturl
        self.content = content
        self.adddate = Tool.Time.timeobj()

    def __str__(self):
        return 'Config,key:%s; rooturl:%s; content:%s ,adddate:%s ,isend:%s' % (
            self.key, self.rooturl, self.content, self.adddate, self.isend)

    __repr__ = __str__
