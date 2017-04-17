from hris.utils import hash_password, gen_access_token, decode_access_token
from flask import request, abort, jsonify, g
from functools import wraps

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session

#auth
from hris.api.auth import can_edit_permit, permitted_to, only_admin
###
from hris.models import (
    User, 
    CompanyDetail,
    Branch
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

@api.route('/branches', methods=['POST'])
@only_admin
def create_branch():
    if not request.json:
        abort(400)
    
    if not set(request.json.keys()) == {'is_branch',
                                        'facility_name',
                                        'facility_type_id',
                                        'llg_id', 
                                        'district_id', 
                                        'province_id', 
                                        'region_id'}:
        abort(401)
    #try to store the branch

    #make sure all the fields are non-empty
    if any(len(str(val).strip()) == 0 for val in request.json.values()):
        abort(411)
    
    #clean up the json values
    is_branch = request.json['is_branch']
    facility_name = request.json['facility_name'].strip()
    facility_type_id = request.json['facility_type_id']
    llg_id = request.json['llg_id']
    district_id = request.json['district_id']
    province_id = request.json['province_id']
    region_id = request.json['region_id']
    ##

    try:
        branch = Branch(is_branch=is_branch,
                        facility_name=facility_name, 
                        llg_id=llg_id,
                        district_id=district_id,
                        province_id=province_id,
                        region_id=region_id,
                        facility_type_id=facility_type_id)
        db_session.add(branch)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        abort(500)
    else:
        return record_created_envelop(request.json)
    



@api.route('/branches', methods=['GET'])
def get_branches():
    try:
        branches = db_session.query(Branch).filter(Branch.is_branch==True).order_by(Branch.facility_name).all()
        all_branches = (dict(id=branch.id,
                             facility_name=branch.facility_name,
                             llg=branch.llg.name,
                             district=branch.district.name,
                             province=branch.province.name,
                             region=branch.region.name,
                             facility_type=branch.facility_type.name) for branch in branches)
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(all_branches))



@api.route('/agencies', methods=['GET'])
def get_agencies():
    try:
        branches = db_session.query(Branch).filter(Branch.is_branch==False).order_by(Branch.facility_name).all()
        all_branches = (dict(id=branch.id,
                             facility_name=branch.facility_name,
                             llg=branch.llg.display_name,
                             district=branch.district.display_name,
                             province=branch.province.display_name,
                             region=branch.region.display_name,
                             facility_type=branch.facility_type.display_name) for branch in branches)
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(all_branches))


    




