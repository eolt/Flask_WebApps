from flask import render_template, url_for
from app import app
from app.form import SigninForm
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

import smtplib
from smtplib import SMTPException

# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apscheduler.schedulers.background import BackgroundScheduler
import atexit

import requests
import os


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


def create_message():
    recipients = []

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": os.environ.get("API_KEY"),
        "server": os.environ.get("SERVER_PREFIX")
    })

    list_id = os.environ.get("LIST_ID")

    try:
        response = mailchimp.lists.get_list_members_info(list_id)

        if len(response['members']) == 0:
            return
        else:
            for i in range(0, len(response['members'])):
                member = response['members'][i]
                email = member['email_address']
                recipients.append(email)

    except ApiClientError as error:
        return

    line = requests.get("https://api.themotivate365.com/stoic-quote").json()
    text = "\"" + line['data']['quote'] + "\"" + " - " + line['data']['author']

    message = MIMEMultipart("alternative")
    message['Subject'] = "Daily Stoicism Quote"
    message["From"] = "Stoic Meditations"

    html = "<html><body><p>" + line['data']['quote'] + " - " + line['data']['author'] + "</p></body></html>"

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        # set up the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(os.environ.get("EMAIL_ADDRESS"), os.environ.get("EMAIL_ADDRESS_PASSWORD"))
        server.ehlo()
        server.sendmail(os.environ.get("EMAIL_ADDRESS"), recipients, message.as_string())
        print("Successfully sent email")
    except SMTPException:
        print("Error: unable to send email")


scheduler = BackgroundScheduler()
scheduler.add_job(func=create_message, trigger='cron', day_of_week='*', hour='7', minute='00')
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
