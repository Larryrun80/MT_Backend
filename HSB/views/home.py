from flask import (Blueprint,
                   render_template,
                   redirect,
                   url_for,
                   flash,
                   jsonify)

from ..models.forms import SigninForm

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('home/index.html')


@home.route('/api')
def api_index():
    return jsonify({
            'status': 100,
            'message': 'ok',
            'result': {
                'message': 'welcome to HSFramework'
            }
        })


@home.route('/signup')
def signup():
    pass


@home.route('/signin', methods=["GET", "POST"])
def signin():
    from ..models.user import User
    from flask_login import login_user

    form = SigninForm()
    if form.validate_on_submit():
        if form.email.data == 'roy@mytoken.io' and\
              form.password.data == 'io.My_token':
            login_user(User())
            return redirect(url_for('home.index'))
        else:
            flash('登陆失败，请重试')
    return render_template('home/signin.html', form=form)
