from airead.app import db
from airead.models import User, UserSubscribe, AdminUser, \
        FeedArticle, FeedSite
from flask.ext import admin, wtf
from flask.ext.admin.contrib import sqlamodel
from flask import flash
from flask.ext.admin.babel import gettext

class MyModelView(sqlamodel.ModelView):
    column_display_pk=True
    can_create = False
    can_edit = False
    can_delete = False
    column_auto_select_related = True

class UserModelView(MyModelView):
    column_searchable_list = ('username',  ) 
    column_display_all_relations = True


class FeedArticleModelView(MyModelView):
    column_exclude_list = ('content', )
    column_searchable_list = ('title',  )
    column_filters = ('updated', 'title', 'site')

class UserSubscribeModelView(MyModelView):
    column_filters = ('user', 'site')

class FeedSiteModelView(MyModelView):
    column_searchable_list = ('url',  'title', )
    can_create = True
    can_edit = True
    can_delete = True
    form_excluded_columns = ('title', 'updated', 'articles')

    def create_model(self, form):
        #super(FeedSiteModelView, self).create_model(form)
        url = form.data['url']
        if FeedSite.query.filter_by(url=url).count() > 0:
            flash(gettext('site %s was existed' % url), 'error')
            return False
        feed_site = FeedSite(url=url)
        db.session.add(feed_site)
        db.session.commit()
        return True


def init_admin(app):
    _admin = admin.Admin(app, name=app.config['ADMIN_VIEW_NAME'])
    _admin.add_view(UserModelView(User, db.session))
    #_admin.add_view(MyModelView(AdminUser, db.session))
    _admin.add_view(UserSubscribeModelView(UserSubscribe, db.session))
    _admin.add_view(FeedArticleModelView(FeedArticle, db.session))
    _admin.add_view(FeedSiteModelView(FeedSite, db.session))
