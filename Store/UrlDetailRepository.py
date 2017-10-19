"""UrlDetail仓库"""
from Store.RepositoryBase import RepositoryBase
from Store.Entity.UrlDetail import UrlDetail
from Store.Entity.Url import Url
from Store.Entity.Config import Config


class UrlDetailRepository(RepositoryBase):
    """UrlDetail仓库"""

    def adds(self, resulturl, urldeatils):
        """新增列表"""
        for urldetail in urldeatils:
            entity = self.session.query(UrlDetail).join(
                Url, Url.id == UrlDetail.urlid).filter(
                    Url.resulturl == resulturl).filter(
                        UrlDetail.key == urldetail.key).first()
            if entity:
                entity.content = urldetail.content
            else:
                url = self.session.query(Url).filter(
                    Url.resulturl == resulturl).first()
                if url:
                    urldetail.urlid = url.id
                    self.session.add(urldetail)
        self.session.commit()
        return urldeatils

    def deletebykey(self, key):
        """根据key删除"""
        entities = self.session.query(UrlDetail).join(
            Url, UrlDetail.urlid == Url.id).join(
                Config, Url.configid == Config.id).filter(Config.key == key)
        count = entities.count()
        for entityjoin in entities:
            entity = self.session.query(UrlDetail).filter(
                UrlDetail.id == entityjoin.id)
            entity.delete()
        self.session.commit()
        return count
