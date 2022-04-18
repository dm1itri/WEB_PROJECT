from flask import render_template, redirect, request, url_for, Blueprint
from flask_login import login_required, current_user
from data import db_session
from data.users import User
from forms.profile_editing import ProfileForm


profile = Blueprint('profile', __name__, url_prefix='/profile', template_folder='templates', static_folder='static')


@profile.route('/')
@login_required
def index():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    languages = user.programming_languages.strip().split(' ') if user.programming_languages.strip() else False
    args = {
        'title': 'Профиль',
        'name': user.name,
        'about': user.about,
        'avatar': 'static/image/' + user.avatar,
        'languages': languages,
        'admin': user.admin
    }
    return render_template('profile/index.html', **args)


@profile.route('/editing', methods=['GET', 'POST'])
@login_required
def editing():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    form = ProfileForm()
    if form.validate_on_submit():
        data = request.form.to_dict()
        if data['name']:
            user.name = data['name']
        if data['password']:
            user.set_password(data['password'])
        if data['about']:
            user.about = data['about']
        db_sess.commit()
        return redirect(url_for('.index'))
    args = {
        'title': 'Редактирование профиля',
        'name': user.name,
        'about': user.about,
        'form': form
    }
    return render_template('profile/editing.html', **args)


@profile.route('/editing/avatar', methods=['GET', 'POST'])
@login_required
def editing_avatar():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if request.method == 'POST':
        my_file = open(f'profile1/static/image/profile_{user.email.replace(".", "_")}.png', 'wb+')
        my_file.write(request.files['file'].read())
        my_file.close()
        user.avatar = f'profile_{user.email.replace(".", "_")}.png'
        db_sess.commit()
        return redirect(url_for('.index'))
    return render_template('profile/editing_avatar.html', avatar='static/image/' + user.avatar)