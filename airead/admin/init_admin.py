from airead.app import db
from airead.models import User, UserSubscribe, AdminUser, \
        FeedArticle, FeedSite
from flask.ext import admin, wtf, login
from flask.ext.admin.contrib import sqlamodel
from flask import flash, redirect, url_for, request, render_template
from flask.ext.admin.babel import gettext

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
        user = db.session.query(AdminUser).filter_by(username=self.username.data).first()
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
            return self.render("airead_admin/admin_index.html");
        else:
            return redirect(url_for('.login'))
    @admin.expose("/login/", methods=("GET", "POST"))
    def login(self):
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = form.get_user()
            if user is None:
                flash('Invalid user')
                return render_template('airead_admin/admin_login.html', form=form)
            if not user.check_password(form.password.data):
                flash('Invalid password')
                return render_template('airead_admin/admin_login.html', form=form)
            login.login_user(user, remember=True)
            return redirect(url_for('.index'))

        return render_template('airead_admin/admin_login.html', form=form)

    @admin.expose("/logout/")
    def logout(self):
        login.logout_user()
        return redirect(url_for('.login'))
