from flask_login import current_user
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError, InputRequired

from vocabulary.models import Word, User


class PreferencesForm(Form):
    username = StringField('usernmae', validators=[
        InputRequired(), Length(1, 64), Regexp('^\w+$')])
    level = SelectField('单词级别')
    learn_number = SelectField('每天的学习量', coerce=int)

    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level.choices = [(i, i) for i in Word.LEVELS]

        self.learn_number.choices = [(i, i) for i in [50, 100, 200]]

    def validate_username(self, field):
        if field.data != current_user.username:
            if User.query.filter_by(username = field.data).first():
                raise ValidationError('用户名已存在')