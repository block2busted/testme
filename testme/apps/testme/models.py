from datetime import datetime
from testme import db


class CustomTestme(db.Model):
    """Testme model"""
    __tablename__ = 'custom_testme'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=True)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    questions = db.relationship('TestmeQuestion', backref='testme_questions', lazy=True)
    answers = db.relationship('TestmeAnswer', backref='testme_answers', lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    execution_count = db.Column(db.Integer, nullable=False, default=0)
    user_testme = db.relationship('UserTestme', backref='user_testme', lazy=True)


    def __repr__(self):
        return f'Test №{self.id}: {self.title}'


class TestmeQuestion(db.Model):
    """Model of testme question"""
    __tablename__ = 'testme_question'

    id = db.Column(db.Integer, primary_key=True)
    testme_id = db.Column(db.Integer, db.ForeignKey('custom_testme.id'), nullable=False)
    title = db.Column(db.String(128), unique=False, nullable=False)
    answers = db.relationship('TestmeAnswer', uselist=False, backref='question_answers', lazy=True)
    right_answer = db.relationship('TestmeRightAnswer', uselist=False, backref='right_answer', lazy=True)


class TestmeAnswer(db.Model):
    """Variable of answers model"""
    __tablename__ = 'testme_answer'

    id = db.Column(db.Integer, primary_key=True)
    answer_1 = db.Column(db.String(128), nullable=False)
    answer_2 = db.Column(db.String(128), nullable=False)
    answer_3 = db.Column(db.String(128), nullable=False)
    answer_4 = db.Column(db.String(128), nullable=False)
    testme_id = db.Column(db.Integer, db.ForeignKey('custom_testme.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('testme_question.id'), nullable=False)

    def __repr__(self):
        return f'Answers of question №{self.question_id}.'


class TestmeRightAnswer(db.Model):
    """Right-answer model"""
    __tablename__ = 'testme_right_answer'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('testme_question.id'), nullable=False)

    def __repr__(self):
        return f'Number of right answer to question №{self.question_id}'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    testme_id = db.Column(db.Integer, db.ForeignKey('custom_testme.id'))
    author = db.Column(db.String(32), nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Comment by {self.author} for testme №{self.testme_id}'


class UserTestme(db.Model):
    __tablename__ = 'user_testme'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(64), nullable=False)
    passed_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    testme_id = db.Column(db.Integer, db.ForeignKey('custom_testme.id'))
    results = db.Column(db.Float, nullable=False)
    answer = db.relationship('UserTestmeAnswer', backref='user_answers', lazy=True)

    def __repr__(self):
        return f'Test passed by {self.username}'


class UserTestmeAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128), nullable=False)
    user_testme_id = db.Column(db.Integer, db.ForeignKey('user_testme.id'))

    def __repr__(self):
        return f'Answer on question №{self.id}: {self.content}'
