"""Config仓库"""
from Store.RepositoryBase import RepositoryBase
from Store.Entity.Config import Config
from Store.Entity.Url import Url


class UrlRepository(RepositoryBase):
    """Config仓库"""
    def add(self, key, ruleno, filepath, sourceurl, resulturl):
        """新增"""
        config = self.session.query(Config).filter(Config.key == key).first()
        url = Url(ruleno, filepath, sourceurl, resulturl, config.id)
        self.session.add(url)
        self.session.commit()
        return url

    def deletebykey(self, key):
        """根据key删除url,返回删除数量"""
        entities = self.session.query(Url).join(Config,
                                                Config.key == key).filter(
                                                    Url.delflag == False)
        total = entities.count()
        entities.delete()
        return total

    def getsnoendbykey(self, key):
        """根据编号查询未结束未删除且不为终止规则的url"""
        entities = self.session.query(Url).join(
            Config, Config.key == key).filter(
                Url.delflag == False, Url.isend == False, Url.ruleno != "End")
        return entities

    def getsbykeyrequesturl(self, key, requestUrl):
        """根据key和请求url查询"""
        entities = self.session.query(Url).join(
            Config, Config.key == key).filter(
                Url.delflag == False, Url.isend == False, Url.resultUrl == requestUrl)
        return entities
