[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0591b76f51d54a39b725ea2d296adc9b)](https://www.codacy.com/app/JorDunn/mailer?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JorDunn/mailer&amp;utm_campaign=Badge_Grade) [![GitHub license](https://img.shields.io/github/license/JorDunn/mailer.svg)](https://github.com/JorDunn/mailer/blob/master/LICENSE)


# Mailer
A utility for sending emails to customers. Currently under construction for its v1.1.0 release. Master will most likely be broken, use the 1.0.0 branch.

Run mailer using this command:

    gunicorn -c gconfig.py run:app

# Crontab
Cron can be used to send emails with postman.py on a set interval. I would highly recommend doing some research on what the best times are for your target audience (e.g. lawyers, soccer moms, etc) are. I've included an example blow:

    # Send emails out at 11:00am every weekday
    0 11 * * 1-5 cd /path/to/mailer && pipenv run postman

You will most likely have to setup PATH in your crontab so it knows where pipenv is. I would also highly recommend setting up sendmail to email you if there are any errors. Amazon AWS has a really nice free tier that can be used to send emails and Zoho has free hosting with a custom domain if you need a mailbox. This project is not sponsored by either Amazon or Zoho, nor am I paid by them in any way.

# TODO for v2.0
* ~~flask-login integration.~~
* ~~Fix models so that circular imports are avoided.~~
* ~~Fix models so that Users and UserManager arn't needed. It should just be a User class.~~
* I need to really setup tox and pytest. (current task)
* Look into use Vue for part of the UI.
* Use javascript/Vue to insert form into the pages with tables, using buttons to reveal/hide the form.
* Expand mjml support to allow editing full template in mailer.
* Allow adding of customers to queue from customers page.
* Change franchises to groups and a dropdown on the login form to select users group. This would allow for multiple users to have the same username in different groups.
* Alternatively, have users login like an email address (e.g. user@group).
* ~~Use flasks g object for user info, in unison with flask-login.~~
* ~~Create more fine grain permissions for users.~~
* ~~Remove Sessions. I don't think I really need to save them.~~