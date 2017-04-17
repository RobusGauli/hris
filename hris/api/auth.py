from flask import request, jsonify
from functools import wraps
from hris.utils import decode_access_token

from hris.api.response_envelop import unauthorized_envelop
from hris import db_session
from hris import ROLES_PERMISSION

#auth

###
from hris.models import (
    User, 
    CompanyDetail,
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

def permitted_to(p_list=None):
    def deco(func):
        @wraps(func)
        def perm_wrapper(*args, **kwargs):
            if not 'Token' in request.headers.keys():
                return unauthorized_envelop()
            try:
                decoded = decode_access_token(request.headers['token'])
            except Exception:
                return unauthorized_envelop()
            else:
                role_id = decoded['role_id']
            
            role = db_session.query(Role).filter(Role.id==role_id).one()
            role = role.to_dict()
            permissions = (role['permission_one'],
                           role['permission_two'],
                           role['permission_three'],
                           role['permission_four'],
                           role['permission_five'])
            print(permissions) 

            #if everythin went well check the permissions

            return func(*args, **kwargs)
        return perm_wrapper
    return deco



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
            raise 
        else:
            role_id = decoded['role_id']
            
            #for admin role,'permission one' must be true
            if not ROLES_PERMISSION[role_id]['permission_one'] == True:
                return unauthorized_envelop()
            return func(*args, **kwargs)
    return admin_wrapper
            
