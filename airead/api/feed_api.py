from flask import Blueprint, g, current_app
from auth import basic_auth
from util import api_response, get_request_json
from code_and_msg import * 
from airead.app import db
from airead.models import User, UserSubscribe, FeedSite, FeedArticle
from airead.feeds import get_feed_link, FeedData
from sqlalchemy.sql.expression import desc

import datetime

"""
subscribe
unsubscribe
get subscribe feeds articles 
get all feeds site(user in app search)
"""

app = Blueprint("feed", __name__)

@app.route("/subscribe/<int:user_id>/", methods=('POST', ))
@basic_auth
def subscribe(user_id):
    """
    subscribe a site's feed
    post json format:
        {'site': site}
    response:
        {'site_id': site_id, 'site_url': url}
    """
    user = User.query.get(user_id)
    if user is None:
        return api_response(success=False, data=None,
                error_code=user_not_exist[0], error_message=user_not_exist[1])
    info = get_request_json()
    if info is None:
        return api_response(success=False, data=None,
                error_code=no_post_data[0], error_message=no_post_data[1])
    site = info['site']
    feed_link = get_feed_link(site)
    if feed_link is None:
        return api_response(success=False, data=None,
                error_code=cant_find_feed[0], error_message=cant_find_feed[1])
    feed_site = None
    if FeedSite.query.filter_by(url=feed_site).count() > 0:
        feed_site = FeedSite.query.filter_by(url=feed_site).first()
    else:
        feed_site = FeedSite(feed_link)
        db.session.add(feed_site)
        db.commit()
    #user_subscribe = UserSubscribe(user_id=user.id, site_id=feed_site.id)
    #db.session.add(user_subscribe)
    #db.session.commit()
    UserSubscribe.subscribe(user.id, feed_site.id)
    return api_response(success=True, data={'site_id': feed_site.id,
        'site_url': feed_site.url})

@app.route("/unsubscribe/<int:user_id>/", methods=('POST', ))
@basic_auth
def unsubscribe(user_id):
    """
    unsubscribe a feed
    post json format:
        {'site_id': site_id}
    response:
        just success
    """
    user = User.query.get(user_id)
    if user is None:
        return api_response(success=False, data=None,
                error_code=user_not_exist[0], error_message=user_not_exist[1])
    info = get_request_json()
    if info is None:
        return api_response(success=False, data=None,
                error_code=no_post_data[0], error_message=no_post_data[1])
    #user_subscribe = UserSubscribe.query.filter_by(user_id=user.id, site_id=info['site_id']).first()
    #if user_subscribe is not None:
    #    db.session.delete(user_subscribe)
    #    db.session.commit()
    UserSubscribe.unsubscribe(user.id, info['site_id'])
    return api_response(success=True)

@app.route("/get_feed_articles/<int:user_id>/", methods=('GET', ))
@basic_auth
def get_feed_articles(user_id):
    """
    get user subscribe articles
    response json format:
        [
            {
                'site_id': site_id, 'site_title': site_title,
                'article_title': article_title, 'article_link': article_link
                'article_updated': article_update(MM-DD), 'article_content': article_content(content)
            },....
        ]
    """
    user = User.query.get(user_id)
    if user is None:
        return api_response(success=None, error_code=user_not_exist[0],
                error_message=user_not_exist[1])
    subscribes = UserSubscribe.query.filter_by(user=user).all()
    user_subscribe = [item.site.id for item in subscribes]
    articles = FeedArticle.query.filter(
            FeedArticle.site_id.in_(user_subscribe)).order_by(desc(FeedArticle.updated)).all()
    data = []
    for item in articles:
        _dict = {}
        _dict['site_id'] = item.site.id
        _dict['site_title'] = item.site.title
        _dict['article_title'] = item.title
        _dict['article_link'] = item.link
        _dict['article_updated'] = item.updated.strftime("%m-%d")
        _dict['article_content'] = item.content
        data.append(_dict)
    return api_response(success=True, data=data)

@app.route("/get_feed_articles/<int:user_id>/<int:page>/", methods=('GET', ))
@basic_auth
def get_feed_articles_page(user_id, page):
    """
    get user subscribe articles, paginate version(page start from 1)
    response json format:
        [
            {
                'site_id': site_id, 'site_title': site_title,
                'article_title': article_title, 'article_link': article_link
                'article_updated': article_update(MM-DD), 'article_content': article_content(content)
            },....
        ]
    """
    if page < 1:
        return api_response(success=False, error_code=error_page_num[0],
                error_message=error_page_num[1])
    user = User.query.get(user_id)
    if user is None:
        return api_response(success=False, error_code=user_not_exist[0],
                error_message=user_not_exist[1])
    subscribes = UserSubscribe.query.filter_by(user=user).all()
    user_subscribe = [item.site.id for item in subscribes]
    try:
        articles = FeedArticle.query.filter(
                FeedArticle.site_id.in_(user_subscribe)).order_by(
                        desc(FeedArticle.updated)).paginate(page=page).all()
        data = []
        for item in articles:
            _dict = {}
            _dict['site_id'] = item.site.id
            _dict['site_title'] = item.site.title
            _dict['article_title'] = item.title
            _dict['article_link'] = item.link
            _dict['article_updated'] = item.updated.strftime("%m-%d")
            _dict['article_content'] = item.content
            data.append(_dict)
        return api_response(success=True, data=data)
    except:
        return api_response(success=False, error_code=last_feed_page[0],
                error_message=last_feed_page[1])

@app.route("/get_all_feed_site/", methods=('GET',))
def get_all_feed_site():
    """
    get all feed site in the database
    response json format:
        [
            {
                'site_id': site_id, 'site_title': site_title,
                'site_url': site_url
            },...
        ]
    """
    feed_site = FeedSite.query.all()
    data = []
    for site in feed_site:
        _dict = {}
        _dict['site_id'] = site.id
        _dict['site_url'] = site.url
        _dict['site_title'] = site.title
        data.append(_dict)
    return api_response(success=True, data=data)
