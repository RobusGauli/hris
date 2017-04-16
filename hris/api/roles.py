'''This module is responsbile for creating roles and assigning different permissions to the roles'''
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

@api.route('/roles', methods = ['POST'])
@can_edit_permit
def create_roles():
    '''This method will create a role and assign diffenet permissions'''

    return 'yeah roles must be created'