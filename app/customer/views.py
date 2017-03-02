from flask import Blueprint, render_template

blueprint = Blueprint('customer', __name__, url_prefix='/customer')


@blueprint.route('/')
def customers():
    """List customers."""
    return render_template('customer/index.html')
