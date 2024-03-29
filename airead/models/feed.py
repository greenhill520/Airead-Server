from airead.database import db
from airead.feeds import FeedData
from flask import current_app as app
from airead.feeds import get_feed_link, CannotGetFeedSite

import datetime

class FeedSite(db.Model):

    __tablename__ = 'feedsite'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(120), nullable=False)
    title = db.Column(db.Unicode(120), nullable=False, unique=True)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    articles = db.relationship('FeedArticle', backref=db.backref('feedsite',
        lazy="joined"), lazy='dynamic', cascade="all,delete")
    subscribed_num = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, url):
        feed_link = get_feed_link(url)
        if feed_link is None:
            raise CannotGetFeedSite(url)
        self.url = feed_link
        feed_data = FeedData(feed_link)
        feed_data.init_data()
        self.title =  feed_data.site_title
        updated = feed_data.site_updated
        if updated is not None:
            self.updated = updated
        else:
            self.updated = datetime.datetime.now()
        #app.logger.info("create feed site %s" % self.title)

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
        app.logger.info("add feed articles %s" % self.title)

    def __repr__(self):
        return "<FeedArticle %s>" % self.title.encode('utf8')

    def __unicode__(self):
        return "%s" % self.title
