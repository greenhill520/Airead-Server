from functools import wraps
from flask import request, Response, g

from airead.models import User

def check_auth(username, hash_password):
    """
    the password is hash password
    """
    users_list = User.query.filter_by(username=username).all()
    if len(users_list) == 0:
        return False
    user = users_list[0]
    if user is None:
        return False
    success = user.check_hash_password(hash_password)
    if not success:
        return False
    else:
        g.user = user
        return True

def challenge():
    return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )


def require_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        encode_auth = request.headers.get('Authorization', None)
        if encode_auth is None:
            return challenge()
        encode_auth = encode_auth.split()[-1]
        decode_auth = encode_auth.decode("base64")
        info = decode_auth.split(":")
        if not check_auth(info[0], info[1]):
            return challenge()
        else:
            return func(*args, **kwargs)

    return decorated
