from flask_admin.contrib.sqla import ModelView
from wtforms.validators import DataRequired, Length
from flask_login import current_user
from flask import redirect, render_template
from flask_admin import AdminIndexView


class UserViews(ModelView):
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect('/')

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.admin == 'Администратор')

    can_export = True
    can_edit = True
    can_create = False
    can_delete = False

    column_display_pk = True
    column_default_sort = ('name', True)
    column_sortable_list = ('id', 'name', 'email')
    column_exclude_list = ['hashed_password']  # исключены из отображения
    form_excluded_columns = ['hashed_password', 'created_date']  # исключены из редактирования
    column_labels = {
        'id': 'ID',
        'name': 'Имя пользователя',
        'about': 'Описание',
        'email': 'Email',
        'avatar': 'Аватар',
        'programming_languages': 'Языки программирования',
        'created_date': 'Дата создания',
        'admin': 'Администратор'
    }
    form_args = {
        'email': dict(label='Почта', validators=[DataRequired()]),
        'password': dict(label='Пароль', validators=[DataRequired(), Length(min=4, max=16,
                                                                            message='Длина пароля должны быть от 4 до 16 символов')]),
        'name': dict(label='Имя пользователя', validators=[DataRequired(), Length(max=64,
                                                                                  message='Длина вашего имени не должна превышать 64 символов')]),
        'about': dict(label="Немного о себе", validators=[
            Length(max=256, message='Длина описания не должна превышать 256 символов')])
    }

    AVAILABLE_USER_TYPES = [
        (u'Администратор', u'Администратор'),
        (u'Пользователь', u'Пользователь'),
    ]
    form_choices = {
        'admin': AVAILABLE_USER_TYPES
    }
    column_searchable_list = ['email']
    column_editable_list = ['name', 'admin']  # быстрое изменение

    create_modal = True
    edit_modal = True



