from flask import Blueprint, redirect, render_template, url_for


from app.customer.forms import CustomerSearchForm, NewCustomerForm
from app.customer.models import Customer
from app.decorators import login_required

blueprint = Blueprint('customer', __name__, url_prefix='/customer')


@blueprint.route('/', methods=('GET', 'POST'))
@login_required
def home():
    """Logged-in user homepage"""
    error = None
    form = CustomerSearchForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        customer = Customer.query.filter_by(phone_number=phone_number).first()
        if customer:
            return render_template('customer/customer.html', customer=customer)
        else:
            error = 'Customer with phone number {} not found'.format(phone_number)
    return render_template('customer/index.html', form=form, error=error)


@blueprint.route('/all')
@login_required
def customers():
    """List customers."""
    return render_template('customer/index.html')


@blueprint.route('/customer/<int:customer_id>')
@login_required
def customer(customer_id):
    """Get customer by id"""
    customer = Customer.query.get(customer_id)
    return render_template('customer/index.html')


@blueprint.route('/customer', methods=('GET', 'POST'))
@login_required
def add_customer():
    """Add new customer"""
    form = NewCustomerForm()
    if form.validate_on_submit():
        customer = Customer(form.first_name.data, form.last_name.data, form.email.data,
                            form.phone_number.data, form.address.data, form.last_order.data,
                            form.send_emai.data)
        db.session.add(customer)
        db.session.commit()
        return render_template('customer/customer.html', customer=customer)
    return render_template('customer/index.html', form=form)