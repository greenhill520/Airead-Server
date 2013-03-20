from flask import Flask
from airead.database import db
from airead.models import User
from airead.logger import init_logger

def init_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    db.app = app
    
    init_logger(app)
    return app

def create_adminuser(app):
    admin = User(username=app.config['ADMIN_NAME'],
            email=app.config['ADMIN_EMAIL'],
            password=app.config['ADMIN_PASSWORD'])
    admin.is_admin = True
    db.session.add(admin)
    db.session.commit()
