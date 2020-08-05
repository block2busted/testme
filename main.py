from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from forms import SignupForm, LoginForm


app = Flask(__name__)


app.config['SECRET_KEY'] = os.getenv('DJANGO_BLOG_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        flash(f'Hello, {signup_form.username.data}! Check your mail to activate an account!', 'success')
        return redirect(url_for('index'))
    return render_template('account/signup.html', signup_form=signup_form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == 'block2bust@gmail.com' and login_form.password.data == 'password':
            flash(f'Hello, admin!', 'success')
            return redirect(url_for('index'))
    return render_template('account/login.html', login_form=login_form)


if __name__ == '__main__':
    app.run(debug=True)
