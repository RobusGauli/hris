from hris.utils import hash_password, gen_access_token, decode_access_token
from flask import request, abort, jsonify, g
from functools import wraps

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session

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

    
    

    
    

    


