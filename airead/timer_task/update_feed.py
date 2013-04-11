from airead.app import init_schedule_app, db
from airead.feeds import FeedData
from airead.models import FeedSite, FeedArticle

import datetime

app = init_schedule_app()

def update_feed(site_id):
    #print 'now update for id %s' % site_id 
    with app.app_context():
        site = FeedSite.query.get(site_id)
        if site is None:
            return
        site_url = site.url
        feed_data = FeedData(site_url)
        feed_data.init_data()
        old_updated = site.updated
        new_updated = feed_data.site_updated
        if new_updated is None or new_updated > old_updated or site.articles.count() == 0: # update the site
            if new_updated is None:
                site.updated = datetime.datetime.now()
            else:
                site.updated = new_updated
            db.session.add(site)
            db.session.commit()
            # now update all articles
            new_articles = feed_data.site_articles
            articles = site.articles.all()
            # delete all articles
            for item in articles:
                db.session.delete(item)
            db.session.commit()
            # add new articles
            for item in new_articles:
                article = FeedArticle(site_id=site_id, link=item['link'],
                        title=item['title'], updated=item['date'],
                        content=item['content'])
                db.session.add(article)
            db.session.commit()

if __name__ == '__main__':
    # simple test
    sites = FeedSite.query.all()
    for s in sites:
        app.logger.info("now update site %s" % s)
        print "now update site %s" % s
        update_feed(s.id)
