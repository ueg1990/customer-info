from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint('customer', __name__, url_prefix='/customer')


@blueprint.route('/')
@login_required
def customers():
    """List customers."""
    return render_template('customer/index.html')
