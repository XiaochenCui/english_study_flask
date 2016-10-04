from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo, ValidationError

from vocabulary.models import User


class LoginForm(Form):
    username = StringField('用户名', validators=[Length(1, 64)])

    password = PasswordField('密码', validators=[Length(1, 64)])

    remember_me = BooleanField('记住我')

    submit = SubmitField('登录')


class RegistrationForm(Form):
    username = StringField('用户名', validators=[
        InputRequired(), Length(1, 64), Regexp('^\w+$')])

    password = PasswordField('密码', validators=[
        InputRequired(), EqualTo('password2', message='两次输入的密码必须相同')])
    password2 = PasswordField('确认密码', validators=[
        InputRequired()])

    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('用户名已存在')


class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[InputRequired()])
    password = PasswordField('新密码', validators=[
        InputRequired(), EqualTo('password2', message='两次输入的密码必须相同')])
    password2 = PasswordField('确认新密码', validators=[InputRequired()])
    submit = SubmitField('提交')
