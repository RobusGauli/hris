from sqlalchemy import Column, String, Date, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    dob = Column(Date)
    created_at = Column(DateTime)
engine = create_engine('postgres://user:postgres@localhost:5432/ff')
Base.metadata.create_all(engine)

