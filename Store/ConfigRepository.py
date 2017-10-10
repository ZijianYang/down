"""Image仓库"""
import pymysql
from Store.RepositoryBase import RepositoryBase
import Store.Entity


class ConfigRepository(RepositoryBase):
    """Config仓库"""

    def gets(self):
        """获取列表"""
        configs = self.session.query(Store.Entity.Config)
        return configs
