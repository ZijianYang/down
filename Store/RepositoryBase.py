"""仓库基类"""
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
from AppConfig import AppConfig





class RepositoryBase(object):
    """仓库基类"""

    def __init__(self):
        """"会话对象"""
        self.session = AppConfig().Session
