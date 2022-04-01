from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4, max=16, message='Длина пароля должны быть от 4 до 16 символов')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    name = StringField('Имя пользователя', validators=[DataRequired(), Length(max=64, message='Длина вашего имени не должна превышать 64 символов')])
    about = TextAreaField("Немного о себе", validators=[Length(max=256, message='Длина описания не должна превышать 256 символов')])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
