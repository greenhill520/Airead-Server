import os

HERE = os.path.dirname(__file__)
DEBUG = True
DATABASE_NAME = 'airead.db'
ADMIN_NAME = "airead"
ADMIN_PASSWORD = "airead"
LOG_FILE = "airead.log"
SECRET_KEY = "7KdQS8mTtXEBW6PDZr0N"

if DEBUG:
    SQLALCHEMY_DATABASE_URI = "sqlite:////" + HERE + "/" + DATABASE_NAME
    SQLALCHEMY_ECHO = False
