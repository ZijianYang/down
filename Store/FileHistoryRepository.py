"""FileHistory仓库"""
from Store.RepositoryBase import RepositoryBase
from Store.Entity.FileHistory import FileHistory
from Store.Entity.UrlDetail import UrlDetail
from Store.Entity.Url import Url


class FileHistoryRepository(RepositoryBase):
    """FileHistory仓库仓库"""

    def add(self, filehistory):
        """新增：如果已存在则不加"""
        entity = self.session.query(FileHistory).filter(
            FileHistory.md5 == filehistory.md5).first()
        if not entity:
            self.session.add(filehistory)
            self.session.commit()
            return True
        else:
            return False

    def getbymd5(self, md5):
        """根据md5查询"""
        entity = self.session.query(FileHistory).filter(
            FileHistory.md5 == md5).first()
        return entity

    def setremarkbymd5(self, md5):
        """根据md5设置remark"""
        filehistory = self.session.query(FileHistory).filter(
            FileHistory.md5 == md5).first()
        urldetails = self.session.query(UrlDetail).join(
            Url, UrlDetail.urlid == Url.id).filter(Url.md5 == md5)
        score = urldetails.filter(UrlDetail.key == "score").first().value
        tags = urldetails.filter(UrlDetail.key == "tags").first().value
        filehistory.update({
            FileHistory.remark1: score,
            FileHistory.remark2: tags
        })
        self.session.commit()
