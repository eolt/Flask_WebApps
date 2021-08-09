# Automated Daily Email Program
Need a daily dose of inspiration to start your day? Enjoy reading quotes from influential people? Using the GET [stoi-quote](https://api.themotivate365.com/stoic-quote) API the daily automated emailer sends one quote of stoicism to enrich your day.

## Implementation
APScheduler runs a background task to automate the email messaging. The task is done once everday specified by the cron command:
```
@schedule.scheduled_job('cron', hour='12', minute='0', timezone=get_localzone())   
```
The hour relies on the localtime of the server which runs the program. I am running my program off [Heroku,](https://daily-stoicism-quotes.herokuapp.com) which is set to UTC time, so the hour is set to trigger at 7 A.M. Central Time (12 hours past). It can be updated to whichever over you would like or off the type of server used. 

The process of sending the email is done using Python library smtplib. I created a gmail account as the default sender of the emails. The list of email recipients is gathered and Saved by GET & POST [Mailchimp API](https://mailchimp.com/developer/marketing/api/)  


## Samples

<img width="1024" height="520" alt="Screen Shot 2021-08-06 at 1 52 43 PM" src="https://user-images.githubusercontent.com/27907086/128744102-dfaaa990-f268-4c4c-bfba-def9ec66e26c.png">


<img width="1024" height="520" alt="Screen Shot 2021-08-06 at 1 55 38 PM" src="https://user-images.githubusercontent.com/27907086/128745294-fffa54b2-f2f5-4a30-90cd-caa796d45c83.png">
