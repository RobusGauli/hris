from sqlalchemy import (
    Column, 
    String, 
    Integer,
    ForeignKey,
    Text, 
    Enum, 
    CheckConstraint, 
    DateTime,
    func, 
    Date,
    Float,
    Boolean
)

#default
#onupdate


from psycopg2 import IntegrityError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence

from hris import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(20), nullable=False, unique=True)
    password = Column(String, nullable=False)
    access_token = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(20))
    updated_by = Column(String(20))
    role_id  = Column(Integer, ForeignKey('roles.id'))
    activate = Column(Boolean, default=False)
    #employee_id


    #relationship
    role = relationship('Role', back_populates='users')

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_type = Column(String, unique=True, nullable=False)
    permission_one = Column(Boolean, default=False)
    permission_two = Column(Boolean, default=False)
    permission_three = Column(Boolean, default=False)
    permission_four = Column(Boolean, default=False)
    permission_five = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(20))
    updated_by = Column(String(20))
    #relationship
    users = relationship('User', back_populates='role', cascade = 'all, delete, delete-orphan')


class CompanyDetail(Base):
    __tablename__ = 'companydetail'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)
    description = Column(String(300))
    currency_symbol = Column(String(2), unique=True)
    is_prefix = Column(Boolean, default=False)
    country = Column(String(30), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Branch(Base):
    __tablename__ = 'branches'

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_branch = Column(Boolean, default=False)
    facility_name = Column(String(40), nullable=False, unique=True)
    #foreignt keys
    facility_type_id = Column(Integer, ForeignKey('facilitytypes.id'))
    llg_id = Column(Integer, ForeignKey('llg.id'))
    district_id = Column(Integer, ForeignKey('districts.id'))
    province_id = Column(Integer, ForeignKey('provinces.id'))
    region_id = Column(Integer, ForeignKey('regions.id'))

    #relationship
    facility_type = relationship('FacilityType', back_populates='branches')
    llg = relationship('LLG', back_populates='branches')
    district = relationship('District', back_populates='branches')
    province = relationship('Province', back_populates='branches')
    region = relationship('Region', back_populates='branches')



class FacilityType(Base):
    __tablename__ = 'facilitytypes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=True, nullable=False)
    display_name = Column(String(200), nullable=False)

    branches = relationship('Branch', back_populates='facility_type', cascade='all, delete, delete-orphan')



class LLG(Base):
    __tablename__ = 'llg'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200))
    branches = relationship('Branch', back_populates='llg', cascade='all, delete, delete-orphan')



class District(Base):
    __tablename__ = 'districts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200))
    branches = relationship('Branch', back_populates='district', cascade='all, delete, delete-orphan')

class Province(Base):
    __tablename__ = 'provinces'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200))
    branches = relationship('Branch', back_populates='province', cascade='all, delete, delete-orphan')

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200))
    branches = relationship('Branch', back_populates='region', cascade='all, delete, delete-orphan')




#create an engine



