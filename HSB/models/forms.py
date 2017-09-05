from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    TextAreaField
    )
from wtforms import validators

from ..utils.validators import Unique


class SigninForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(),
                                  validators.Email(),
                                  validators.Length(min=6, max=50),
                                  Unique()])
    password = PasswordField("Password", [validators.DataRequired()])


class CurrencyForm(FlaskForm):
    name = StringField('币名 - Name', [validators.DataRequired()])
    symbol = StringField('代码 - Symbol', [validators.DataRequired()])
    alias = StringField('别名 - Alias')
    mytoken_id = StringField('MytokenId (默认和symbol一致)')
    enabled = BooleanField('是否在线')
    ico_cost = StringField('ICO成本')
    description = TextAreaField('项目描述')
    ico_date = StringField('ICO募集时间')
    ico_amount = StringField('ICO总量')
    ico_distribution = TextAreaField('分发方案')


class SearchForm(FlaskForm):
    search = StringField('搜索', [validators.DataRequired()])
