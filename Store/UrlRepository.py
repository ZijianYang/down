"""Url仓库"""
from Store.RepositoryBase import RepositoryBase
from Store.Entity.Config import Config
from Store.Entity.Url import Url


class UrlRepository(RepositoryBase):
    """Url仓库"""

    def add(self, key, url):
        """新增：key值,下层处理规则，文件保存地址，请求地址，处理之后的结果地址"""
        config = self.session.query(Config).filter(Config.key == key).first()
        url.configid = config.id
        self.session.add(url)
        self.session.commit()
        return url

    def deletebykey(self, key):
        """根据key删除url,返回删除数量"""
        entities = self.session.query(Url).join(
            Config, Config.id == Url.configid).filter(Config.key == key,
                                                      Url.delflag == False)
        for entityjoin in entities:
            entity = self.session.query(Url).filter(
                Url.id == entityjoin.id)
            entity.delete()
        return entities.count()

    def getsnoendbynorulenokey(self, key, ruleno, count=100):
        """根据编号查询未结束未删除且不为某个规则的url,默认前100条"""
        entities = self.session.query(Url).join(
            Config, Config.id == Url.configid).filter(
                Config.key == key, Url.delflag == False, Url.isend == False,
                Url.ruleno != ruleno).order_by(Url.id).limit(count)
        return entities

    def getsbykeyrequesturl(self, key, requesturl):
        """根据key和请求url查询未删除的"""
        entities = self.session.query(Url).join(
            Config, Config.id == Url.configid).filter(
                Config.key == key, Url.sourceurl == requesturl,
                Url.delflag == False)
        return entities

    def endbyrequesturl(self, requesturl):
        """根据请求路径结束"""
        url = self.session.query(Url).filter(Url.resulturl == requesturl)
        if url:
            url.update({Url.isend: True})
            self.session.commit()
