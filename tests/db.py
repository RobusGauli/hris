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

Base = declarative_base()


#for employee
class EmployeeCategoryRank(Base):
    __tablename__ = 'emp_cat_ranks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(11), nullable=False, unique=True)
    display_name = Column(String(11), nullable=False, unique=True)

    #realtionship 
    emp_categories = relationship('EmployeeCategory', back_populates='emp_cat_rank', cascade='all, delete, delete-orphan')

class EmployeeCategory(Base):
    __tablename__ = 'emp_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    display_name = Column(String(50), nullable=False, unique=True)
    emp_cat_rank_id = Column(Integer, ForeignKey('emp_cat_ranks.id'))

    #realationship
    emp_cat_rank = relationship('EmployeeCategoryRank', back_populates='emp_categories')
    #relationship
    employees = relationship('Employee', back_populates='employee_category', cascade='all, delete, delete-orphan')


#lets hardcord the grade of the employee

class EmployeeType(Base):
    __tablename__ = 'emp_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False, unique=True)
    display_name = Column(String(30), nullable=False, unique=True)

    #relationship
    employees = relationship('Employee', back_populates='employee_type', cascade='all, delete, delete-orphan')



class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(40), nullable=False)
    middle_name = Column(String(40))
    last_name = Column(String(40), nullable=False)
    sex = Column( Enum('M', 'F', 'O', name='sex'))
    date_of_birth = Column(Date)
    village = Column(String(100))
    llg = Column(String(100))
    district = Column(String(100))
    province = Column(String(100))
    region = Column(String(100))
    country = Column(String(40))
    email_address = Column(String(100))
    contact_number = Column(String(20))

    employement_number = Column(Integer, unique=True)
    salary_step = Column(String(6))
    date_of_commencement = Column(Date)
    contract_end_date = Column(Date)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(50))
    updated_by = Column(String(50))
    photo = Column(String(500))
    document = Column(String(500))

    employee_type_id = Column(Integer, ForeignKey('emp_types.id'))
    employee_category_id = Column(Integer, ForeignKey('emp_categories.id'))

    #relationship 
    employee_type = relationship('EmployeeType', back_populates='employees')
    employee_category = relationship('EmployeeCategory', back_populates='employees')