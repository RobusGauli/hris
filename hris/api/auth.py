from flask import request, jsonify
from functools import wraps
from hris.utils import decode_access_token

from hris.api.response_envelop import unauthorized_envelop
from hris import db_session
from hris import ROLES_PERMISSION
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound

#auth

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
    Training,
    Role
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

def can_edit_permit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        #check if there is access_token in the headers
        if not 'Token' in request.headers.keys():
            return jsonify({'message': 'not_authorized', 'code': '401'})
        #try decoding the token
        decoded = decode_access_token(request.headers['token'])
        if not decoded:
            return jsonify({'message': 'not authorized', 'code': '401'})
        
        if decoded['role_id'] == 1:
            return func(*args, **kwargs)
        else:
            return jsonify({'message' : 'not authorized', 'code' : '401'})

    return wrapper




def only_admin(func):
    @wraps(func)
    def admin_wrapper(*args, **kwargs):
        print(request.headers)
        if  'Token' not in request.headers.keys():
            return unauthorized_envelop()
        try:
            print(request.headers)
            decoded = decode_access_token(request.headers['Token'])
            if decoded is None:
                return unauthorized_envelop()
            
        except Exception:
            return unauthorized_envelop()
        else:
            role_id = decoded['role_id']
            
            #for admin role,'permission one' must be true
            if not ROLES_PERMISSION[role_id]['permission_one'] == True:
                return unauthorized_envelop()
            return func(*args, **kwargs)
    return admin_wrapper
            



def allow_permission(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):

        if 'Token' not in request.headers.keys():
            return unauthorized_envelop()
        try:
            decoded = decode_access_token(request.headers['Token'])
            if decoded is None:
                return unauthrorized_envelop()
        except Exception as e:
            return unauthorized_envelop()
        else:
            role_id = decoded['role_id']
            user_name = decoded['user_name']

        if ROLES_PERMISSION[role_id]['permission_one'] == True:
            return func(*args, **kwargs)
        print('herer is the line that need to be called')
        #now check the employee_branch_id and know if he belongs to agency or branch
        emp_branch_id = request.json.get('employee_branch_id')
        print(emp_branch_id)
        try:
            branch = db_session.query(Branch).filter(Branch.id==emp_branch_id).one()
        except NoResultFound as e:
            return record_notfound_envelop()
        except Exception as e:
            
            return fatal_error_envelop()
        else:
            
            is_branch = branch.is_branch
            print(is_branch)
            if is_branch:
                return handle_branch(branch, emp_branch_id, role_id, user_name, func, *args, **kwargs)
            elif is_branch==False: #this means it is agency
                return handle_agency(branch, emp_branch_id, role_id, user_name, func, *args, **kwargs)
    return _wrapper



def handle_branch(branch, emp_branch_id, role_id, user_name, func, *args, **kwargs):
    print('hdnle branch callsed')
    if ROLES_PERMISSION[role_id]['permission_two'] == True:
        return func(*args, **kwargs)
    else:
        print('asdasdasdasdasdasd')
        #go ahead and check the permission that if he can edit for his/her own branch or not
        if ROLES_PERMISSION[role_id]['permission_four'] == True:
            try:
                user = db_session.query(User).filter(User.user_name==user_name).one()
                emp = user.employee
                if emp is None:
                    return unauthorized_envelop()
            except NoResultFound as e:
                return record_notfound_envelop()
            except Exception as e:
                return fatal_error_envelop()
            else:
                print('yeasdsadsad')
                employee_branch_id = emp.employee_branch_id
                print(employee_branch_id, emp_branch_id)
                if employee_branch_id == emp_branch_id:
                    print('yeahs')
                    return func(*args, **kwargs)
                else:
                    return unauthorized_envelop()
        else:
            return unauthorized_envelop()

    




def handle_agency(branch, emp_branch_id, role_id, user_name,  func, *args, **kwargs):
    if ROLES_PERMISSION[role_id]['permission_three'] == True:
        return func(*args, **kwargs)
    else:
        print('permission three is false now check permission five')
        #go ahead and check the permission that if he can edit for his/her own branch or not
        if ROLES_PERMISSION[role_id]['permission_five'] == True:
            try:
                user = db_session.query(User).filter(User.user_name==user_name).one()
                emp = user.employee
                if emp is None:
                    return unauthorized_envelop()
            except NoResultFound as e:
                return record_notfound_envelop()
            except Exception as e:
                return fatal_error_envelop()
            else:
                print('yeasdsadsad')
                employee_branch_id = emp.employee_branch_id
                print(employee_branch_id, emp_branch_id)
                if employee_branch_id == emp_branch_id:
                    print('yeahs')
                    return func(*args, **kwargs)
                else:
                    return unauthorized_envelop()
        else:
            return unauthorized_envelop()



