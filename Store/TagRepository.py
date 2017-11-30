"""Url仓库"""
from Store.RepositoryBase import RepositoryBase
from Store.Entity.Config import Config
from Store.Entity.Tag import Tag
import sqlalchemy


class TagRepository(RepositoryBase):
    """Url仓库"""

    def addorupdate(self, tag):
        """新增"""
        entities = self.session.query(Tag).filter(Tag.tag == tag)
        if entities and entities.count() > 0:
            entities.update({Tag.count: entities.first().count + 1})
        else:
            entity = Tag(tag, 1)
            self.session.add(entity)
        self.session.commit()

    def gets(self, tag, count=10):
        """根据内容查询"""
        entities = self.session.query(Tag).filter(Tag.tag.like(
            tag + '%')).order_by(sqlalchemy.desc(Tag.count)).limit(count)
        return entities
