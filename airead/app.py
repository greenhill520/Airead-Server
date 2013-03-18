from flask import Flask
from airead.database import db
from airead.models import User

def init_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    db.app = app

    return app

def create_adminuser(app):
    admin = User(username=app.config['ADMIN_NAME'],
            email=app.config['ADMIN_EMAIL'],
            password=app.config['ADMIN_PASSWORD'])
    db.session.add(admin)
    db.session.commit()
