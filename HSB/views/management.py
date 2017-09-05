from flask import (Blueprint,
                   render_template,
                   redirect,
                   url_for,
                   flash,
                   jsonify)
from flask_login import login_required


mgt = Blueprint('management', __name__)


@mgt.route('/')
def index():
    return render_template('home/index.html')


@mgt.route('/currency')
@login_required
def mgt_currency_list():
    from ..models.currency import Currency

    return_data = {}
    (return_data['columns'], return_data['rows']) = Currency.get_list()
    return render_template('management/mgt_list.html',
                           data=return_data,
                           edit=True)


@mgt.route('/currency/<currency_id>', methods=["GET", "POST"])
@login_required
def mgt_currency_detail(currency_id=0):
    from ..models.currency import Currency
    from ..models.forms import CurrencyForm

    form = CurrencyForm()
    data = {
      'oid': currency_id,
    }

    if form.validate_on_submit():
        # update currency
        Currency.query.get(currency_id).update(form)

        flash('success')
        return redirect(url_for('management.mgt_currency_list'))
    else:
        form = Currency.query.get(currency_id).bind_form()

    return render_template('management/mgt_detail.html',
                           form=form,
                           data=data)
