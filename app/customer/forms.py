from flask_wtf import FlaskForm as Form
from wtforms import BooleanField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import Email, Length, Required


class CustomerSearchForm(Form):
    phone_number = StringField('Phone Number',
                                validators=[Required(), Length(min=10, max=10)])


class NewCustomerForm(Form):
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    email = email = StringField('Email', validators=[Required(), Email()])
    phone_number = StringField('Phone Number',
                                validators=[Required(), Length(min=10, max=10)])
    address = TextAreaField('Address')
    last_order = TextAreaField('Last Order')
    send_email = BooleanField('Get emails about latest deals')


class UpdateDeleteForm(Form):
    update = SubmitField('Update Customer')
    delete = SubmitField('Delete Customer')
    customer_id = HiddenField()