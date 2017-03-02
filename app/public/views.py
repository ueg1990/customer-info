from flask import Blueprint, render_template

blueprint = Blueprint('public', __name__)


@blueprint.route('/')
def home():
    """Return Home Page"""
    return 'Hello World!' 
