import datetime
import json
import time
from pprint import pprint

from jose import jwt
from nacl.pwhash import scrypt
from pony.orm import (Database, Optional, PrimaryKey, Required, db_session,
                      select)
from pony.orm.serialization import to_dict, to_json

from mailer.config import Config
from mailer.models import db
from mailer.models.customers import Customers
from mailer.models.sessions import SessionManager


class Queue(db.Entity):

    _table_ = 'queue'

    queue_id = PrimaryKey(int, auto=True)
    customer_id = Required(int)


class QueueManager(object):

    @classmethod
    @db_session
    def add_queue(cls, customer_id):
        print("Trying to add customer to queue...")
        try:
            Queue(customer_id=customer_id)
            print("Success")
            return True
        except Exception as e:
            print("Failure: {}".format(e))
            return False

    @classmethod
    @db_session
    def remove_queue(cls, queue_id):
        if Queue.exists(queue_id=queue_id):
            try:
                queue = Queue.get(queue_id=queue_id)
                queue.delete()
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    @classmethod
    @db_session
    def get_queue(cls):
        try:
            data = {}
            for q in Queue.select(lambda q: q.queue_id > 0):
                for c in Customers.select(lambda c: c.customer_id == q.customer_id):
                    data[q.queue_id] = {'queue_id': q.queue_id,
                                        'customer_id': c.customer_id,
                                        'first_name': c.first_name,
                                        'last_name': c.last_name,
                                        'email': c.email,
                                        'phone': c.phone
                                        }
            return data
        except BaseException as e:
            print("Failure: {}".format(e))
            return {}