import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_dance.contrib.github import make_github_blueprint, github


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('DJANGO_BLOG_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


github_blueprint = make_github_blueprint(client_id='ec166421daed34852672', client_secret='3b547a4737f446317c937e0f75533696993a3c31')

app.register_blueprint(github_blueprint, url_prefix='/github-oauth-login')

from testme.apps.testme import routes
from testme.apps.account import routes
