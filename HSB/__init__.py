import os

from flask import Flask, render_template

from .utils.utils import print_log

app = Flask(__name__, instance_relative_config=True)
ProjectDir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir))
app.basedir = ProjectDir
# print_log('Project Dir: {}'.format(ProjectDir))

# ###################
# ## Loading Configs
# ###################
# Load config from '/config.py'
if os.path.isfile('{}/config.py'.format(ProjectDir)):
    app.config.from_object('config')
    print_log('Loaded settings from "/config.py"')
else:
    print_log('Skipped loading settings from "/config.py": file not found')

# Load config from '/instance/default.py'
print_log('{}/instance/default.py'.format(ProjectDir))
if (os.path.isdir('{}/instance'.format(ProjectDir)) and
        os.path.isfile('{}/instance/default.py'.format(ProjectDir))):
    app.config.from_pyfile('default.py')
    print_log('Loaded settings from "/instance/default.py"')
else:
    print_log(
        'Skipped loading settings from "/instance/default.py": file not found')

# Load config from envvar, make sense to add APP_CONFIG_FILE to env var
try:
    app.config.from_envvar('APP_CONFIG_FILE')
except:
    print_log('The environment variable is not set and skip env var settings.')

# print_log(app.config)

# ###################
# ## Enable Markdown
# ###################
from flaskext.markdown import Markdown
Markdown(app)

# ####################
# ## Enable Blueprint
# ####################
from .views.home import home
from .views.management import mgt

app.register_blueprint(home)
app.register_blueprint(mgt, url_prefix='/admin')

# #############################
# ## Enable SQLAlchemy Support
# #############################
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# ########################
# ## Enable Email Support
# ########################
from flask_mail import Mail
mail = Mail(app)

# ##################
# ## Enable Bcrypt
# ##################
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ######################
# ## Enable Flask Login
# ######################
from flask_login import LoginManager
from .models.user import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home.signin"

@login_manager.user_loader
def load_user(user_id):
    return User()

# ##################
# ## Enable Toolbar
# ##################
from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)


@app.before_request
def do_before_request():
    # you can put database init code here
    pass


@app.teardown_request
def do_teardown_request(exception):
    # you can put database close code here
    pass


@app.errorhandler(404)
def file_not_found(error):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('error/500.html'), 500


# ###################
# ## Enable ErrorLog
# ###################
if not app.debug:
    import logging
    # we use log file to log errors here
    # you can also implement mail notification
    # see logging.handlers.SMTPHandler
    from logging.handlers import TimedRotatingFileHandler
    log_file = '{dir}/{file}'.format(dir=app.basedir,
                                     file=app.config['ERROR_LOG'])
    if not os.path.exists(os.path.split(log_file)[0]):
        os.makedirs(os.path.split(log_file)[0])
    file_handler = TimedRotatingFileHandler(log_file,
                                            when='midnight',
                                            interval=1,
                                            backupCount=0)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Project start up...')
