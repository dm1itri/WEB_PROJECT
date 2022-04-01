from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.validators import Length


class ProfileForm(FlaskForm):
    name = StringField('Имя', validators=[Length(max=64, message='Длина вашего имени не должна превышать 64 символов')])
    about = TextAreaField('Обо мне',  validators=[Length(max=256, message='Длина описания не должна превышать 256 символов')])
    password = PasswordField('Пароль', validators=[Length(max=16, message='Длина пароля должны быть от 4 до 16 символов')])
    submit = SubmitField('Сохранить изменения')