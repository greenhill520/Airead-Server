from user_api import app as user_app
from feed_api import app as feed_app

def init_api(app):
    """
    register all api blueprints here
    """
    app.register_blueprint(user_app, url_prefix=app.config['USER_API_PREFIX'])
    app.register_blueprint(feed_app, url_prefix=app.config['FEED_API_PREFIX'])
