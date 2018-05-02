from pony.orm import Required, Optional, PrimaryKey, Database, db_session
import datetime
import time
from nacl.pwhash import scrypt
from jose import jwt
from mailer.config import Config
from mailer.models import db
from mailer.models.sessions import SessionManager
from pprint import pprint


class Customers(db.Entity):

    _table_ = 'customers'

    customer_id = PrimaryKey(int, auto=True)
    first_name = Required(str)
    last_name = Required(str)
    email = Required(str, unique=True)
    phone = Required(str)


class CustomerManager(object):

    @classmethod
    @db_session
    def add_customer(cls, first_name, last_name, email, phone):
        if Customers.exists(email=email):
            print("Customer exists")
            return False
        else:
            try:
                print("Trying to add customer... ")
                customer = Customers(first_name=first_name,
                                     last_name=last_name, email=email, phone=phone)
                pprint(customer)
                print("Success")
                return True, customer.customer_id
            except Exception as e:
                print(e)
                return False

    @classmethod
    @db_session
    def get_customer(cls, email):
        if Customers.exists(email=email):
            try:
                customer = Customers.get(email=email)
                return customer
            except Exception as e:
                print(e)
                return False

    @classmethod
    @db_session
    def remove_customer(cls, customer_id):
        if Customers.exists(customer_id=customer_id):
            try:
                customer = Customers(customer_id=customer_id)
                customer.delete()
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    @classmethod
    @db_session
    def update_customer(cls, customer_id, first_name, last_name, email):
        if Customers.exists(customer_id=customer_id):
            try:
                customer = Customers(customer_id=customer_id)
                customer.first_name = first_name
                customer.last_name = last_name
                customer.email = email
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False
