import os

HERE = os.path.dirname(__file__)
DEBUG = True
DATABASE_NAME = 'airead.db'
ADMIN_NAME = "airead"
ADMIN_PASSWORD = "airead"
LOG_FILE = "airead.log"
TIMER_LOG_FILE = "airead_timer.log"
SECRET_KEY = "7KdQS8mTtXEBW6PDZr0N"
NAME = "AiRead"
ADMIN_VIEW_NAME = "AiRead Data Viewer"
API_PREFIX = "/api/"
USER_API_PREFIX = API_PREFIX + "user"
FEED_API_PREFIX = API_PREFIX + "feed"

if DEBUG:
    SQLALCHEMY_DATABASE_URI = "sqlite:////" + HERE + "/" + DATABASE_NAME
    SQLALCHEMY_ECHO = False
