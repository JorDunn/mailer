from pony.orm import Required
from mailer.app import pony

db = pony.db


class Customers(db.Entity):

    _table_ = 'customers'

    first_name = Required(str)
    last_name = Required(str)
    email = Required(str)


class Devices(db.Entity):

    _table_ = 'devices'

    customer_id = Required(int)
    make = Required(str)
    model = Required(str)
    repair = Required(str)
    emailed = Required(bool)
