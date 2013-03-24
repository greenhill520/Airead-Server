from flask import Blueprint, g, current_app
from auth import basic_auth
from util import api_response, get_request_json
from airead.app import db
from code_and_msg import *
from airead.models import User

app = Blueprint("user", __name__)
"""
register
login
"""

# unsafe
@app.route("/register/", methods=('POST', ))
def register():
    """
    Register a new user
    post json format:
        {'username': username, 'password': password, 'email': email}
    response json format:
        {'user_id': id}
    """
    info = get_request_json()
    if info is None:
        return api_response(success=False, data=None,
                error_code=no_post_data[0], error_messag=no_post_data[1])
    username = info['username']  
    password = info['password']
    email = info['password']
    if User.query.filter_by(username=username).count() > 0:
        return api_response(success=False, data=None,
                error_code=user_exist[0], error_message=user_exist[1])
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    current_app.logger.info('user %s registered' % user.username)
    return api_response(success=True, data={'user_id': user.id})

@app.route("/login/", methods=('POST', ))
@basic_auth
def login():
    """
    login
    no post data, just insert password and username in authorization header
    response json format:
        {'user_id': user_id}
    """
    if g.user is not None:
        current_app.logger.info('user %s logined' % g.user.username)
        return api_response(success=True, data={'user_id': g.user.id})
    else:
        return api_response(success=False, data=None,
                error_code=unknown_error[0], error_message=unknown_error[1])
