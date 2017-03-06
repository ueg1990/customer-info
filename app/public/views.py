import os
from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from app.decorators import login_required

ADMIN_USERNAME = 'user' #os.environ['CUSTOMER_INFO_ADMIN_USERNAME']
ADMIN_PASSWORD_HASH = 'pbkdf2:sha1:1000$Z6h2m5v4$10c6f4bae53c8f9eacb61bbb6922347b87419fba' #os.environ['CUSTOMER_INFO_ADMIN_PASSWORD_HASH']

blueprint = Blueprint('public', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Return Home Page (also contains Login form)"""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if _validate_credentials(username, password):
            session['logged_in'] = True
            return redirect(url_for('customer.home'))
        else:
            error = 'Invalid username or password'
    # If user logs in and immediately clicks Back button, should be redirected
    # to home page of a logged in user
    if session.get('logged_in'):
        return redirect(url_for('customer.home'))
    return render_template('public/index.html', error=error)


def _validate_credentials(username, password):
    return (username == ADMIN_USERNAME and
            check_password_hash(ADMIN_PASSWORD_HASH, password))


@blueprint.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('public.home'))
