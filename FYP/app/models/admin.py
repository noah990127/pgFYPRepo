from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base


class Admin(Base):
    id = Column(Integer, primary_key=True, autoincrement=True) # id自增长
    name = Column(String(15), nullable=False)
    _password = Column('password', String(12))

    def __init__(self, id, name, password):
        super(Admin,self).__init__()
        self.id = id
        self.name = name
        self._password = password