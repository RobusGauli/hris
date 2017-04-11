from flask import request, jsonify
from functools import wraps
from hris.utils import decode_access_token

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