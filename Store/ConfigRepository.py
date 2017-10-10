"""Image仓库"""
from Store.RepositoryBase import RepositoryBase
from Store.Entity.Config import Config


class ConfigRepository(RepositoryBase):
    """Config仓库"""

    def add(self, config):
        """新增"""
        self.session.add(config)
        self.session.commit()

    def adds(self, configs):
        """批量新增"""
        for config in configs:
            self.session.add(config)
        self.session.commit()

    def updatecontent(self, content, configid):
        """更新内容"""
        # 使用update方法
        self.session.query(Config).filter(Config.id == configid).update({Config.content:content})

    def gets(self):
        """查询所有"""
        entities = self.session.query(Config).filter(not Config.delflag)
        return entities

    def getbyisend(self, isend):
        """是否结束查询"""
        entities = self.session.query(Config).filter(isend)
        return entities

    def getbykey(self, key):
        """关键字查询"""
        entity = self.session.query(Config).filter(Config.key == key)
        return entity
