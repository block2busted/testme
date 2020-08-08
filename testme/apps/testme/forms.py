from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class TestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create')


class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add comment')
