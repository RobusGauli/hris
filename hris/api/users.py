from hris.utils import hash_password, gen_access_token, decode_access_token, can_edit_permit
from flask import request, abort, jsonify, g
from functools import wraps

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session
from hris.models import (
    User, 
    CompanyDetail
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


@api.route('/users', methods=['POST'])
def register_user():
    '''This view register the user by generating ht access token with the given role'''
    if request.args and request.args['action'] == 'register':
    
    #check if all key existst
        if not set(request.json.keys()) == {'user_name', 'password', 'role_id'}:
            return jsonify({'message' : 'missing keys'})
    
    #lower case the user_name
        if any(len(val.strip()) < 5 for val in request.json.values() if isinstance(val, str)):
            return jsonify({'message' : 'Not adequate length of values'})

    #lower case the user_name
        user_name = request.json['user_name'].strip().lower()
        role_id = request.json['role_id']
        hashed_pass = hash_password(request.json['password'].encode())
    #get the user access_token
        user_access_token = gen_access_token(role_id, user_name)
        user = User(user_name=user_name, password=hashed_pass, role_id=role_id, access_token=user_access_token.decode('utf-8'))
        try:
            db_session.add(user)

            db_session.commit()
        except IntegrityError as ie:
        #hadle the error here
            return record_exists_envelop()
        

        else:
            return jsonify({'message' : 'user_added_successfully', 'access_token' : user_access_token.decode('utf-8')})

    elif request.args['action'] == 'login':
        if not set(request.json.keys()) == {'user_name', 'password'}:
            return jsonify({'message' : 'missing keys'})
        user_name = request.json['user_name']
        password = request.json['password']

        #now hass the password
        hashed_pass = hash_password(password)
        
        #get the user from the users for the password and user name
        try:
            user = db_session.query(User).filter(User.user_name==user_name).filter(User.password==hashed_pass).one()
            print(user.password == hashed_pass)
            print(user)
            return record_json_envelop({'access_token' : user.access_token})
        except NoResultFound as e:
            return record_notfound_envelop('User doesn\'t exists')


@api.route('/company', methods=['POST'])
@can_edit_permit
def add_company_detail():

    if not set(request.json.keys()) == {'name', 'currency_symbol', 'is_prefix', 'country', 'description'}:
        return missing_keys_envelop()
    if len(request.json['name']) < 4 or len(request.json['country']) < 3 or len(request.json['currency_symbol']) < 1: 
        return length_require_envelop()
    
    #now shape up the fields
    name = request.json['name'].strip()
    currency_symbol = request.json['currency_symbol'].lower().strip()
    is_prefix = request.json['is_prefix']
    country = request.json['country'].strip()
    des = request.json['description'].strip()

    company = CompanyDetail(name=name, currency_symbol=currency_symbol, is_prefix=is_prefix, country=country, description=des)



    try:
        db_session.add(company)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    else:
        return record_created_envelop(request.json)




    

    
    
