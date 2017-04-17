from hris.utils import hash_password, gen_access_token, decode_access_token
from flask import request, abort, jsonify, g
from functools import wraps

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session

#auth
from hris.api.auth import can_edit_permit, only_admin
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
@only_admin
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
@only_admin
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

@api.route('/empcategoryranks/<int:id>', methods=['PUT'])
@only_admin
def update_rank(id):
    if not request.json:
        abort(400)
    
    if 'name' not in request.json.keys():
        abort(401)
    
    #now try to update the facilty name
    name = request.json['name'].lower().strip()
    display_name = request.json['name'].strip()

    try:
        rank = db_session.query(EmployeeCategoryRank).filter(EmployeeCategoryRank.id==id).one()
        rank.name = name
        rank.display_name = display_name
        db_session.add(rank)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        
        abort(500)

    else:
        return record_updated_envelop(request.json)


@api.route('/empcategoryranks/<int:rank_id>/empcategories', methods=['POST'])
@only_admin
def create_emp_cat(rank_id):
    if not request.json:
        abort(400)
    if not 'name' in request.json.keys():
        abort(401)
    
    if len(request.json['name'].strip()) < 2:
        abort(411)
    
    #strip down the values
    display_name = request.json['name'].strip()
    name = display_name.lower()
    emp_cat_rank_id = rank_id

    #try to put onto database
    try:
        cat = EmployeeCategory(name=name, display_name=display_name, emp_cat_rank_id=emp_cat_rank_id)
        db_session.add(cat)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)


@api.route('/empcategories', methods=['GET'])
@only_admin
def get_emp_categories():

    try:
        ranks = db_session.query(EmployeeCategory).order_by(EmployeeCategory.name).all()
        rks = (dict(id=rank.id, name=rank.display_name, emp_cat_rank=rank.emp_cat_rank.name, emp_cat_rank_id=rank.emp_cat_rank.id)
                                                                          for rank in ranks)
    except ResultNotFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(rks))
        

@api.route('/empcategories/<int:id>', methods=['PUT'])
@only_admin
def update_emp_category(id):
    if not request.json:
        abort(400)
    
    name = request.json.get('name', None)
    emp_cat_rank_id  = request.json.get('emp_cat_rank_id', None)
    
    #now try to update the facilty name
    if name is not None:
        name = request.json['name'].lower().strip()
        display_name = request.json['name'].strip()
    
    try:
        cat = db_session.query(EmployeeCategory).filter(EmployeeCategory.id==id).one()
        if name is not None:
            cat.name = name
            cat.display_name = display_name
        if emp_cat_rank_id is not None:
            cat.emp_cat_rank_id = emp_cat_rank_id    
        db_session.add(cat)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        
        abort(500)
    else:
        return record_updated_envelop(request.json)



@api.route('/employeetypes', methods=['POST'])
@only_admin
def create_employee_type():

    if not request.json:
        abort(400)
    
    if not 'name' in request.json.keys():
        abort(401)
    
    if len(request.json['name'].strip()) < 2:
        abort(411)
    
    #clear up the values
    display_name = request.json['name'].strip()
    name = display_name.lower()

    try:
        e_type = EmployeeType(name=name, display_name=display_name)
        db_session.add(e_type)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json) 
    

@api.route('/employeetypes', methods=['GET'])
@only_admin
def get_employee_types():

    try:
        types = db_session.query(EmployeeType).all()
        tys = (dict(id=ty.id, name=ty.display_name) for ty in types)
    except ResultNotFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(tys))
    


@api.route('/employeetypes/<int:id>', methods=['PUT'])
@only_admin
def update_emp_type(id):
    if not request.json:
        abort(400)
    
    name = request.json.get('name', None)
    
    
    #now try to update the facilty name
    if name is not None:
        name = request.json['name'].lower().strip()
        display_name = request.json['name'].strip()
    
    try:
        typ = db_session.query(EmployeeType).filter(EmployeeType.id==id).one()
        if name is not None:
            typ.name = name
            typ.display_name = display_name
          
        db_session.add(typ)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        
        abort(500)
    else:
        return record_updated_envelop(request.json)