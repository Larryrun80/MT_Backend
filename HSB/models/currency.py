import arrow
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
    search_field = db.Column(db.String(255))
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

    @classmethod
    def get_list(cls, **kwargs):
        list_columns = [
            {
              'name': 'Token ID',
              'attr': 'id',
              'format': '{attr}',
              'need_safe': False
            },
            {
              'name': 'Token Name',
              'attr': 'name',
              'format': '{attr}',
              'need_safe': False
            },
            {
              'name': 'Symbol',
              'attr': 'symbol',
              'format': '{attr}',
              'need_safe': False
            },
            {
              'name': '别名',
              'attr': 'alias',
              'format': '{attr}',
              'need_safe': False
            },
            {
              'name': 'MyToken ID',
              'attr': 'mytoken_id',
              'format': '{attr}',
              'need_safe': False
            },
            {
              'name': '排名',
              'attr': 'rank',
              'format': '{attr}',
              'need_safe': False
            },
            {
              'name': 'ico信息',
              'attr': 'ico',
              'format': '{attr}',
              'need_safe': False,
              'type': 'bool'
            },
            {
              'name': '在线',
              'attr': 'enabled',
              'format': '{attr}',
              'need_safe': False,
              'type': 'bool',
            },
            {
              'name': '创建时间',
              'attr': 'created_at',
              'format': '{attr}',
              'need_safe': False,
              'type': 'datetime'
            },
        ]

        currencies = []
        if 'keyword' in kwargs.keys() and kwargs['keyword']:
            currencies = cls.query.filter(
                Currency.search_field.like('%{}%'.format(kwargs['keyword'])))

        rows_data = []
        for currency in currencies:
            row_data = []
            for col in list_columns:
                col_type = col.get('type', 'string')
                row_data.append(col['format'].format(
                    attr=currency.get_attr_value(col['attr'], col_type)))

            rows_data.append(row_data)

        return (list_columns, rows_data)

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

    def get_attr_value(self, attr, attr_type='string'):
        if attr not in self.attr_map.keys():
            if hasattr(self, attr):
                data = getattr(self, attr)
            else:
                raise RuntimeError('illegal attribution: {}'.format(attr))
        else:
            data = self.attr_map[attr]

        if attr_type == 'string':
            return data
        if attr_type == 'bool':
            return True if data else False
        if attr_type == 'datetime':
            return arrow.get(data).format('YYYY-MM-DD HH:MM:SS')

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
