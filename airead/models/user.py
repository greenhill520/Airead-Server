from airead.database import db
from werkzeug import generate_password_hash, check_password_hash
from feed import FeedSite
from flask import current_app as app

import md5

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self._gen_password(password) 
        app.logger.info("add a new user %s" % self.username)

    def __repr__(self):
        return "<User %s>" % self.username

    def check_password(self, password):
        if self.password is None:
            return False
        mdpwd = md5.md5(password).hexdigest()
        if mdpwd == self.password:
            return True
        else:
            return False

    def check_hash_password(self, hash_password):
        if self.password == hash_password:
            return True
        return False

    def change_password(self, new_password):
        self.password = self._gen_password(new_password) 
        db.session.commit()

    def _gen_password(self, raw_pwd):
        pwd = md5.md5(raw_pwd)
        return pwd.hexdigest()

    def subscribe(self, site):
        subscribed = UserSubscribe.query.filter_by(user=self, site=site).all()
        if len(subscribed) == 0: # user has not subscribed this site yet
            new_sub = UserSubscribe(self, site)
            db.session.add(new_sub)
            db.session.commit()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

# not a good choice
class UserSubscribe(db.Model):

    __tablename__ = 'usersubscribe'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',
        ondelete='CASCADE'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('feedsite.id',
        ondelete='CASCADE'), nullable=False)
    user = db.relationship("User", innerjoin=True, lazy="joined",
            backref=db.backref('usersubscribe', cascade="all,delete"))
    site = db.relationship("FeedSite", innerjoin=True, lazy="joined",
            backref=db.backref('usersubscribe', cascade="all,delete"))

    def __init__(self, *args, **kwargs):
        super(UserSubscribe, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<User %s subscribed %s>" % (self.user.username,
                self.site.title)
    
    def __unicode__(self):
        return "<%s>" % (self.site.title)

    @classmethod
    def subscribe(cls, user_id, feedsite_id):
        if UserSubscribe.query.filter_by(user_id=user_id,
                site_id=feedsite_id).count() > 0: # already subscribed
            return
        user_subscribe = UserSubscribe(user_id=user_id, site_id=feedsite_id)
        db.session.add(user_subscribe)
        db.session.commit()
        feedsite = FeedSite.query.get(feedsite_id)
        feedsite.subscribed_num = feedsite.subscribed_num + 1
        db.session.add(feedsite)
        db.session.commit()

    @classmethod
    def unsubscribe(cls, user_id, feedsite_id):
        user_subscribe = UserSubscribe.query.filter_by(user_id=user_id,
                site_id=feedsite_id).first()
        if user_subscribe is not None:
            db.session.delete(user_subscribe)
            db.session.commit()
            feedsite = FeedSite.query.get(feedsite_id)
            feedsite.subscribed_num = feedsite.subscribed_num - 1
            db.session.add(feedsite)
            db.session.commit()

class AdminUser(db.Model):

    __tablename__ = 'adminuser'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False) 

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def __repr__(self):
        return "<Admin %s>" % self.username

    def __unicode__(self):
        return self.username

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
