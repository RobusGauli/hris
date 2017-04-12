from flask import Blueprint

api = Blueprint('api', __name__)

from hris.api import users, locations, branches, employees
