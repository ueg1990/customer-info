from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint('public', __name__)


@blueprint.route('/')
def home():
    """Return Home Page"""
    return 'Hello World!' 
