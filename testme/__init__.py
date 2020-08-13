import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_oauth import OAuth


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('DJANGO_BLOG_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACE_MODIFICATIONS'] = True
app.config['WHOOSH_base'] = 'whoosh'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

oauth = OAuth()

github_oauth = oauth.remote_app(
    'github',
    consumer_key='ec166421daed34852672',
    consumer_secret='3b547a4737f446317c937e0f75533696993a3c31',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)


from testme.apps.testme import routes
from testme.apps.account import routes
