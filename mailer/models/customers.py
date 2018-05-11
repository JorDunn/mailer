from pony.orm import PrimaryKey, Required, db_session

from mailer.models import db


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
            print("Customer exists, returning existing customer...")
            return Customers.get(email=email)
        else:
            try:
                customer = Customers(first_name=first_name,
                                     last_name=last_name, email=email, phone=phone)
                return True, customer.customer_id
            except Exception as e:
                print("Failure: {}".format(e))
                return False

    @classmethod
    @db_session
    def get_customer_by_id(cls, customer_id: int) -> dict or bool:
        if Customers.exists(customer_id=customer_id):
            try:
                return Customers[customer_id]
            except Exception as e:
                print(e)
                return False

    @classmethod
    @db_session
    def get_customer_by_email(cls, email: str) -> dict or bool:
        if Customers.exists(email=email):
            try:
                return Customers.get(email=email)
            except Exception as e:
                print(e)
                return False

    @classmethod
    @db_session
    def remove_customer(cls, customer_id):
        if Customers.exists(customer_id=customer_id):
            try:
                customer = Customers[customer_id]
                customer.delete()
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    @classmethod
    @db_session
    def update_customer(cls, customer_id, first_name, last_name, email, phone):
        if Customers.exists(customer_id=customer_id):
            try:
                customer = Customers[customer_id]
                customer.first_name = first_name
                customer.last_name = last_name
                customer.email = email
                customer.phone = phone
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    @classmethod
    @db_session
    def get_customers(cls) -> dict:
        try:
            return Customers.select(lambda c: c.customer_id > 0)[:]
        except Exception as e:
            print("Failure: {}".format(e))
            return {}
