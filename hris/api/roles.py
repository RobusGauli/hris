'''This module is responsbile for creating roles and assigning different permissions to the roles'''
from hris.utils import hash_password, gen_access_token, decode_access_token, random_string
from flask import request, abort, jsonify, g
from functools import wraps

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session, engine

#auth
from hris.api.auth import can_edit_permit
###
from hris.models import (
    User, 
    CompanyDetail, 
    Role
)
from functools import wraps

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
    length_require_envelop,
    extra_keys_envelop,
    keys_require_envelop
)


def update_query(table_name,mapping, id):
    inner = ', '.join('{:s} = {!r}'.format(key, val) for key, val in mapping)
    query = '''UPDATE {} SET {:s} where id = {:d}'''.format(table_name, inner, id)
    return query


def handle_keys_for_post_request(model, *, _exclude=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            fields_db = set(col.name for col in model.__mapper__.columns)
            if not request.json:
                abort(400)
            required_keys = fields_db - set(_exclude) if _exclude else set()
            result = request.json.keys() - required_keys
            if result:
                return extra_keys_envelop('Keys not Accepeted %r' % (', '.join(key for key in result)))
            #check if there are any missing keys
            result = required_keys - request.json.keys()
            if result:
                return keys_require_envelop('Keys required %r' %(' ,'.join(key for key  in result)))
            #check if there are any fields emopty
            if not all(len(str(val).strip()) >= 1 for val in request.json.values()):
                return length_require_envelop()
            #everythin is okay return the function
            return func(*args, **kwargs)
        return wrapper
    return decorator

def handle_keys_for_update_request(model, *, _exclude=None):
    def _decorator(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):

            fields_db = set(col.name for col in model.__mapper__.columns)
            if not request.json:
                abort(400)
            required_keys = fields_db - set(_exclude) if _exclude else set()
            result = request.json.keys() - required_keys
            if result:
                return extra_keys_envelop('Keys not Accepeted %r' % (', '.join(key for key in result)))
            #check if there are any missing keys
            
            if not all(len(str(val).strip()) >= 1 for val in request.json.values()):
                return length_require_envelop()
            #everythin is okay return the function
            return func(*args, **kwargs)
        return _wrapper
    return _decorator


@api.route('/roles', methods = ['POST'])
@handle_keys_for_post_request(Role, _exclude=('id', 'updated_at', 'updated_by', 'created_at', 'created_by'))
def create_roles():
    '''This method will create a role and assign diffenet permissions'''
    try:
         role = Role(**request.json)
         db_session.add(role)
         db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

@api.route('/roles', methods=['GET'])
def get_roles():
    try:
        roles = db_session.query(Role).filter(Role.role_type != 'admin').all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(role.to_dict() for role in roles))




@api.route('/roles/<int:r_id>', methods=['PUT'])
@handle_keys_for_update_request(Role, _exclude=('id', ))
def update_role(r_id):
    #check to see if they want to update the admin_role. refuse to change the admin_roel
    

    #clean up the json values
    cleaned_json = ((key, val.strip()) if isinstance(val, str) else (key, val) for key, val in request.json.items())

    query = update_query(Role.__tablename__, cleaned_json, r_id)

    with engine.connect() as con:
        try:
            con.execute(query)
        except IntegrityError as e:
            return record_exists_envelop()
        except Exception as e:
            return fatal_error_envelop()
        else:
            return record_updated_envelop(request.json)


