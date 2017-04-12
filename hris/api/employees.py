from hris.utils import hash_password, gen_access_token, decode_access_token
from flask import request, abort, jsonify, g
from functools import wraps

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session
from hris import engine

#auth
from hris.api.auth import can_edit_permit
###
from hris.models import (
    User, 
    CompanyDetail,
    Branch,
    EmployeeCategoryRank,
    EmployeeCategory,
    EmployeeType,
    Employee,
    EmployeeExtra,
    Qualification,
    Certification,
    Training
)


from hris.api.response_envelop import (
    records_json_envelop,
    record_exists_envelop,
    record_json_envelop,
    record_created_envelop,
    record_notfound_envelop,
    record_updated_envelop,
    record_not_updated_env,
    fatal_error_envelop,
    missing_keys_envelop, 
    length_require_envelop
)


@api.route('/employees', methods=['POST'])
@can_edit_permit
def create_employee():
    if not request.json:
        abort(400)
    
    req_fields = {'first_name',
                  'last_name', 
                  'sex', 
                  'address_one', 
                  'age', 
                  'retirement_age', 
                  'employee_type_id', 
                  'employee_category_id',
                  'date_of_birth',
                  'address_one',
                  'employement_number',
                  'employee_branch_id'}
    result = req_fields  - request.json.keys()

    #if there is some value then abort
    if result:
        abort(401)
    
    #if everything is included, check to see if there is any empty values
    if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
        abort(411)
    
    #now clean up the data to insert into database(onyl for strin)
    data = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}

    #now try to insert 
    try:
        print(data)
        emp = Employee(**data)
        db_session.add(emp)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

    

@api.route('/employees/<int:id>', methods=['PUT'])
@can_edit_permit
def update_employee(id):
    '''This i iwill user the raw sql query because this would be easier to reason about'''

    if not request.json:
        abort(400)
    
    if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
        abort(411)
    
    #clean up the data
    data = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}

    #prepate the sql query
    inner = ', '.join('{} = {!r}'.format(key, val) for key, val in data.items())
    query = '''UPDATE employees SET {}, updated_at=Now() where id={}'''.format(inner, id)

    #try to executre
    with engine.connect() as con:
        try:
            con.execute(query)
        except IntegrityError as e:
            return record_exists_envelop()
        except Exception as e:
            return fatal_error_envelop()
        else:
            return record_updated_envelop(request.json)



@api.route('/employees', methods=['GET'])
@can_edit_permit
def get_employees():
    try:
        employees = db_session.query(Employee).all()
        emps = ({ 'first_name' : emp.first_name if emp.first_name else '',
                  'middle_name' : emp.middle_name if emp.middle_name else '',
                  'last_name' : emp.last_name if emp.last_name else '',
                  'sex' : emp.sex if emp.sex else '',
                  'date_of_birth' : str(emp.date_of_birth) if emp.date_of_birth else '',
                  'address_one' : emp.address_one if emp.address_one else '',
                  'address_two' : emp.address_two if emp.address_two else '',
                  'village' : emp.village if emp.village else '',
                  'llg' : emp.llg if emp.llg else '',
                  'district' : emp.district if emp.district else '',
                  'province' : emp.province if emp.province else '',
                  'region' : emp.region if emp.region else '',
                  'country' : emp.country if emp.country else '',
                  'email_address' : emp.email_address if emp.email_address else '',
                  'contact_number' : emp.contact_number if emp.contact_number else '',
                  'alt_contact_number' : emp.alt_contact_number if emp.alt_contact_number else '',
                  'age' : emp.age if emp.age else '',
                  'retirement_age' : emp.retirement_age if emp.retirement_age else '',
                  'employement_number' : emp.employement_number if emp.employement_number else '',
                  'salary_step' : emp.salary_step if emp.salary_step else '',
                  'date_of_commencement' : emp.date_of_commencement if emp.date_of_commencement else '',
                  'contract_end_date' : emp.contract_end_date if emp.contract_end_date else ''
                                    

        } for emp in employees)
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(emps))


    
    

    


