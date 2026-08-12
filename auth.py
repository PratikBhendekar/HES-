from functools import wraps
from flask import session, redirect

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def is_admin():
    return session.get('user_type') == 'admin'

def get_current_user():
    return {
        'user_id': session.get('user_id'),
        'username': session.get('username'),
        'name': session.get('name'),
        'user_type': session.get('user_type')
    }