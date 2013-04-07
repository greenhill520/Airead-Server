from airead.models import User, UserSubscribe, FeedArticle, FeedSite, AdminUser
from airead.database import db
from airead import create_adminuser
from flask import current_app as app

if __name__ == '__main__':
    db.create_all()
    create_adminuser()
    test_user = User("test", "test@test.com", "123123")
    site = FeedSite("http://mindhacks.cn/")
    db.session.add(test_user)
    db.session.add(site)
    db.session.commit()
    UserSubscribe.subscribe(test_user.id, site.id)
