from sqlalchemy import Column, String, Integer, DateTime, orm
from app.models.base import Base

class Order(Base):
	recordID = Column(Integer, primary_key=True, autoincrement=True) # id自增长
	stuID = Column(Integer, nullable=False)
	sID = Column(Integer, nullable=False)
	time = Column(DateTime, nullable=True)
	status = Column(Integer, nullable=False)