from flask.ext.script import Manager
from flask import current_app as app
from airead.models import User, UserSubscribe, FeedArticle, FeedSite, AdminUser
from airead.database import db
from airead import init_app, create_adminuser

manager = Manager(init_app)

@manager.command
def createdb():
    db.create_all()

@manager.command
def createadmin():
    create_adminuser(app) 

@manager.command
def dropdb():
    db.drop_all()

@manager.shell
def make_shell():
    return dict(app=app, 
            db=db,
            User=User,
            UserSubscribe=UserSubscribe,
            FeedArticle=FeedArticle,
            FeedSite=FeedSite,
            AdminUser=AdminUser,
            use_bpython=True)

@manager.command
def runserver():
    app.run(port=8080)

@manager.command
def create_test_data():
    test_user = User("text", "text@text.com", "123123")
    site = FeedSite("http://mindhacks.cn/")
    db.session.add(test_user)
    db.session.add(site)
    db.session.commit()
    UserSubscribe.subscribe(test_user.id, site.id)

@manager.command
def create_all_data():
    createdb()
    createadmin()
    create_test_data()

if __name__ == '__main__':
    manager.run()
