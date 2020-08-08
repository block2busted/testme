from datetime import datetime
from testme import db


class Testme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.Column(db.String(32), nullable=False)
    comments = db.relationship('Comment', backref='testme', lazy=True)

    def __repr__(self):
        return f'Test {self.title}'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    testme_id = db.Column(db.Integer, db.ForeignKey('testme.id'))
    author = db.Column(db.String(32), nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Comment by {self.author} for testme №{self.testme_id}'