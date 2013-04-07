from airead.app import db
from airead.models import User, UserSubscribe, AdminUser, \
        FeedArticle, FeedSite
from airead.feeds import CannotGetFeedSite, get_feed_link
from flask.ext import admin, wtf, login
from flask.ext.admin.contrib import sqlamodel
from flask import flash, redirect, url_for, request, render_template
from flask.ext.admin.babel import gettext  as _
from sqlalchemy.sql.expression import desc

class MyModelView(sqlamodel.ModelView):
    column_display_pk=True
    can_create = False
    can_edit = False
    can_delete = False
    column_auto_select_related = True

    def is_accessible(self):
        return login.current_user.is_authenticated()


class UserModelView(MyModelView):
    column_searchable_list = ('username',  ) 
    column_display_all_relations = True


class FeedArticleModelView(MyModelView):
    column_exclude_list = ('content', )
    column_searchable_list = ('title',  )
    column_filters = ('updated', 'title', 'site')

class UserSubscribeModelView(MyModelView):
    column_filters = ('user', 'site')
    can_delete = True

class FeedSiteModelView(MyModelView):
    column_searchable_list = ('url',  'title', )
    can_create = True
    can_edit = True
    can_delete = True
    form_excluded_columns = ('title', 'updated', 'articles', 'subscribed_num')
    #column_display_all_relations = True

    def create_model(self, form):
        #super(FeedSiteModelView, self).create_model(form)
        url = form.data['url']
        if FeedSite.query.filter_by(url=url).count() > 0:
            flash(_('site %s was existed' % url), 'error')
            return False
        try:
            feed_link = get_feed_link(url)
            if feed_link is None:
                raise CannotGetFeedSite(url)
            feed_site = FeedSite(url=feed_link)
            db.session.add(feed_site)
            db.session.commit()
        except CannotGetFeedSite, e:
            flash(_(e.msg), 'error')
            return False
        except:
            flash(_('Unknown Error'), 'error')
            return False
        return True


def init_admin(app):
    init_login(app);
    _admin = admin.Admin(app, name=app.config['ADMIN_VIEW_NAME'],
            index_view=RequireLoginView())
    #_admin.add_view(RequireLoginView())
    _admin.add_view(UserModelView(User, db.session))
    #_admin.add_view(MyModelView(AdminUser, db.session))
    _admin.add_view(UserSubscribeModelView(UserSubscribe, db.session))
    _admin.add_view(FeedArticleModelView(FeedArticle, db.session))
    _admin.add_view(FeedSiteModelView(FeedSite, db.session))


# login 
class LoginForm(wtf.Form):
    username = wtf.TextField(validators=[wtf.required()])
    password = wtf.PasswordField(validators=[wtf.required()])

    def get_user(self):
        user = db.session.query(AdminUser).filter_by(
                username=self.username.data.strip()).first()
        return user

def init_login(app):
    login_manager = login.LoginManager()
    login_manager.setup_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

class RequireLoginView(admin.AdminIndexView):
    @admin.expose("/")
    def index(self):
        if login.current_user.is_authenticated():
            feed_site_num = db.session.query(FeedSite).count()
            user_num = db.session.query(User).count()
            article_num = db.session.query(FeedArticle).count()
            sites = db.session.query(FeedSite).order_by(desc(FeedSite.subscribed_num)).all()
            if len(sites) > 10: # top 10 popular sites
                sites = sites[:10]
            return self.render("airead_admin/admin_index.html",
                    feed_site_num=feed_site_num, user_num=user_num,
                    article_num=article_num, sites=sites);
        else:
            print "redirect to login"
            return redirect(url_for('.login'))
    @admin.expose("/login/", methods=("GET", "POST"))
    def login(self):
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = form.get_user()
            if user is None:
                flash(_('Invalid user'))
                return render_template('airead_admin/admin_login.html', form=form)
            if not user.check_password(form.password.data):
                flash(_('Invalid password'))
                return render_template('airead_admin/admin_login.html', form=form)
            login.login_user(user, remember=True)
            return redirect(url_for('.index'))
        return render_template('airead_admin/admin_login.html', form=form)

    @admin.expose("/logout/")
    def logout(self):
        login.logout_user()
        return redirect(url_for('.login'))
