from pony.orm import Required, PrimaryKey
from mailer.models import db


class Queue(db.Entity):

    _table_ = 'queue'

    pass
