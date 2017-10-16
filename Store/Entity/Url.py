"""链接(Url)"""
import sqlalchemy
import Tool
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
    sourceurl = sqlalchemy.Column("sourceurl", sqlalchemy.Text, nullable=False)
    resulturl = sqlalchemy.Column("resulturl", sqlalchemy.Text, nullable=False)
    filepath = sqlalchemy.Column("filepath", sqlalchemy.Text, nullable=False)
    md5 = sqlalchemy.Column("md5", sqlalchemy.String(50), nullable=False)
    isend = sqlalchemy.Column("isend", sqlalchemy.Boolean, default=False)
    # 添加外键,关联到表
    configid = sqlalchemy.Column("configid", sqlalchemy.Integer, sqlalchemy.ForeignKey("Config.id"))
    # 添加关系属性,关联到本实例的configid外键属性上
    config = sqlalchemy.orm.relationship("Config", foreign_keys="Url.configid")

    # 添加关系属性,UrlDetail的urlid外键属性上
    # urldetails = sqlalchemy.orm.relationship("UrlDeatil", foreign_keys="UrlDeatil.urlid")
    # 连续使用有定义顺序问题

    def __init__(self, ruleno, filepath, sourceurl, resulturl, md5=""):
        """构造函数"""
        self.adddate = Tool.Time.timeobj()
        self.ruleno = ruleno
        self.filepath = filepath
        if md5 == "":
            self.md5 = Tool.FileHelper.md5frompath(filepath)
        self.sourceurl = sourceurl
        #self.configid = configid
        self.resulturl = resulturl

    def __str__(self):
        return 'Url,ruleno:%s; sourceurl:%s; resulturl:%s ,filepath:%s ,isend:%s' % (
            self.ruleno, self.sourceurl, self.resulturl, self.filepath, self.isend)

    __repr__ = __str__
