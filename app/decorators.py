from functools import wraps

from flask import redirect, session, url_for

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('logged_in', False):
            return f(*args, **kwargs)
        return redirect(url_for('public.login'))
    return wrapper