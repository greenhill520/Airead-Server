from airead.database import db
from airead.feeds import FeedData

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

    def __init__(self, url):
        self.url = url
        feed_data = FeedData(url)
        feed_data.init_data()
        self.title =  feed_data.site_title
        self.updated = feed_data.site_updated

    def __repr__(self):
        return "<FeedSite %s>" % self.title

    def __unicode__(self):
        return "<FeedSite %s>" % self.title


class FeedArticle(db.Model):

    __tablename__ = 'feedarticle'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('feedsite.id',
        ondelete='CASCADE'))
    link = db.Column(db.Text, nullable=False)
    title = db.Column(db.UnicodeText, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow,
            nullable=False)
    content = db.Column(db.UnicodeText, nullable=False)
    site = db.relationship('FeedSite', innerjoin=True, lazy="joined")

    def __init__(self, *args, **kwargs):
        super(FeedArticle, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<FeedArticle %s>" % self.title.encode('utf8')

    def __unicode__(self):
        return "%s" % self.title
