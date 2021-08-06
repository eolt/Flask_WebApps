import os

from app import app
from app.form import SigninForm
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from flask import render_template, url_for

@app.route('/', methods=['GET', 'POST'])
def main_page():
    sign_up = SigninForm()
    if sign_up.validate_on_submit():
        first_name = sign_up.firstName.data
        email = sign_up.email.data

        mailchimp = Client()
        mailchimp.set_config({
            "api_key": os.environ.get("API_KEY"),
            "server": os.environ.get("SERVER_PREFIX")
        })

        list_id = os.environ.get("LIST_ID")

        member_info = {
            "email_address": email,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": first_name,
            }
        }

        try:
            mailchimp.lists.add_list_member(list_id, member_info)
            return render_template('success.html', name=first_name)
        except ApiClientError as error:
            return render_template('failure.html', name=first_name)

    return render_template('signup.html', form=sign_up)
