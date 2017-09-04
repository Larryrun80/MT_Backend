import arrow

from .. import db
from .managementview import ManagementView


class Ico(db.Model, ManagementView):
    """docstring for ico"""

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    symbol = db.Column(db.String(20))
    alias = db.Column(db.String(20))
    description = db.Column(db.String(500))
    ico_cost = db.Column(db.String(100))
    ico_datetime = db.Column(db.String(50))
    ico_amount = db.Column(db.String(50))
    ico_distribution = db.Column(db.String(500))
    is_deleted = db.Column(db.Integer())
    created_at = db.Column(db.Integer())
    updated_at = db.Column(db.Integer())

    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'),
                            autoincrement=True)
    currency = db.relationship('Currency', foreign_keys='Ico.currency_id',
                               backref='Ico_currency_id')

    def __init__(self, **kwargs):
        # for k, v in kwargs.items:
        #     print(k, v)
        self.is_deleted = 0
        self.created_at = arrow.now().timestamp
        self.updated_at = arrow.now().timestamp

    def __repr__(self):
        return 'ico cost: {}'.format(self.ico_cost)
