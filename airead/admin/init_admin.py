from airead.models import User, UserSubscribe, AdminUser, \
        FeedArticle, FeedSite
from airead.app import db
from flask.ext import admin
from flask.ext.admin.contrib import sqlamodel

class MyModelView(sqlamodel.ModelView):
    can_edit=False
    can_create=False

def init_admin(app):
    _admin = admin.Admin(app)
    _admin.add_view(MyModelView(User, db.session))
    _admin.add_view(MyModelView(AdminUser, db.session))
    _admin.add_view(MyModelView(UserSubscribe, db.session))
    _admin.add_view(MyModelView(FeedArticle, db.session))
    _admin.add_view(MyModelView(FeedSite, db.session))
