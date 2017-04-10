import os

from flask import Flask 


#exception
#########
from psycopg2 import IntegrityError

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
##########

from config import config

#flask extension
#start the engine
engine = create_engine('postgres://user:postgres@localhost:5432/second')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def shutdown_session(exception=None):
    print('Session closed')
    db_session.remove()

#import models so that they are registered with SQLalchemy
from hris import models


def create_app(config_name=None, main=True):
    if config_name is None:
        config_name = os.environ.get('FLACK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    #regster the teardown context function
    app.teardown_appcontext(shutdown_session)

    from hris.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    #initialize flask extensio
    
    return app


def init_db():
    from hris import models
    Base.metadata.create_all(engine)