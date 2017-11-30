"""链接(Url)"""
import sqlalchemy
import Tool
from Store.Entity.EntityBase import EntityBase
import Store.Entity.Config
import Store.Entity.UrlDetail



class Tag(EntityBase):
    """标签(Tag)"""
    __tablename__ = "Tag"  # 表名
    __table_args__ = {
        "mysql_engine": "InnoDB",  # 表的引擎
        "mysql_charset": "utf8",  # 表的编码格式
    }

    id = sqlalchemy.Column(
        "id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    delflag = sqlalchemy.Column("delflag", sqlalchemy.Boolean, default=False)
    adddate = sqlalchemy.Column("adddate", sqlalchemy.DateTime, nullable=False)
    # 表结构,具体更多的数据类型自行百度
    tag = sqlalchemy.Column("tag", sqlalchemy.String(50), nullable=False)
    count = sqlalchemy.Column("count", sqlalchemy.Integer, nullable=False)

    def __init__(self, tag, count=0):
        """构造函数"""
        self.adddate = Tool.Time.timeobj()
        self.tag = tag
        self.count = count

    def __str__(self):
        return 'tag,tag:%s; count:%s; ' % (
            self.tag, self.count)

    __repr__ = __str__
