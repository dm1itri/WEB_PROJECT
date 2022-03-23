from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    name = StringField('Имя')
    about = TextAreaField('Обо мне')
    password = PasswordField('Пароль')
    submit = SubmitField('Сохранить изменения')