from flask import render_template, redirect, url_for, flash, request
from Public import app
from Public.form import SigninForm
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

from Public.mailchimp_account_data import *


@app.route('/', methods=['GET', 'POST'])
def main_page():
    sign_up = SigninForm()

    if sign_up.validate_on_submit():
        first_name = sign_up.firstName.data
        email = sign_up.email.data

        mailchimp = Client()
        mailchimp.set_config({
            "api_key":  get_api(),
            "server":  get_server_prefix()
        })

        list_id = get_list_id()

        member_info = {
            "email_address": email,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": first_name,
            }
        }

        try:
            response = mailchimp.lists.add_list_member(list_id, member_info)
            return render_template('success.html', name=first_name)
        except ApiClientError as error:
            return render_template('failure.html', name=first_name)

    return render_template('signup.html', form=sign_up)
