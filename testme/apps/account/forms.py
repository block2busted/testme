from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from .models import User


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('SignUp')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is busy. Please, try something different!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is busy. Please, try something different!')

    def validate_password(self, password):
        pass


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class ProfileUpdateForm(FlaskForm):
    photo = FileField('Update profile photo', validators=[FileAllowed(['jpg', 'png'])])
    first_name = StringField('First name', validators=[Optional()])
    last_name = StringField('Last name', validators=[Optional()])
    birth_date = DateField('Date of birth', validators=[Optional()], format='%d.%m.%Y')
    about = StringField('About', validators=[Optional()])
    submit = SubmitField('Update', validators=[DataRequired()])
