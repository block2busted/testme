from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    right_answers = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    ]

    question = StringField('Question', validators=[DataRequired()])
    answer_1 = StringField('Answer 1', validators=[DataRequired()])
    answer_2 = StringField('Answer 2', validators=[DataRequired()])
    answer_3 = StringField('Answer 3', validators=[DataRequired()])
    answer_4 = StringField('Answer 4', validators=[DataRequired()])
    right_answer = SelectField('Right answer', coerce=int, choices=right_answers)

    class Meta:
        csrf = None


class TestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    question = FieldList(FormField(QuestionForm), min_entries=5)
    add_question = SubmitField('Add question')
    submit = SubmitField('Create testme')


class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={'placeholder': 'Content'})
    submit = SubmitField('Add comment')
