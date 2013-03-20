from airead.database import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return "<User %s>" % self.username

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def change_password(self, new_password):
        self.password = generate_password_hash(new_password)
        db.session.commit()

    def subscribe(self, site):
        subscribed = UserSubscribe.query.filter_by(user=self, site=site).all()
        if len(subscribed) == 0: # user has not subscribed this site yet
            new_sub = UserSubscribe(self, site)
            db.session.add(new_sub)
            db.session.commit()


class UserSubscribe(db.Model):

    __tablename__ = 'usersubscribe'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    site = db.Column(db.Integer, db.ForeignKey('feedsite.id'), nullable=False)

    def __init__(self, user, site):
        self.user = user
        self.site = site
