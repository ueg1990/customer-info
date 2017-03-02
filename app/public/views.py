import os
from flask import Blueprint, redirect, render_template, request, session, url_for

from app.decorators import login_required

ADMIN_USERNAME = os.environ['CUSTOMER_INFO_ADMIN_USERNAME']
ADMIN_PASSWORD_HASH = os.environ['CUSTOMER_INFO_ADMIN_PASSWORD_HASH']

blueprint = Blueprint('public', __name__)


@blueprint.route('/')
def home():
    """Return Home Page"""
    return render_template('public/index.html')


def _validate_credentials(username, password):
    return (username == ADMIN_USERNAME and
            check_password_hash(ADMIN_PASSWORD_HASH, password))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Return Login page"""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if _validate_credentials(username, password):
            session['logged_in'] = True
            return redirect(url_for('customer/index.html'))
        else:
            error = 'Invalid username or password'
    return render_template('public/login.html', error=error)


@blueprint.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))
