from pony.orm import Required, PrimaryKey
from mailer.models import db


class Customer(db.Entity):

    _table_ = 'customer'

    pass
