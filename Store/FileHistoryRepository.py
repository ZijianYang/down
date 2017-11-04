"""FileHistory仓库"""
from Store.RepositoryBase import RepositoryBase
from Store.Entity.FileHistory import FileHistory
from Store.Entity.UrlDetail import UrlDetail
from Store.Entity.Url import Url
import sqlalchemy


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
            FileHistory.md5 == md5)
        urldetails = self.session.query(UrlDetail).join(
            Url, UrlDetail.urlid == Url.id).filter(Url.md5 == md5)
        scoredetail = urldetails.filter(UrlDetail.key == "Score").first()
        score = scoredetail.content if scoredetail else None
        tagsdetail = urldetails.filter(UrlDetail.key == "Tags").first()
        tags = tagsdetail.content if tagsdetail else None
        print("%s,%s" % (score, tags))
        if filehistory and (score or tags):
            filehistory.update({
                FileHistory.remark1: score,
                FileHistory.remark2: tags
            })
            self.session.commit()
            return True
        else:
            return False

    def getsremarknull(self, index, size):
        """查询备注为null的filehistory"""
        entities = self.session.query(FileHistory).filter(
            sqlalchemy.or_(FileHistory.remark1 == None, FileHistory.remark2 ==
                           None, FileHistory.remark3 == None))
        star = index*size
        end = (index+1)*size
        total = entities.count()
        #print("%s,%s" % (star, end))
        items = entities[star:end]
        return {"total":total, "list":items}
