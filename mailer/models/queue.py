from pony.orm import Required, Optional, PrimaryKey, Database, db_session
import datetime
import time
from nacl.pwhash import scrypt
from jose import jwt
from mailer.config import Config
from mailer.models import db
from mailer.models.sessions import SessionManager
from pprint import pprint


class Queue(db.Entity):

    _table_ = 'queue'

    queue_id = PrimaryKey(int, auto=True)
    customer_id = Required(int)


class QueueManager(object):

    @classmethod
    @db_session
    def add_queue(cls, customer_id):
        try:
            Queue(customer_id=customer_id)
            return True
        except:
            return False

    @classmethod
    @db_session
    def remove_queue(cls, queue_id):
        if Queue.exists(queue_id=queue_id):
            try:
                queue = Queue(queue_id=queue_id)
                queue.delete()
                return True
            except:
                return False
        else:
            return False

    @classmethod
    @db_session
    def get_queue(cls):
        queue = Queue.select()
        pprint(queue)
        return queue
