"""Image仓库"""
from Store.RepositoryBase import RepositoryBase
from Store.Entity.Config import Config


class ConfigRepository(RepositoryBase):
    """Config仓库"""

    def add(self, config):
        """新增"""
        entity = self.session.query(Config).filter(Config.key == config.key).first()
        if not entity:
            self.session.add(config)
            self.session.commit()
            return entity

    def adds(self, configs):
        """批量新增"""
        entities = []
        for config in configs:
            entity = self.add(config)
            if entity:
                entities.append(entity)
        self.session.commit()
        return entities

    def updatecontent(self, content, key):
        """更新内容"""
        # 使用update方法
        entity = self.session.query(Config).filter(Config.key == key)
        if entity:
            entity.update({
                Config.content:
                content
            })
            self.session.commit()
            return entity.first()

    def updates(self, configs):
        """批量更新"""
        entities = []
        for config in configs:
            entity = self.updatecontent(config.content, config.key)
            if entity:
                entities.append(entity)
        self.session.commit()
        return entities

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
        return entities.first()

    def deletebykey(self, key):
        """根据key删除"""
        entity = self.session.query(Config).filter(
            Config.key == key)
        if entity:
            entity.update({Config.delflag:True})
            return entity.first()
