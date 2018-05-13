from typing import Union

from flask import flash
from pony.orm import db_session

from mailer.models import Customers, Queue


class CustomerManager(object):

    @classmethod
    @db_session
    def add_customer(cls, first_name: str, last_name: str, email: str, phone: int) -> bool:
        """Returns True if the customer already exists or is added, False is customer couldn't be added."""
        if Customers.exists(email=email):
            flash("Customer already exists", 'customer_error')
            return True
        else:
            try:
                Customers(first_name=first_name, last_name=last_name, email=email, phone=phone)
                return True
            except Exception as err:
                flash("Error creating customer: {}".format(err), 'customer_error')
                print(err)
                return False

    @classmethod
    @db_session
    def get_customer_by_id(cls, customer_id: int) -> Union[dict, bool]:
        if Customers.exists(customer_id=customer_id):
            try:
                return Customers[customer_id]
            except Exception as err:
                print(err)
                return False

    @classmethod
    @db_session
    def get_customer_by_email(cls, email: str) -> Union[dict, bool]:
        """This function is used when adding a customer to the queue. We don't want
        multiple customers with the same info in the system, so we check to make sure
        the email address doesn't already exist."""
        if Customers.exists(email=email):
            try:
                return Customers.get(email=email)
            except Exception as err:
                print(err)
                return False

    @classmethod
    @db_session
    def remove_customer(cls, customer_id: int) -> bool:
        if Customers.exists(customer_id=customer_id):
            try:
                queue_item = Queue.select(lambda q: q.customer_id == customer_id)
                queue_item.delete()
                customer = Customers[customer_id]
                customer.delete()
                return True
            except Exception as err:
                print(err)
                return False
        else:
            return False

    @classmethod
    @db_session
    def update_customer(cls, customer_id: int, first_name: str, last_name: str, email: str, phone: int) -> bool:
        if Customers.exists(customer_id=customer_id):
            try:
                customer = Customers[customer_id]
                customer.first_name = first_name
                customer.last_name = last_name
                customer.email = email
                customer.phone = phone
                return True
            except Exception as err:
                print(err)
                return False
        else:
            return False

    @classmethod
    @db_session
    def get_customers(cls) -> dict:
        try:
            return Customers.select(lambda c: c.customer_id > 0)[:]
        except Exception as err:
            print(err)
            return {}
