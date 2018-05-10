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
        """Returns a dict with the queue items and customer info for each item. This could probably
        be a JOIN statement in the future"""
        json_data = {}
        try:
            queue_json = json.loads(to_json(select(q for q in Queue)))
            for key, data in queue_json['Queue'].items():
                customer = json.loads(
                    to_json(select(c for c in Customers if c.customer_id == data['customer_id'])))
                for key2, data2 in customer['Customers'].items():
                    json_data[key] = {'queue_id': data['queue_id'], 'customer_id': data2['customer_id'],
                                      'first_name': data2['first_name'], 'last_name': data2['last_name'], 'email': data2['email'], 'phone': data2['phone']}
            return json_data
        except Exception as e:
            print(e)
            return json_data
