from airead.app import app
app.config.from_pyfile("config.py")

from airead.models import User, UserSubscribe, FeedArticle, FeedSite
from airead.database import db

db.create_all()
