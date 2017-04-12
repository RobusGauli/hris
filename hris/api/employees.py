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


@api.route('/empcategoryranks', methods=['POST'])
@can_edit_permit
def create_emp_cat_ranks():
    if not request.json:
        abort(400)
    if not 'name' in request.json.keys():
        abort(401)
    
    if len(request.json['name'].strip()) < 2:
        abort(411)
    

    #if everything is fine
    name = request.json['name'].lower().strip()
    display_name = request.json['name']

    #put to db
    try:
        rank = EmployeeCategoryRank(name=name, display_name=display_name)
        db_session.add(rank)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)


@api.route('/empcategoryranks', methods=['GET'])
@can_edit_permit
def get_emp_cat_ranks():

    try:
        ranks = db_session.query(EmployeeCategoryRank).order_by(EmployeeCategoryRank.name).all()
        ranks = (dict(id=rank.id,
                      name = rank.display_name) for rank in ranks)
    except ResultNotFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(ranks))



#@api.route('')
