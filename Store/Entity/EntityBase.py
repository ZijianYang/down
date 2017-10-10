"""模型基类"""
import sqlalchemy

# 首先需要生成一个BaseModel类,作为所有模型类的基类
EntityBase = sqlalchemy.ext.declarative.declarative_base()
