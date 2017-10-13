"""Config仓库"""
from Store.RepositoryBase import RepositoryBase
from Store.Entity.Config import Config
from Store.Entity.Url import Url


class UrlRepository(RepositoryBase):
    """Config仓库"""
    def add(self, key, ruleno, filepath, sourceurl, resulturl):
        """新增：key值,下层处理规则，文件保存地址，请求地址，处理之后的结果地址"""
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

    def getsbykeyrequesturl(self, key, requesturl):
        """根据key和请求url查询未删除的"""
        entities = self.session.query(Url).join(
            Config, Config.key == key).filter(
                Url.delflag == False, Url.resulturl == requesturl)
        return entities

    def endbyrequesturl(self, requesturl):
        """根据请求路径结束"""
        url = self.session.query(Url).filter(Url.resulturl == requesturl)
        if url:
            url.update({
                Url.isend:True
            })
            self.session.commit()
