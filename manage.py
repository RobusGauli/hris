import os
import subprocess
import sys


from flask_script import Manager, Server
from hris import create_app

manager = Manager(create_app)
manager.add_command('runserver', Server())

if __name__ == '__main__':
    manager.run()