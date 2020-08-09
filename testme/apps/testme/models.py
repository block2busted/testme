from datetime import datetime
from testme import db


class Testme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    question = db.Column(db.String(128), unique=False, nullable=False)
    answer_1 = db.Column(db.String(128), nullable=False)
    answer_2 = db.Column(db.String(128), nullable=False)
    answer_3 = db.Column(db.String(128), nullable=False)
    answer_4 = db.Column(db.String(128), nullable=False)
    right_answer = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    execution_count = db.Column(db.Integer, nullable=False, default=0)
    comments = db.relationship('Comment', backref='testme', lazy=True)

    def __repr__(self):
        return f'{self.question}'


class CustomTestme(db.Model):
    """Testme model"""
    __tablename__ = 'custom_testme'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=True)
    questions = db.relationship('TestmeQuestion', backref='testme_questions', lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    execution_count = db.Column(db.Integer, nullable=False, default=0)

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
    question_id = db.Column(db.Integer, db.ForeignKey('testme_question.id'), nullable=False)

    def __repr__(self):
        return f'Answers of question №{self.question_id}.'


class TestmeRightAnswer(db.Model):
    """Right-answer model"""
    __tablename__ = 'testme_right_answer'

    id = db.Column(db.Integer, primary_key=True)
    right_answer_number = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('testme_question.id'), nullable=False)

    def __repr__(self):
        return f'Number of right answer to question №{self.question_id}'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    testme_id = db.Column(db.Integer, db.ForeignKey('testme.id'))
    author = db.Column(db.String(32), nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Comment by {self.author} for testme №{self.testme_id}'
