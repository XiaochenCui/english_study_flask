from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired(), Length(1, 64)])

    password = PasswordField('password', validators=[DataRequired()])

    remember_me = BooleanField('remember me')

    submit = SubmitField('login')


class RegistrationForm(Form):
    username = StringField('usernmae', validators=[
        DataRequired(), Length(1, 64), Regexp('^\w+$')])

    password = PasswordField('password', validators=[
        DataRequired(), EqualTo('password2', message='password must match!')])
    password2 = PasswordField('assume password', validators=[
        DataRequired()])

    submit = SubmitField('register')