from sqlalchemy import orm

from .. import db
from .ico import Ico 
from .managementview import ManagementView


class Currency(db.Model, ManagementView):
    """docstring for currency"""

    # Columns
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50))
    symbol = db.Column(db.String(20))
    alias = db.Column(db.String(50))
    logo = db.Column(db.String(255))
    mytoken_id = db.Column(db.String(20))
    website = db.Column(db.String(255))
    rank = db.Column(db.Integer)
    enabled = db.Column(db.Integer)
    created_at = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)

    ico = db.relationship('Ico', foreign_keys='Ico.currency_id',
                          backref='Currency_ico', uselist=False)

    def __init__(self, **kwargs):
        pass

    @orm.reconstructor
    def init_on_load(self):
        self.attr_map = {
            'ico_cost': self.ico.ico_cost if self.ico else None,
            'description': self.ico.description if self.ico else None,
            'ico_date': self.ico.ico_datetime if self.ico else None,
            'ico_amount': self.ico.ico_amount if self.ico else None,
            'ico_distribution': self.ico.ico_distribution if self.ico else None
        }

    def __repr__(self):
        return '{} ({})'.format(self.name, self.symbol)

    def bind_form(self):
        from .forms import CurrencyForm

        form = CurrencyForm()
        for item in form:
            if item.id != 'csrf_token':
                item.data = self.get_attr_value(item.id)

        return form

    def update(self, form):
        for item in form:
            self.set_attr_value(item.id, item.data)

        db.session.merge(self)
        db.session.commit()

    def get_attr_value(self, attr):
        if attr not in self.attr_map.keys():
            if hasattr(self, attr):
                return getattr(self, attr)
            else:
                raise RuntimeError('illegal attribution: {}'.format(attr))
        else:
            return self.attr_map[attr]

    def set_attr_value(self, attr, val):
        if attr not in self.attr_map.keys():
            setattr(self, attr, val)
        else:
            if not self.ico:
                self.ico = Ico()
                self.ico.symbol = self.symbol
                self.ico.name = self.name
                self.ico.alias = self.alias

            setattr(self.ico, attr, val)
