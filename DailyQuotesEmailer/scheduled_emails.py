import os
import smtplib
import requests

from tzlocal import get_localzone
from smtplib import SMTPException
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apscheduler.schedulers.blocking import BlockingScheduler

schedule = BlockingScheduler()


@schedule.scheduled_job('cron', hour='12', minute='0', timezone=get_localzone())
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


schedule.start()
