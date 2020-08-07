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
    tests = db.relationship('Testme', backref='test_author', lazy=True)
    profile = db.relationship('UserProfile', backref='user_profile', lazy=True)
    oauth_token = db.Column(db.String(100), nullable=True)

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
