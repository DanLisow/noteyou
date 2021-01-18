from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    create_engine
)
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

engine = create_engine('mysql+mysqlconnector://testuser:ZXCv!@#4@db/testdb')
Session = sessionmaker()
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True)
    login = Column(Text)
    password = Column(Text)

    def __repr__(self):
        return "<User('%s','%s')>" % (self.login, self.password)


class Notes(Base):
    __tablename__ = 'notes'

    id_note = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id_user'))
    text = Column(Text)

    def __repr__(self):
        return self.text
