from typing import Sequence, Union

from flask import flash

from mailer.models import Customers, Queue


class CustomerManager(object):

    @classmethod
    def add_customer(cls, first_name: str, last_name: str, email: str, phone: int) -> bool:
        """Returns True if the customer already exists or is added, False is customer couldn't be added."""
        if Customers.exists(email=email):
            flash("Customer already exists", 'customer_error')
            return True
        else:
            try:
                Customers(first_name=first_name.capitalize(),
                          last_name=last_name.capitalize(), email=email.lower(), phone=phone)
                return True
            except Exception as err:
                flash("Error creating customer: {}".format(err), 'customer_error')
                print(err)
                return False

    @classmethod
    def get_customer(cls, **kwargs: Sequence) -> Union[dict, bool]:
        if 'email' in kwargs:
            if Customers.exists(email=kwargs['email']):
                try:
                    return Customers.get(email=kwargs['email'])
                except Exception as err:
                    print(err)
                    return False
        elif 'customer_id' in kwargs:
            if Customers.exists(customer_id=kwargs['customer_id']):
                try:
                    return Customers[kwargs['customer_id']]
                except Exception as err:
                    print(err)
                    return False

    @classmethod
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
    def get_customers(cls) -> dict:
        try:
            return Customers.select(lambda c: c.customer_id > 0)[:]
        except Exception as err:
            print(err)
            return {}
