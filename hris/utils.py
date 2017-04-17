import time
import hashlib
from functools import wraps
from flask import request, jsonify



import jwt

SECRET = 'shivapandeyisverybad'

STRINGS = 'ABCSJKSHDJHG'
from random import choice

def random_string(num):
    return ''.join(choice(STRINGS) for i in range(num))
    

def timestamp():
    return int(time.time())

def hash_password(password):
    if isinstance(password, str):
        password = password.encode()
    return hashlib.sha256(password).hexdigest()
    


def gen_access_token(role_id, user_name, issuer='drose.com.np'):
    payload = {'role_id' : role_id, 'user_name': user_name, 'iss': issuer}

    encoded = jwt.encode(payload, SECRET, algorithm='HS256')
    return encoded

def decode_access_token(encoded):
    decoded = None
    try:

        decoded = jwt.decode(encoded, SECRET, algorithms=['HS256'])

    except jwt.DecodeError as e:
        pass
    else:
        return decoded

#simple decorator function to allow access to the endpoint

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



