from airead.models import User, UserSubscribe, FeedArticle, FeedSite, AdminUser
from airead.database import db
from airead import create_adminuser, app

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_adminuser(app)
        # test data
        test_user = User("test", "test@test.com", "123123")
        site = FeedSite("http://mindhacks.cn/")
        db.session.add(test_user)
        db.session.add(site)
        db.session.commit()
        UserSubscribe.subscribe(test_user.id, site.id)
