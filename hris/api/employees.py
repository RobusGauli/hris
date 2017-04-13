from hris.utils import hash_password, gen_access_token, decode_access_token
from flask import request, abort, jsonify, g
from functools import wraps

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session
from hris import engine

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
    length_require_envelop,
    extra_keys_envelop,
    keys_require_envelop
)


@api.route('/employees', methods=['POST'])
@can_edit_permit
def create_employee():
    if not request.json:
        abort(400)
    
    req_fields = {'first_name',
                  'last_name', 
                  'sex', 
                  'address_one', 
                  'age', 
                  'retirement_age', 
                  'employee_type_id', 
                  'employee_category_id',
                  'date_of_birth',
                  'address_one',
                  'employement_number',
                  'employee_branch_id'}
    result = req_fields  - request.json.keys()

    #if there is some value then abort
    if result:
        abort(401)
    
    #if everything is included, check to see if there is any empty values
    if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
        abort(411)
    
    #now clean up the data to insert into database(onyl for strin)
    data = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}

    #now try to insert 
    try:
        print(data)
        emp = Employee(**data)
        db_session.add(emp)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

    

@api.route('/employees/<int:id>', methods=['PUT'])
@can_edit_permit
def update_employee(id):
    '''This i iwill user the raw sql query because this would be easier to reason about'''

    if not request.json:
        abort(400)
    
    if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
        abort(411)

    if 'age' not in request.json or 'retirement_age' not in request.json:
        return jsonify({'message' : 'please send both the age and retirement_age'})
        abort(400)
    age = request.json['age']
    retirement_age = request.json['retirement_age']
    #first check about the age
    if int(age) > int(retirement_age) or int(age) < 18:
        return record_not_updated_env('Age cannot be more than retirement age or less than 18')
    
    #clean up the data
    data = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}

    #prepate the sql query
    inner = ', '.join('{} = {!r}'.format(key, val) for key, val in data.items())
    query = '''UPDATE employees SET {}, updated_at=Now() where id={}'''.format(inner, id)

    #try to executre
    with engine.connect() as con:
        try:
            con.execute(query)
        except IntegrityError as e:
            return record_exists_envelop()
        except Exception as e:
            return fatal_error_envelop()
        else:
            return record_updated_envelop(request.json)



@api.route('/employees', methods=['GET'])
@can_edit_permit
def get_employees():
    try:
        employees = db_session.query(Employee).filter(Employee.del_flag==False).all()
        emps = ({ 'first_name' : emp.first_name if emp.first_name else '',
                  'middle_name' : emp.middle_name if emp.middle_name else '',
                  'last_name' : emp.last_name if emp.last_name else '',
                  'sex' : emp.sex if emp.sex else '',
                  'date_of_birth' : str(emp.date_of_birth) if emp.date_of_birth else '',
                  'address_one' : emp.address_one if emp.address_one else '',
                  'address_two' : emp.address_two if emp.address_two else '',
                  'village' : emp.village if emp.village else '',
                  'llg' : emp.llg if emp.llg else '',
                  'district' : emp.district if emp.district else '',
                  'province' : emp.province if emp.province else '',
                  'region' : emp.region if emp.region else '',
                  'country' : emp.country if emp.country else '',
                  'email_address' : emp.email_address if emp.email_address else '',
                  'contact_number' : emp.contact_number if emp.contact_number else '',
                  'alt_contact_number' : emp.alt_contact_number if emp.alt_contact_number else '',
                  'age' : emp.age if emp.age else '',
                  'retirement_age' : emp.retirement_age if emp.retirement_age else '',
                  'employement_number' : emp.employement_number if emp.employement_number else '',
                  'salary_step' : emp.salary_step if emp.salary_step else '',
                  'date_of_commencement' : emp.date_of_commencement if emp.date_of_commencement else '',
                  'contract_end_date' : emp.contract_end_date if emp.contract_end_date else '',
                  'id' : emp.id if emp.id else ''
                                    

        } for emp in employees)
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(emps))


@api.route('/employees/<int:id>')
@can_edit_permit
def get_employee(id):
    try:
        emp  = db_session.query(Employee).filter(Employee.id==id).one()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return jsonify({ 'first_name' : emp.first_name if emp.first_name else '',
                  'middle_name' : emp.middle_name if emp.middle_name else '',
                  'last_name' : emp.last_name if emp.last_name else '',
                  'sex' : emp.sex if emp.sex else '',
                  'date_of_birth' : str(emp.date_of_birth) if emp.date_of_birth else '',
                  'address_one' : emp.address_one if emp.address_one else '',
                  'address_two' : emp.address_two if emp.address_two else '',
                  'village' : emp.village if emp.village else '',
                  'llg' : emp.llg if emp.llg else '',
                  'district' : emp.district if emp.district else '',
                  'province' : emp.province if emp.province else '',
                  'region' : emp.region if emp.region else '',
                  'country' : emp.country if emp.country else '',
                  'email_address' : emp.email_address if emp.email_address else '',
                  'contact_number' : emp.contact_number if emp.contact_number else '',
                  'alt_contact_number' : emp.alt_contact_number if emp.alt_contact_number else '',
                  'age' : emp.age if emp.age else '',
                  'retirement_age' : emp.retirement_age if emp.retirement_age else '',
                  'employement_number' : emp.employement_number if emp.employement_number else '',
                  'salary_step' : emp.salary_step if emp.salary_step else '',
                  'date_of_commencement' : emp.date_of_commencement if emp.date_of_commencement else '',
                  'contract_end_date' : emp.contract_end_date if emp.contract_end_date else '',
                  'id' : emp.id if emp.id else ''
                                    

        })


@api.route('/employees/<int:id>/qualifications', methods=['POST'])
@can_edit_permit
def create_qualification_by_emp(id):
    if not request.json:
        abort(400)
    #check if there is empty field comming up
    if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
        abort(411)
    #clean up the values
    qual = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}
    #insert
    print(id)
    try:
        print(id)
        db_session.add(Qualification(**qual, employee_id=id))
        db_session.commit()
    except IntegrityError as e:
        return fatal_error_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)


@api.route('/employees/<int:id>/qualifications', methods=['GET'])
@can_edit_permit
def get_qualifications_by_emp(id):
    try:
        qls = db_session.query(Qualification).filter(Qualification.employee_id==id).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        quals = ({
            'id' : q.id,
            'name' : q.name if q.name else '',
            'institute_name' : q.institute_name if q.institute_name else '',
            'city' : q.city if q.city else '',
            'state' : q.state if q.state else '',
            'province' : q.province if q.province else '',
            'country' : q.country if q.country else '',
            'start_date' : q.start_date if q.start_date else '',
            'end_date' : q.end_date if q.end_date else ''
        } for q in qls)
        return records_json_envelop(list(quals))


@api.route('/employees/<int:emp_id>/qualifications/<int:q_id>', methods=['PUT'])
@can_edit_permit
def update_qualification_by_emp(emp_id, q_id):
    if not request.json:
        abort(400)
    #check to see if there is any empty values
    if not all(len(str(val).strip()) for val in request.json.values()):
        abort(411)
    #check to see if the request has the right type of keys
    result = request.json.keys() - set(col.name for col in Qualification.__mapper__.columns)
    if result:
        
        return extra_keys_envelop('Keys: {!r} not accepted'.format(', '.join(r for r in result)))
    
    #clearn up the values for string
    #generator expression
    cleaned_json = ((key, val.strip()) if isinstance(val, str) else (key, val) for key, val in request.json.items())
        #this means that it has extra set of keys that is not necessary
    #make the custom query
    inner = ', '.join('{:s} = {!r}'.format(key, val) for key, val in cleaned_json)
    query = '''UPDATE qualifications SET {:s} WHERE id = {:d}'''.format(inner, q_id)
    

    #try to executre
    with engine.connect() as con:
        try:
            con.execute(query)
        except IntegrityError as e:
            return record_exists_envelop()
        except Exception as e:
            return fatal_error_envelop()
        else:
            return record_updated_envelop(request.json)

############@@@@############

@api.route('/employees/<int:id>/certifications', methods=['POST'])
@can_edit_permit
def create_certification_by_emp(id):
    if not request.json:
        abort(400)
    #check if there is empty field comming up
    if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
        abort(411)
    
    #check if there is no registration number and registration body
    result = {'regulatory_body', 'registration_number'} - request.json.keys()
    if result:
        return keys_require_envelop('"regulatory_body" and "regstration_number" is required')
    #clean up the values
    cert = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}
    #insert
    print(id)
    try:
        print(id)
        db_session.add(Certification(**cert, employee_id=id))
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

@api.route('/employees/<int:id>/certifications', methods=['GET'])
@can_edit_permit
def get_certifications_by_emp(id):
    try:
        certs = db_session.query(Certification).filter(Certification.employee_id==id).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        certs = ({
            'id' : q.id,
            'registration_number' : q.registration_number if q.registration_number else '',
            'regulatory_body' : q.regulatory_body if q.regulatory_body else '',
            'registration_type' : q.registration_type if q.registration_type else '',
            'last_renewal_date' : q.last_renewal_date if q.last_renewal_date else '',
            'expiry_date' : q.expiry_date if q.expiry_date else ''
            
        } for q in certs)
        return records_json_envelop(list(certs))


@api.route('/employees/<int:emp_id>/certifications/<int:c_id>', methods=['PUT'])
@can_edit_permit
def update_certification_by_emp(emp_id, c_id):
    if not request.json:
        abort(400)
    #check to see if there is any empty values
    if not all(len(str(val).strip()) for val in request.json.values()):
        abort(411)
    #check to see if the request has the right type of keys
    result = request.json.keys() - set(col.name for col in Certification.__mapper__.columns)
    if result:
        
        return extra_keys_envelop('Keys: {!r} not accepted'.format(', '.join(r for r in result)))
    
    #clearn up the values for string
    #generator expression
    cleaned_json = ((key, val.strip()) if isinstance(val, str) else (key, val) for key, val in request.json.items())
        #this means that it has extra set of keys that is not necessary
    #make the custom query
    inner = ', '.join('{:s} = {!r}'.format(key, val) for key, val in cleaned_json)
    query = '''UPDATE certifications SET {:s} WHERE id = {:d}'''.format(inner, c_id)
    

    #try to executre
    with engine.connect() as con:
        try:
            con.execute(query)
        except IntegrityError as e:
            return record_exists_envelop()
        except Exception as e:
            return fatal_error_envelop()
        else:
            return record_updated_envelop(request.json)


#######------------------__##########################

@api.route('/employees/<int:id>/trainings', methods=['POST'])
@can_edit_permit
def create_training_by_emp(id):
    if not request.json:
        abort(400)
    #check if there is empty field comming up
    if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
        abort(411)
    
    #check if there is no registration number and registration body
    result = {'name'} - request.json.keys()
    if result:
        return keys_require_envelop('key : "name" is required')
    #clean up the values
    trs = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}
    #insert
    print(id)
    try:
        print(id)
        db_session.add(Training(**trs, employee_id=id))
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

@api.route('/employees/<int:id>/trainings', methods=['GET'])
@can_edit_permit
def get_trainings_by_emp(id):
    try:
        trs = db_session.query(Training).filter(Training.employee_id==id).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        trs = ({
            'id' : q.id,
            'name' : q.name if q.name else '',
            'organiser_name' : q.organiser_name if q.organiser_name else '',
            'funding_source' : q.funding_source if q.funding_source else '',
            'duration' : q.duration if q.duration else '',
            'institute' : q.institue if q.institue else '',
            'duration' : q.duration if q.duration else '',
            'city' : q.city if q.city else '',
            'state' : q.state if q.state else '',
            'province' : q.province if q.province else ''            
        } for q in trs)
        return records_json_envelop(list(trs))


@api.route('/employees/<int:emp_id>/trainings/<int:t_id>', methods=['PUT'])
@can_edit_permit
def update_training_by_emp(emp_id, t_id):
    if not request.json:
        abort(400)
    #check to see if there is any empty values
    if not all(len(str(val).strip()) for val in request.json.values()):
        abort(411)
    #check to see if the request has the right type of keys
    result = request.json.keys() - set(col.name for col in Training.__mapper__.columns)
    if result:
        
        return extra_keys_envelop('Keys: {!r} not accepted'.format(', '.join(r for r in result)))
    
    #clearn up the values for string
    #generator expression
    cleaned_json = ((key, val.strip()) if isinstance(val, str) else (key, val) for key, val in request.json.items())
        #this means that it has extra set of keys that is not necessary
    #make the custom query
    inner = ', '.join('{:s} = {!r}'.format(key, val) for key, val in cleaned_json)
    query = '''UPDATE trainings SET {:s} WHERE id = {:d}'''.format(inner, t_id)
    

    #try to executre
    with engine.connect() as con:
        try:
            con.execute(query)
        except IntegrityError as e:
            return record_exists_envelop()
        except Exception as e:
            return fatal_error_envelop()
        else:
            return record_updated_envelop(request.json)
