"""
In this module, we add logic to add customers, who opted to receive emails about
special offers, to the MailChimp mailing list
"""
import os

import requests
from flask import current_app
from mailchimp3 import MailChimp


MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID')
MAILCHIMP_USERNAME = os.environ.get('MAILCHIMP_USERNAME')

mailchimp_client = MailChimp(MAILCHIMP_USERNAME, MAILCHIMP_API_KEY)


def add_member_to_subscription_list(email):
    """Add given email_address to MailChimp subscription list"""
    try:
        current_app.logger.info('Subscribing customer with email {} to mailchimp'.format(email))
        mailchimp_client.lists.members.create(list_id=MAILCHIMP_LIST_ID,
                                              data={'email_address': email,
                                              'status': 'subscribed'})
    except requests.exceptions.RequestException as e:
        current_app.logger.error(e)
    else:
        return mailchimp_client.lists.members.subscriber_hash


def remove_member_from_subscription_list(mailchimp_subscriber_hash):
    """Remove cusotmer from MailChimp subsription list"""
    try:
        current_app.logger.info('Unsubscribing customer from mailchimp')
        mailchimp_client.lists.members.delete(list_id=MAILCHIMP_LIST_ID,
                                              subscriber_hash=mailchimp_subscriber_hash)
    except requests.exceptions.RequestException:
        current_app.logger.error(e)