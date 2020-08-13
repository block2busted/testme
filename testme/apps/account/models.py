from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from testme import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    photo = db.Column(db.String(20), nullable=True, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    created_tests = db.relationship('CustomTestme', backref='created_tests_author', lazy=True)
    profile = db.relationship('UserProfile', uselist=False, backref='user_profile')
    comments = db.relationship('Comment', backref='user_comment', lazy=True)
    passed_testme_list = db.relationship('UserTestme', backref='passed_testme_list', lazy=True)
    user_testme_answer = db.relationship('UserTestmeAnswer', backref='user_testme_answer')

    def __repr__(self):
        return f'{self.username}'

    def create_profile(self, *args, **kwargs):
        profile = UserProfile(user_id=self.id, username=self.username)
        db.session.add(profile)
        db.session.commit()


class UserProfile(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    photo = db.Column(db.String(64), nullable=True, default='default.jpg')
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    about = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'Profile {self.username}'
