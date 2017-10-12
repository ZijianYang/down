"""链接(Url)"""
import sqlalchemy
import Tool.Time
from Store.Entity.EntityBase import EntityBase
import Store.Entity.Config
import Store.Entity.UrlDetail



class Url(EntityBase):
    """链接(Url)"""
    __tablename__ = "Url"  # 表名
    __table_args__ = {
        "mysql_engine": "InnoDB",  # 表的引擎
        "mysql_charset": "utf8",  # 表的编码格式
    }

    id = sqlalchemy.Column(
        "id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    delflag = sqlalchemy.Column("delflag", sqlalchemy.Boolean, default=False)
    adddate = sqlalchemy.Column("adddate", sqlalchemy.DateTime, nullable=False)
    # 表结构,具体更多的数据类型自行百度
    ruleno = sqlalchemy.Column("ruleno", sqlalchemy.String(50), nullable=False)
    sourceUrl = sqlalchemy.Column("sourceUrl", sqlalchemy.Text, nullable=False)
    resultUrl = sqlalchemy.Column("resultUrl", sqlalchemy.Text, nullable=False)
    filepath = sqlalchemy.Column("filepath", sqlalchemy.Text, nullable=False)
    isend = sqlalchemy.Column("isend", sqlalchemy.Boolean, default=False)
    # 添加外键,关联到表
    configid = sqlalchemy.Column("configid", sqlalchemy.Integer, sqlalchemy.ForeignKey("Config.id"))
    # 添加关系属性,关联到本实例的configid外键属性上
    config = sqlalchemy.orm.relationship("Config", foreign_keys="Url.configid")
    
    # 添加关系属性,UrlDetail的urlid外键属性上
    #urldetails = sqlalchemy.orm.relationship("UrlDeatil", foreign_keys="UrlDeatil.urlid")

    def __init__(self, key, rooturl, content):
        self.key = key

    def __str__(self):
        return 'Url,key:%s;ruleno:%s; sourceUrl:%s; resultUrl:%s ,filepath:%s ,isend:%s' % (
            self.config.key, self.ruleno, self.sourceUrl, self.resultUrl, self.filepath, self.isend)

    __repr__ = __str__
