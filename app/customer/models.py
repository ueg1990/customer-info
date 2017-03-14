from app.extensions import db


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.String(10), unique=True)
    address = db.Column(db.Text)
    last_order = db.Column(db.Text)
    send_email = db.Column(db.Boolean)
    mailchimp_member_id = db.Column(db.String(32))

    def __init__(self, first_name, last_name, email, phone_number, address,
                 last_order, send_email=False, mailchimp_member_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.last_order = last_order
        self.send_email = send_email
        self.mailchimp_member_id = mailchimp_member_id

    def __repr__(self):
        return '<Customer {} {}>'.format(self.first_name, self.last_name)
