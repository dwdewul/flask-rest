from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'bob', '1234')
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u._id: u for u in users}

def authenticate(username, password):
    """Authenticate the user"""
    user = username_mapping.get(username, None)

    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    """Return the user's identity"""
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
