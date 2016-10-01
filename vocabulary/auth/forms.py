from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo, ValidationError

from vocabulary.models import User


class LoginForm(Form):
    username = StringField('username', validators=[Length(1, 64)])

    password = PasswordField('password', validators=[Length(1, 64)])

    remember_me = BooleanField('remember me')

    submit = SubmitField('login')


class RegistrationForm(Form):
    username = StringField('usernmae', validators=[
        InputRequired(), Length(1, 64), Regexp('^\w+$')])

    password = PasswordField('password', validators=[
        InputRequired(), EqualTo('password2', message='password must match!')])
    password2 = PasswordField('assume password', validators=[
        InputRequired()])

    submit = SubmitField('register')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('用户名已存在')