from flask import render_template, flash, redirect, url_for, request, session, jsonify
from testme import app, bcrypt, db, github_oauth
from .models import User, UserProfile
from .forms import SignupForm, LoginForm, ProfileUpdateForm
from flask_login import login_user, logout_user, current_user, login_required
from .services import save_photo


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(signup_form.password.data).decode('utf-8')
        user = User(
            username=signup_form.username.data,
            email=signup_form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        user.create_profile()
        flash(f'Hello, {user.username}! Check your mail to activate an account!', 'success')
        return redirect(url_for('index'))
    return render_template('account/signup.html', signup_form=signup_form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        login_form = LoginForm()
        if login_form.validate_on_submit():
            user = User.query.filter_by(email=login_form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, login_form.password.data):
                login_user(user, remember=login_form.remember.data)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('index'))
            else:
                flash('Please, check your email and password', 'danger')
        return render_template('account/login.html', login_form=login_form)
    else:
        login_form = LoginForm()
        return render_template('account/login.html', login_form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    profile_form = ProfileUpdateForm()
    user_profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    image_file = url_for('static', filename=f'profile_pics/{user_profile.photo}')
    if request.method == 'POST':
        if profile_form.validate_on_submit():
            user_profile.first_name = profile_form.first_name.data
            user_profile.last_name = profile_form.last_name.data
            user_profile.birth_date = profile_form.birth_date.data
            user_profile.about = profile_form.about.data
            if profile_form.photo.data:
                photo_file = save_photo(profile_form.photo.data)
                user_profile.photo = photo_file
            db.session.commit()
        return render_template(
                'account/profile.html',
                image_file=image_file,
                profile_form=profile_form,
                user_profile=user_profile
            )
    else:
        return render_template(
            'account/profile.html',
            image_file=image_file,
            profile_form=profile_form,
            user_profile=user_profile
        )
