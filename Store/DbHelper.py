import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
import Store
import Store.Entity
import Tool.Time
from AppConfig import AppConfig



def delete():
    """初始化库"""
    appconfig = AppConfig()
    import Store.Entity
    # 删除所有表
    Store.Entity.EntityBase.metadata.drop_all(appconfig.engine)
    appconfig.session.close()

def init():    
    """初始化库"""
    appconfig = AppConfig()
    import Store.Entity
    # 创建所有表,如果表已经存在,则不会创建
    Store.Entity.EntityBase.metadata.create_all(appconfig.engine)
    appconfig.session.close()


def seed():
    """初始化数据"""
    try:
        session = AppConfig().session
        # 清空数据,不需要commit操作
        session.query(Store.Entity.Config).filter(Store.Entity.Config.id != -1).delete()
        # 删除数据的另外一种形式:session.delete()

        # 插入数据,这里的一个实例只插入一次,第二次插入不生效
        session.add(Store.Entity.Config(key="First", content="student1", rooturl="1.jpg" ,adddate=Tool.Time.timeobj()))
        session.commit()
    except Exception as excep:
        print(excep)
        session.rollback()
        raise
    session.close()
