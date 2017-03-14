"""
In this module, we add logic to add customers, who opted to receive emails about
special offers, to the MailChimp mailing list
"""
import os

import requests
from mailchimp3 import MailChimp


MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID')
MAILCHIMP_USERNAME = os.environ.get('MAILCHIMP_USERNAME')


class MailChimpException(requests.exceptions.RequestException):
    pass


def add_member_to_subscription_list(email):
    """Add given email_address to MailChimp subscription list"""
    client = MailChimp(MAILCHIMP_USERNAME, MAILCHIMP_API_KEY)
    try:
        client.lists.members.create(list_id=MAILCHIMP_LIST_ID, data={'email_address': email,
                                    'status': 'subscribed'})
    except MailChimpException:
        pass
    else:
        return client.lists.members.subscriber_hash



def remove_member_from_subscription_list(mailchimp_subscriber_hash):
    """Remove cusotmer from MailChimp subsription list"""
    client = MailChimp(MAILCHIMP_USERNAME, MAILCHIMP_API_KEY)
    try:
        client.lists.members.delete(list_id=MAILCHIMP_LIST_ID,
                                    subscriber_hash=mailchimp_subscriber_hash)
    except MailChimpException:
        pass