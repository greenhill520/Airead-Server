from airead.database import db
from user import User

import datetime

class FeedSite(db.Model):

    __tablename__ = 'feedsite'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(120), nullable=False)
    title = db.Column(db.Unicode(120), nullable=False, unique=True)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow,
            nullable=False)
    articles = db.relationship('FeedArticle', backref='feedsite',
            lazy='dynamic')

    def __init__(self, url, title, updated):
        self.url = url
        self.title = title
        self.updated = updated

    def __repr__(self):
        return "<FeedSite %s>" % self.title


class FeedArticle(db.Model):

    __tablename__ = 'feedarticle'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('feedsite.id'))
    link = db.Column(db.Text, nullable=False)
    title = db.Column(db.UnicodeText, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow,
            nullable=False)
    content = db.Column(db.UnicodeText, nullable=False)

    def __init__(self, site_id, link, title, updated, content):
        self.site_id = site_id
        self.link = link
        self.title = title
        self.updated = updated
        self.content = content

    def __repr__(self):
        return "<FeedArticle %s>" % self.title
