from typing import Any, Dict

from flask import flash
from pony.orm import db_session

from mailer.models import Customers, Queue, Templates


class QueueManager(object):

    @classmethod
    @db_session
    def add_queue(cls, customer_id: int, template_id: int) -> bool:
        if Queue.exists(customer_id=customer_id):
            # We don't want to be spamming the customers.
            # Don't add to queue if they are already there.
            flash("Customer is already in the queue.", 'queue_error')
            return False
        else:
            try:
                Queue(customer_id=customer_id, template_id=template_id)
                return True
            except Exception as err:
                flash("Error adding customer to the queue: {}".format(
                    err), 'queue_error')
                print(err)
                return False

    @classmethod
    @db_session
    def remove_queue(cls, queue_id: int) -> bool:
        if Queue.exists(queue_id=queue_id):
            try:
                queue = Queue[queue_id]
                queue.delete()
                return True
            except Exception as err:
                print(err)
                return False
        else:
            return False

    @classmethod
    @db_session
    def get_queue_item(cls, queue_id) -> dict:
        try:
            queue_item = Queue[queue_id]
            customer = Customers[queue_item.customer_id]
            template = Templates[queue_item.template_id]
            return customer, template
        except Exception as err:
            print(err)
            return {}

    @classmethod
    @db_session
    def get_queue(cls) -> dict:
        try:
            data: Dict(str, Any) = {}
            for q in Queue.select(lambda q: q.queue_id > 0):
                for c in Customers.select(lambda c: c.customer_id == q.customer_id):
                    data[q.queue_id] = {'queue_id': q.queue_id,
                                        'template_id': q.template_id,
                                        'customer_id': c.customer_id,
                                        'first_name': c.first_name,
                                        'last_name': c.last_name,
                                        'email': c.email,
                                        'phone': c.phone
                                        }
            return data
        except Exception as err:
            print(err)
            return {}
