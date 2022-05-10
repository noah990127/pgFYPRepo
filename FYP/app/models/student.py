from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base


class Student(Base):
    seq = Column(Integer, primary_key=True, autoincrement=True) # id自增长
    stuID = Column(Integer, unique = True, nullable=False) # 身份证号码
    _password = Column('password', String(12))
    name = Column(String(15), nullable=False)
    teleNum = Column(String(11), nullable=False)
    confidency = Column(Integer, nullable=False)

