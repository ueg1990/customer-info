from flask import Blueprint, render_template, redirect, session, url_for

from app.decorators import login_required

blueprint = Blueprint('public', __name__)


@blueprint.route('/')
def home():
    """Return Home Page"""
    return render_template('public/index.html')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Return Login page"""
    session['logged_in'] = True
    return render_template('public/login.html')


@blueprint.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))
