from airead.models import User, UserSubscribe, AdminUser, \
        FeedArticle, FeedSite
from airead.app import db
from flask.ext import admin
from flask.ext.admin.contrib import sqlamodel


def init_admin(app):
    _admin = admin.Admin(app)
    _admin.add_view(sqlamodel.ModelView(User, db.session))
    _admin.add_view(sqlamodel.ModelView(AdminUser, db.session))
    _admin.add_view(sqlamodel.ModelView(UserSubscribe, db.session))
    _admin.add_view(sqlamodel.ModelView(FeedArticle, db.session))
    _admin.add_view(sqlamodel.ModelView(FeedSite, db.session))
