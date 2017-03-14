from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError


from app.extensions import db
from app.customer.forms import (CustomerSearchForm, NewCustomerForm, UpdateDeleteForm,
                                UpdateCustomerForm)
from app.customer.mailchimp import (add_member_to_subscription_list,
                                    remove_member_from_subscription_list)
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
            return redirect(url_for('customer.customer', customer_id=customer.id))
        else:
            error = 'Customer with phone number {} not found'.format(phone_number)
    form.phone_number.data = ''
    return render_template('customer/index.html', form=form, error=error)


@blueprint.route('/all')
@login_required
def customers():
    """List customers."""
    customers = Customer.query.all()
    return render_template('customer/customers.html', customers=customers)


@blueprint.route('/<int:customer_id>', methods=('GET', 'POST'))
@login_required
def customer(customer_id):
    """Get customer by id"""
    customer = Customer.query.get(customer_id)
    form = UpdateDeleteForm()
    if form.validate_on_submit():
        if form.update.data:
            return redirect(url_for('customer.update_customer', customer_id=customer.id))
        else:
            if customer.send_email:
                remove_member_from_subscription_list(customer.mailchimp_member_id)
            db.session.delete(customer)
            db.session.commit()
            return redirect(url_for('customer.home'))
    return render_template('customer/customer.html', customer=customer, form=form)


@blueprint.route('/add', methods=('GET', 'POST'))
@login_required
def add_customer():
    """Add new customer"""
    error_dict = {}
    form = NewCustomerForm()
    if form.validate_on_submit():
        customer = Customer(form.first_name.data, form.last_name.data, form.email.data,
                            form.phone_number.data, form.address.data, form.last_order.data,
                            form.send_email.data)
        customer_exists = Customer.query.filter((Customer.phone_number == customer.phone_number) |
                                                (Customer.email == customer.email)).first()
        if customer_exists:
            error_dict['error'] = 'Customer with given email or phone number already exists.'
            error_dict['customer_id'] = customer_exists.id
        else:
            if customer.send_email:
                mailchimp_member_id = add_member_to_subscription_list(customer.email)
                customer.mailchimp_member_id = mailchimp_member_id
            db.session.add(customer)
            db.session.commit()
            return redirect(url_for('customer.customer', customer_id=customer.id))
    return render_template('customer/customer_form.html', form=form,
                           form_action=url_for('customer.add_customer'), error_dict=error_dict)


@blueprint.route('/update/<int:customer_id>', methods=('GET', 'POST'))
@login_required
def update_customer(customer_id):
    """Update given customer"""
    customer = Customer.query.get(customer_id)
    current_send_email_status = customer.send_email
    form = UpdateCustomerForm(obj=customer)
    if form.validate_on_submit():
        form.populate_obj(customer)
        if current_send_email_status != form.send_email.data:
            _update_customer_email_subscription(customer, form.send_email.data)
        db.session.commit()
        return redirect(url_for('customer.customer', customer_id=customer.id))
    return render_template('customer/customer_form.html', form=form,
                            form_action=url_for('customer.update_customer',
                            customer_id=customer.id))


def _update_customer_email_subscription(customer, send_email):
    if send_email:
        mailchimp_member_id = add_member_to_subscription_list(customer.email)
        customer.mailchimp_member_id = mailchimp_member_id
    else:
        remove_member_from_subscription_list(customer.mailchimp_member_id)
        customer.mailchimp_member_id = None