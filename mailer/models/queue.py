from pony.orm import Required, Optional, PrimaryKey, Database, db_session, select
from pony.orm.serialization import to_dict, to_json
import datetime
import time
from nacl.pwhash import scrypt
from jose import jwt
from mailer.config import Config
from mailer.models import db
from mailer.models.sessions import SessionManager
from mailer.models.customers import Customers
from pprint import pprint
import json


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
        except KeyError:
            return json_data
