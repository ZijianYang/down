"""FileHistory仓库"""
from Store.RepositoryBase import RepositoryBase
from Store.Entity.FileHistory import FileHistory


class FileHistoryRepository(RepositoryBase):
    """FileHistory仓库仓库"""

    def add(self, filehistory):
        """新增：如果已存在则不加"""
        entity = self.session.query(FileHistory).filter(FileHistory.md5 == filehistory.md5).first()
        if not entity:
            self.session.add(filehistory)
            self.session.commit()
            return True
        else:
            return False

    def getbymd5(self, md5):
        """根据md5查询"""
        entity = self.session.query(FileHistory).filter(FileHistory.md5 == md5).first()
        return entity
