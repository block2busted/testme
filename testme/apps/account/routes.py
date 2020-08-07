from flask import render_template, flash, redirect, url_for, request, session, jsonify
from testme import app, bcrypt, db, vk_oauth, github_oauth
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


@app.route('/vk-oauth')
def vk_oauth_login():
    return vk_oauth.authorize(callback=url_for(
        'vk_oauth_authorized',
        next=request.args.get('next') or request.referrer or None)
    )


@app.route('/vk-oauth-authorized')
@vk_oauth.authorized_handler
def vk_oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash('You denied the request to sign in.')
        return redirect(next_url)

    session['vk_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['vk_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


@app.route('/github-oauth')
def github_oauth_login():
    return github_oauth.authorize(callback=url_for(
        'github_oauth_authorized',
        _external=True)
    )


@app.route('/github-oauth-authorized')
@github_oauth.authorized_handler
def github_oauth_authorized(response):
    print(response)
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            response
        )
    session['github_token'] = (response['access_token'], '')
    github_token = response['access_token']
    me = github_oauth.get('user')
    return jsonify(me.data)


@github_oauth.tokengetter
def get_github_oauth_token():
    return session.get('github_token')



