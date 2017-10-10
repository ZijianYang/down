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
        self.session.query(Config).filter(Config.id == configid).update({
            Config.content:
            content
        })

    def gets(self):
        """查询所有未删除的"""
        entities = self.session.query(Config).filter(Config.delflag == False)
        return entities

    def getbyisend(self, isend=False):
        """根据是否结束查询且未删除"""
        entities = self.session.query(Config).filter(
            Config.isend == isend).filter(Config.delflag == False)
        return entities

    def getbykey(self, key):
        """关键字查询最近的"""
        entities = self.session.query(Config).filter(
            Config.key == key).order_by(Config.adddate.desc())
        return entities
