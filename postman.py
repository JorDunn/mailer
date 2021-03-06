#!/usr/bin/env python3.6

from pony.orm import db_session
from mailer.models import db, Queue
from mailer.models.email import EmailManager
from mailer.config import Config

try:
    db.bind(provider=Config.PONY['provider'], user=Config.PONY['user'],
            password=Config.PONY['password'], db=Config.PONY['dbname'],
            host=Config.PONY['host'], port=Config.PONY['port'])
    db.generate_mapping()
except Exception as err:
    print(err)

with db_session:
    try:
        for q in Queue.select(lambda q: q.queue_id > 0):
            email = EmailManager()
            email.construct_email(q.queue_id)
            email.send(debuglevel=Config.EMAIL['debuglevel'])
            q.delete()
    except Exception as err:
        print(err)
