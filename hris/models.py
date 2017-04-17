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

    #one to one with employees
    employee = relationship('Employee', uselist=False, back_populates='user')

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_type = Column(String, unique=True, nullable=False)
    permission_one = Column(Boolean, default=False) #user can edit, insert the database (do the main settings)

    permission_two = Column(Boolean, default=False) # user can edit, delete the data of branches (can view all the branches and agencies employees and data)
    permission_three = Column(Boolean, default=False) # User can edit , delete the data for agencies(can view all the agencies employees and data)

    permission_four = Column(Boolean, default=False) #user can only view all the employees of his/her own agency

    permission_five = Column(Boolean, default=False) # user can view all the employees of agencies
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(20))
    updated_by = Column(String(20))
    #relationship
    users = relationship('User', back_populates='role', cascade = 'all, delete, delete-orphan')

    def to_dict(self):
        role = {
            'role_type' : self.role_type if self.role_type else '',
            'permission_one' : self.permision_one if self.permission_one else False,
            'permission_two' : self.permission_two if self.permission_two else False,
            'permission_three' : self.permission_three if self.permission_three else False,
            'permission_four' : self.permission_four if self.permission_four else False,
            'permission_five' : self.permission_five if self.permission_five else False,
            'id' : self.id 
        }
        return role


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

    #realiationhsip
    employees = relationship('Employee', back_populates='employee_branch', cascade='all, delete, delete-orphan')




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
    sex = Column(Enum('M', 'F', 'O', name='sex'), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address_one = Column(String(50), nullable=False)
    address_two = Column(String(50))
    village = Column(String(100))
    llg = Column(String(100))
    district = Column(String(100))
    province = Column(String(100))
    region = Column(String(100))
    country = Column(String(40))
    email_address = Column(String(100), unique=True)
    contact_number = Column(String(20), unique=True)
    alt_contact_number = Column(String(20), unique=True)
    age = Column(Integer, nullable=False)
    retirement_age = Column(Integer, nullable=False, default=50)

    employement_number = Column(Integer, unique=True)
    salary_step = Column(String(6))
    date_of_commencement = Column(Date)
    contract_end_date = Column(Date)

    #about del flag
    del_flag = Column(Boolean, default=False)


    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(50))
    updated_by = Column(String(50))
    photo = Column(String(500), unique=True)
    document = Column(String(500), unique=True)

    #branch_id_of_employee
    employee_branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    #relationship
    employee_branch = relationship('Branch', back_populates='employees')

    employee_type_id = Column(Integer, ForeignKey('emp_types.id'), nullable=False)
    employee_category_id = Column(Integer, ForeignKey('emp_categories.id'), nullable=False)

    #one to one with users table
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    user = relationship('User', back_populates='employee')

    #one to one with employeeextra table
    employee_extra = relationship('EmployeeExtra', uselist=False, back_populates='employee')

    #relationship 
    employee_type = relationship('EmployeeType', back_populates='employees')
    employee_category = relationship('EmployeeCategory', back_populates='employees')
    
    #other relationship
    qualifications = relationship('Qualification', back_populates='employee', cascade='all, delete, delete-orphan')
    certifications = relationship('Certification', back_populates='employee', cascade='all, delete, delete-orphan')
    trainings = relationship('Training', back_populates='employee', cascade='all, delete, delete-orphan')


class EmployeeExtra(Base):
    __tablename__ = 'employee_extra'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), unique=True)

    ref_name = Column(String(40))
    ref_address = Column(String(40))
    ref_contact_number = Column(String(20))
    emp_father_name = Column(String(40))
    emp_mother_name = Column(String(40))
    emp_single = Column(Boolean, default=True)
    emp_wife_name = Column(String(40))
    emp_num_of_children = Column(Integer)

    #relationship
    employee = relationship('Employee', back_populates='employee_extra')

class Qualification(Base):
    __tablename__ = 'qualifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60))
    institute_name = Column(String(100))
    city = Column(String(30))
    state = Column(String(30))
    province = Column(String(30))
    country = Column(String(40))
    start_date = Column(Date)
    end_date = Column(Date)

    employee_id = Column(Integer, ForeignKey('employees.id'))
    #relationship
    employee = relationship('Employee', back_populates='qualifications')


class Certification(Base):
    __tablename__ = 'certifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    registration_number = Column(String(40), nullable=False, unique=True)
    regulatory_body = Column(String(40), nullable=False)
    registration_type = Column(String(40))
    last_renewal_date = Column(Date)
    expiry_date = Column(Date)
    
    employee_id = Column(Integer, ForeignKey('employees.id'))
    #relationship
    employee = relationship('Employee', back_populates='certifications')


class Training(Base):
    __tablename__ = 'trainings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    organiser_name = Column(String(200))
    funding_source = Column(String(200))
    duration = Column(String(30))
    institue = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    province = Column(String(50))
    country = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)

    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship('Employee', back_populates='trainings')


