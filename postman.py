#!/usr/bin/env python3.6

from pony.orm import db_session
from mailer.models import db, Queue, Templates, Customers
from mailer.models.email import EmailManager
from mailer.config import Config

try:
    db.bind(provider=Config.PONY['provider'], user=Config.PONY['user'],
            password=Config.PONY['password'], db=Config.PONY['dbname'])
    db.generate_mapping()
except TypeError:
    print("Already bound to database")

email = EmailManager()
email.construct_email(1)
