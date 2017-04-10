from flask import request, abort, jsonify, g

from hris.api import api

@api.route('/users')
def get_users():
    return 'asdd'