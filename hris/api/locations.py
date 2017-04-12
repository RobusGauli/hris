from hris.utils import hash_password, gen_access_token, decode_access_token
from flask import request, abort, jsonify, g
from functools import wraps

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session

#auth
from hris.api.auth import can_edit_permit

from hris.models import (
    FacilityType,
    LLG,
    District,
    Province,
    Region
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


@api.route('/facilities', methods=['POST'])
@can_edit_permit
def create_facility():
    if not set(request.json.keys()) == {'name'}:
        return jsonify({'message' : 'missing keys'})
    
    if not len(request.json['name']) > 3:
        return jsonify({'message' : 'not adequate lenght'})
    
    #lower case the facility name
    display_name = request.json['name'].strip()
    name = request.json['name'].lower().strip()

    #insert into the database
    try:
        fac = FacilityType(name=name, display_name=display_name)
        db_session.add(fac)
        db_session.commit()
    except IntegrityError as ie:
        return record_exists_envelop()
    
    else:
        return record_created_envelop(request.json)



@api.route('/districts', methods=['POST'])
@can_edit_permit
def create_district():
    if not set(request.json.keys()) == {'name'}:
        return jsonify({'message' : 'missing keys'})
    
    if not len(request.json['name']) > 3:
        return jsonify({'message' : 'not adequate lenght'})
    
    #lower case the facility name
    display_name = request.json['name'].strip()
    name = request.json['name'].lower().strip()

    #insert into the database
    try:
        dis = District(name=name, display_name=display_name)
        db_session.add(dis)
        db_session.commit()
    except IntegrityError as ie:
        return record_exists_envelop()
    
    else:
        return record_created_envelop(request.json)


@api.route('/llg', methods=['POST'])
@can_edit_permit
def create_llg():
    if not set(request.json.keys()) == {'name'}:
        return jsonify({'message' : 'missing keys'})
    
    if not len(request.json['name']) > 3:
        return jsonify({'message' : 'not adequate lenght'})
    
    #lower case the facility name
    display_name = request.json['name'].strip()
    name = request.json['name'].lower().strip()

    #insert into the database
    try:
        dis = LLG(name=name, display_name=display_name)
        db_session.add(dis)
        db_session.commit()
    except IntegrityError as ie:
        return record_exists_envelop()
    
    else:
        return record_created_envelop(request.json)


@api.route('/provinces', methods=['POST'])
@can_edit_permit
def create_province():
    if not set(request.json.keys()) == {'name'}:
        return jsonify({'message' : 'missing keys'})
    
    if not len(request.json['name']) > 3:
        return jsonify({'message' : 'not adequate lenght'})
    
    #lower case the facility name
    display_name = request.json['name'].strip()
    name = request.json['name'].lower().strip()

    #insert into the database
    try:
        dis = Province(name=name, display_name=display_name)
        db_session.add(dis)
        db_session.commit()
    except IntegrityError as ie:
        return record_exists_envelop()
    
    else:
        return record_created_envelop(request.json)

@api.route('/regions', methods=['POST'])
@can_edit_permit
def create_region():
    if not set(request.json.keys()) == {'name'}:
        return jsonify({'message' : 'missing keys'})
    
    if not len(request.json['name']) > 3:
        return jsonify({'message' : 'not adequate length'})
    
    #lower case the facility name
    display_name = request.json['name'].strip()
    name = request.json['name'].lower().strip()

    #insert into the database
    try:
        dis = Region(name=name, display_name=display_name)
        db_session.add(dis)
        db_session.commit()
    except IntegrityError as ie:
        return record_exists_envelop()
    
    else:
        return record_created_envelop(request.json)
    

#...........................>#


@api.route('/facilities', methods=['GET'])
@can_edit_permit
def get_facilities():
    
    try:
        facilities = db_session.query(FacilityType).order_by(FacilityType.name).all()
        gen_exp = (dict(name = f.name, id=f.id) for f in facilities)
        return records_json_envelop(list(gen_exp))
    except Exception as e:
        return fatal_error_envelop()

@api.route('/llg', methods=['GET'])
@can_edit_permit
def get_llg():
    
    try:
        llgs = db_session.query(LLG).order_by(LLG.name).all()
        gen_exp = (dict(name = f.name, id=f.id) for f in llgs)
        return records_json_envelop(list(gen_exp))
    except Exception as e:
        return fatal_error_envelop()


@api.route('/districts', methods=['GET'])
@can_edit_permit
def get_districts():
    
    try:
        districts = db_session.query(District).order_by(District.name).all()
        gen_exp = (dict(name = f.name, id=f.id) for f in districts)
        return records_json_envelop(list(gen_exp))
    except Exception as e:
        return fatal_error_envelop()

@api.route('/provinces', methods=['GET'])
@can_edit_permit
def get_provinces():
    
    try:
        provinces = db_session.query(Province).order_by(Province.name).all()
        gen_exp = (dict(name = f.name, id=f.id) for f in provinces)
        return records_json_envelop(list(gen_exp))
    except Exception as e:
        return fatal_error_envelop()


@api.route('/regions', methods=['GET'])
@can_edit_permit
def get_regions():
    
    try:
        provinces = db_session.query(Region).order_by(Region.name).all()
        gen_exp = (dict(name = f.name, id=f.id) for f in provinces)
        return records_json_envelop(list(gen_exp))
    except Exception as e:
        return fatal_error_envelop()
#..............................
    

@api.route('/facilities/<int:id>', methods=['PUT'])
@can_edit_permit
def update_facility(id):
    if not request.json:
        abort(400)
    
    if 'name' not in request.json.keys():
        abort(401)
    
    #now try to update the facilty name
    name = request.json['name'].lower().strip()
    display_name = request.json['name'].strip()

    try:
        facility = db_session.query(FacilityType).filter(FacilityType.id==id).one()
        facility.name = name
        facility.display_name = display_name
        db_session.add(facility)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
         
        abort(500)
    else:
        return record_updated_envelop(request.json)


@api.route('/llg/<int:id>', methods=['PUT'])
@can_edit_permit
def update_llg(id):
    if not request.json:
        abort(400)
    
    if 'name' not in request.json.keys():
        abort(401)
    
    #now try to update the facilty name
    name = request.json['name'].lower().strip()
    display_name = request.json['name'].strip()

    try:
        facility = db_session.query(LLG).filter(LLG.id==id).one()
        facility.name = name
        facility.display_name = display_name
        db_session.add(facility)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        
        abort(500)
    else:
        return record_updated_envelop(request.json)


@api.route('/districts/<int:id>', methods=['PUT'])
@can_edit_permit
def update_district(id):
    if not request.json:
        abort(400)
    
    if 'name' not in request.json.keys():
        abort(401)
    
    #now try to update the facilty name
    name = request.json['name'].lower().strip()
    display_name = request.json['name'].strip()

    try:
        facility = db_session.query(District).filter(District.id==id).one()
        facility.name = name
        facility.display_name = display_name
        db_session.add(facility)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        abort(500)
    else:
        return record_updated_envelop(request.json)

    

@api.route('/provinces/<int:id>', methods=['PUT'])
@can_edit_permit
def update_province(id):
    if not request.json:
        abort(400)
    
    if 'name' not in request.json.keys():
        abort(401)
    
    #now try to update the facilty name
    name = request.json['name'].lower().strip()
    display_name = request.json['name'].strip()

    try:
        facility = db_session.query(Province).filter(Province.id==id).one()
        facility.name = name
        facility.display_name = display_name
        db_session.add(facility)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
         
        abort(500)
    else:
        return record_updated_envelop(request.json)

    
@api.route('/regions/<int:id>', methods=['PUT'])
@can_edit_permit
def update_region(id):
    if not request.json:
        abort(400)
    
    if 'name' not in request.json.keys():
        abort(401)
    
    #now try to update the facilty name
    name = request.json['name'].lower().strip()
    display_name = request.json['name'].strip()

    try:
        facility = db_session.query(Region).filter(Region.id==id).one()
        facility.name = name
        facility.display_name = display_name
        db_session.add(facility)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        
        abort(500)
    else:
        return record_updated_envelop(request.json)

    


    




@api.errorhandler(400)
def badrequest(error):
    return jsonify({'message' : 'Bad request'}), 400

@api.errorhandler(401)
def missingkeys(error):
    return jsonify({'message': 'Missing keys'}), 401

@api.errorhandler(404)
def notfound(error):
    return record_notfound_envelop(), 404

@api.errorhandler(500)
def servererror(error):
    return fatal_error_envelop(), 500

@api.errorhandler(411)
def lengthrequired(error):
    return length_require_envelop(), 411 

