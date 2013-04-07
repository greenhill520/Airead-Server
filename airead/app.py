from flask import Flask
from airead.database import db
from airead.models import User, AdminUser
from airead.logger import init_logger, init_timer_log
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

def init_schedule_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    db.app = app
    init_timer_log(app)

    return app


def create_adminuser(app):
    admin = AdminUser(username=app.config['ADMIN_NAME'],
            password=app.config['ADMIN_PASSWORD'])
    db.session.add(admin)
    db.session.commit()
    app.logger.info('create admin %s' % app.config['ADMIN_NAME'])

app = init_app()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

