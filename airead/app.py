from flask import Flask
from airead.database import db
from airead.models import User, AdminUser
from airead.logger import init_logger
from airead.admin import init_admin
from airead.api import init_api

def init_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    db.app = app
    app.debug = app.config['DEBUG']
    
    init_logger(app)
    init_admin(app)
    init_api(app)
    return app

def create_adminuser(app):
    admin = AdminUser(username=app.config['ADMIN_NAME'],
            password=app.config['ADMIN_PASSWORD'])
    db.session.add(admin)
    db.session.commit()
    app.logger.info('create admin %s' % app.config['ADMIN_NAME'])
