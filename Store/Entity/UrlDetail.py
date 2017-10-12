"""链接详情(UrlDetail)"""
import sqlalchemy
import Tool.Time
from Store.Entity.EntityBase import EntityBase
import Store.Entity.Config
import Store.Entity.Url


class UrlDetail(EntityBase):
    """链接详情(UrlDetail)"""
    __tablename__ = "UrlDetail"  # 表名
    __table_args__ = {
        "mysql_engine": "InnoDB",  # 表的引擎
        "mysql_charset": "utf8",  # 表的编码格式
    }

    id = sqlalchemy.Column(
        "id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    delflag = sqlalchemy.Column("delflag", sqlalchemy.Boolean, default=False)
    adddate = sqlalchemy.Column("adddate", sqlalchemy.DateTime, nullable=False)
    # 表结构,具体更多的数据类型自行百度
    key = sqlalchemy.Column("key", sqlalchemy.String(50), nullable=False)
    content = sqlalchemy.Column(
        "content", sqlalchemy.String(250), nullable=False)
    # 添加外键,关联到表
    #urlid = sqlalchemy.Column("urlid", sqlalchemy.Integer, sqlalchemy.ForeignKey("Url.id"))
    # 添加关系属性,urlid
    #url = sqlalchemy.orm.relationship("UrlDetail", foreign_keys="UrlDetail.urlid")    

    def __init__(self, key, rooturl, content):
        self.key = key
        self.rooturl = rooturl
        self.content = content
        self.adddate = Tool.Time.timeobj()

    def __str__(self):
        return 'UrlDetail,key:%s; rooturl:%s; content:%s ,adddate:%s ,isend:%s' % (
            self.key, self.rooturl, self.content, self.adddate, self.isend)

    __repr__ = __str__
