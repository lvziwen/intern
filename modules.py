#! coding: utf8

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('mysql://root:lvziwen0201@localhost/GDou?charset=utf8', echo=True)
Session = sessionmaker(bind=engine)


class Student(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    gender = Column(Integer)
    age = Column(Integer)
    phone = Column(String(11))
    password = Column(String(64))
    email = Column(String(64))
    qq_num = Column(String(32))
    school = Column(String(64))
    academy = Column(String(64))
    sign_up_time = Column(Integer)
