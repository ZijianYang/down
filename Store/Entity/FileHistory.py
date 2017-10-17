"""文件历史(FileHistory)"""
import sqlalchemy
import Tool
from Store.Entity.EntityBase import EntityBase


class FileHistory(EntityBase):
    """文件历史(FileHistory)"""
    __tablename__ = "FileHistory"  # 表名
    __table_args__ = {
        "mysql_engine": "InnoDB",  # 表的引擎
        "mysql_charset": "utf8",  # 表的编码格式
    }

    id = sqlalchemy.Column(
        "id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    delflag = sqlalchemy.Column("delflag", sqlalchemy.Boolean, default=False)
    adddate = sqlalchemy.Column("adddate", sqlalchemy.DateTime, nullable=False)
    # 表结构,具体更多的数据类型自行百度
    filepath = sqlalchemy.Column("filepath", sqlalchemy.Text, nullable=False)
    md5 = sqlalchemy.Column("md5", sqlalchemy.String(50), nullable=False)


    # 添加关系属性,UrlDetail的urlid外键属性上
    # urldetails = sqlalchemy.orm.relationship("UrlDeatil", foreign_keys="UrlDeatil.urlid")
    # 连续使用有定义顺序问题

    def __init__(self, filepath, md5=""):
        """构造函数"""
        self.adddate = Tool.Time.timeobj()
        self.filepath = filepath
        if md5 == "":
            self.md5 = Tool.FileHelper.md5frompath(filepath)
        else:
            self.md5 = md5

    def __str__(self):
        return 'Url,filepath:%s; md5:%s;' % (self.filepath, self.md5)

    __repr__ = __str__
