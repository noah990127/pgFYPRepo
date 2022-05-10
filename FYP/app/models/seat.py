from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base


class Seat(Base):
    sID = Column(Integer, primary_key=True, autoincrement=True) # id自增长
    status = Column(Integer, nullable=False) 
    floor = Column(Integer, nullable=False) 

