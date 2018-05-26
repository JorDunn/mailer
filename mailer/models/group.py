from pony.orm import Required, PrimaryKey
from mailer.models import db


class Group(db.Entity):

    _table_ = 'group'

    gid = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)

    def get_id(self):
        return self.gid

    def __repr__(self):
        return '<Group {}>'.format(self.name)

    def __add__(self, operand):
        # this will allow you to merge subgroups. Users from the right subgroup will be put in the left subgroup.
        pass


class Subgroup(db.Entity):

    _table_ = 'subgroup'

    sgid = PrimaryKey(int, auto=True)
    gid = Required(int)
    name = Required(str, unique=True)

    def get_id(self):
        return self.sgid

    def __repr__(self):
        return '<Subgroup {}>'.format(self.name)

    def __add__(self, operand):
        # this will allow you to merge subgroups. Users from the right subgroup will be put in the left subgroup.
        pass
