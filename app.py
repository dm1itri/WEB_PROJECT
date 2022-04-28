from flask import Flask, render_template, redirect, request, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_babelex import Babel
from flask_restful import Api

from data import db_session
from data.users import User
from data.olympiads import Olympiad
from data.programming_languages import ProgrammingLanguage
from forms.user import RegisterForm, LoginForm
from views import UserViews, OlympiadsViews, ProgrammingLanguagesViews
from profile1.routes import profile
from api.routes import ApiUser, ApiProgrammingLanguage, ApiOlympiads
from random import choice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# app.config['UPLOAD_FOLDER'] = '/static/image/profile'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
# app.config['SQLALCHEMY_DATABASE_URI'] = 'db/users.sqlite'

login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/users.sqlite")
babel = Babel(app)
app.register_blueprint(profile)
api = Api(app)

api.add_resource(ApiUser, '/api/user/<string:email>')
api.add_resource(ApiProgrammingLanguage, '/api/language/<string:name>')
api.add_resource(ApiOlympiads, '/api/olympiads/<string:type_olympiad>')


@babel.localeselector
def get_locale():
    override = request.args.get('lang')
    if override:
        session['lang'] = override
    return session.get('lang', 'ru')


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if current_user.admin != 'Администратор':
            return redirect(url_for('main_page'))
        return super(MyAdminIndexView, self).index()


admin = Admin(app, index_view=MyAdminIndexView(), name='Кабинет Администратора',
              template_mode='bootstrap4', base_template='admin/base_admin.html')
admin.add_view(UserViews(User, db_session.create_session(), name='Пользователи'))
admin.add_view(OlympiadsViews(Olympiad, db_session.create_session(), name='Олимпиады'))
admin.add_view(ProgrammingLanguagesViews(ProgrammingLanguage, db_session.create_session(),
                                         name='Языки программирования'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', exception='Страница не найдена'), 404


@app.errorhandler(500)
def not_found_error(error):
    return render_template('404.html', exception='Внутренняя ошибка сервера'), 500


@app.route('/')
def main_page():
    lang = ''
    button = True
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        lang = db_sess.query(User).filter(
            User.id == current_user.id).first().programming_languages.strip().split(' ')
        lang = choice(lang)
        button = False
    args = {
        'title': 'Главная',
        'programming_lang': lang,
        'button': button,
    }
    return render_template('main.html', **args)


@app.get('/olympiads')
def olympiads():
    db_sess = db_session.create_session()
    olympiads_list = db_sess.query(Olympiad).order_by(Olympiad.type).all()
    args = {
        'title': 'Уголок Олимпиадника',
        'olympiads': olympiads_list
    }
    return render_template('olympiads.html', **args)


@app.get('/tests')
def tests():
    return render_template('tests.html', title='Тесты')


@app.get('/tests/1/<name>')
def tests_1(name):
    '''Можно было и объединить функции test_1 и tests_2 так, как у них одинаковый функционал,
    но для понимания, что к чему тносится разделил'''
    args_pages = {
        'Какой_ЯП_твой': [('/languages/python', 'обработка_данных.png', 'Обработка данных'),
                          ('/languages/python', 'создание_искусственного_интеллекта.png',
                           'Создание исскуственного интеллекта'),
                          ('/tests/1/софт_для_ПК', 'софт_для_ПК.png', 'Софт для ПК'),
                          ('/tests/1/веб_разработка', 'веб_разработка.png', 'Веб-разработка'),
                          ('/tests/1/мобильные_приложения', 'мобильные_приложения.png',
                           'Мобильные приложения'),
                          ('/tests/1/разработка_игр', 'разработка_игр.png', 'Разработка игр')],
        'софт_для_ПК': [('/languages/java', 'все_платформы.png', 'Все платформы'),
                        ('/languages/c_sharp', 'windows.png', 'Windows'),
                        ('/languages/swift', 'mac.png', 'Mac')],
        'веб_разработка': [('/languages/javascript', 'внешний_вид_сайта.png', 'Внешний вид сайта'),
                           ('/languages/python', 'работа_с_сервером.png', 'Работа с сервером')],
        # при работе с сервером можно ещё и учитывать масштаб проекта
        'мобильные_приложения': [('/languages/swift', 'ios.png', 'IOS'),
                                 ('/languages/java', 'андроид.png', 'Андроид')],
        'разработка_игр': [('/languages/c_sharp', 'небольшие_игры.png', 'Небольшие проекты'),
                           ('/languages/c++', 'крупные_игры.png', 'Крупные проекты')]
    }
    name_pages = {
        'Какой_ЯП_твой': render_template('tests_1.html', title='Какой ЯП?', sp=args_pages[name]),
        'софт_для_ПК': render_template('tests_1.html', title='Софт для ПК', sp=args_pages[name]),
        'веб_разработка': render_template('tests_1.html', title='Веб-Разработка',
                                          sp=args_pages[name]),
        'мобильные_приложения': render_template('tests_1.html', title='Мобильные приложения',
                                                sp=args_pages[name]),
        'разработка_игр': render_template('tests_1.html', title='Разработка игр',
                                          sp=args_pages[name])
    }
    return name_pages[name]


@app.route('/tests/2/<name>')
def tests_2(name):
    args_pages = {
        'Выберите_формат_обучения': [
            ('/tests/2/Как_хорошо_знакомы_с_программированием?', 'tests_2/самостоятельный.png',
             'Самостоятельный'),
            ('/tests/2/Хочешь_быть_привязнным_ко_времени_и_месту?',
             'tests_2/с_наставником.png', 'С наставником')],
        'Как_хорошо_знакомы_с_программированием': [
            ('/education/самостоятельно-новичок', 'tests_2/новичок.png', 'Новичок'),
            ('/education/самостоятельно-профессионал', 'tests_2/опытный.png', 'Опытный')],
        'Хочешь_быть_привязнным_ко_времени_и_месту': [
            ('/education/очно-с_наставником', 'tests_2/конечно.png',
             'Привязанность ко времени и месту'),
            ('/education/заочно-c_наставником', 'tests_2/нет.png',
             'Обучение при помощи средств дистанционной связи')]
    }
    name_pages = {
        'Выберите_формат_обучения': render_template('tests_1.html',
                                                    title='Какой формат обучения?',
                                                    sp=args_pages[name]),
        'Как_хорошо_знакомы_с_программированием': render_template('tests_1.html',
                                                                  title='Уровень программирования',
                                                                  sp=args_pages[name]),
        'Хочешь_быть_привязнным_ко_времени_и_месту': render_template('tests_1.html',
                                                                     title='Привязанность к месту',
                                                                     sp=args_pages[name]),
    }
    return name_pages[name]


@app.route('/education/<name>')
def education(name):
    args_page = {
        'заочно-c_наставником': ('Отличный вариант обучения для человека, который не хочет тратить '
                                 'время на дорогу. Но очень важно во время дистанцинного занаятия не'
                                 ' отвлекаться на посторонние вещи, то для многих является трудностью',
                                 'tests_2/нет.png'),
        'очно-с_наставником': ('Большими плюсами данного способа является вовлеченность в жизнь '
                               'коллектива, а также четкий контроль со стороны педагога',
                               'tests_2/конечно.png'),
        'самостоятельно-новичок': ('Самый трудный вариант для большинства людей. При обучении '
                                   'придется всю информацию подбирать и структурировать самостоятельно.'
                                   ' Очень важно контролировать время уделяемое на обучение.'
                                   ' Получается, что это как минусы, так и плюсы.',
                                   'tests_2/новичок.png'),
        'самостоятельно-профессионал': ('При понимании большинства механизмов и знания '
                                        'программирования лучшим способом будет самостоятельное '
                                        'изучение официальной документации на определенные библиотеки',
                                        'tests_2/опытный.png'),
    }
    args = {
        'title': name.replace('_', ' ').replace('-', ' ').title(),
        'language': name.replace('-', '\n').title().replace('_', ' '),
        'about': args_page[name][0],
        'image': args_page[name][1],
        'add_language': None,
    }
    return render_template('languages.html', **args)


@app.route('/languages/<name>', methods=['GET', 'POST'])
def languages(name):
    add_language = None
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if request.method == 'POST':
            if name in user.programming_languages.strip().split(' '):
                user.programming_languages = user.programming_languages.replace(f'{name} ', '')
            else:
                user.programming_languages = user.programming_languages + name + ' '
            db_sess.commit()
        add_language = False if name in user.programming_languages.strip().split(' ') else True
    lang_arg = db_sess.query(ProgrammingLanguage).filter(ProgrammingLanguage.name == name).first()
    args = {
        'title': name.replace('_', ' ').title(),
        'language': name.replace('_', ' ').title(),
        'about': lang_arg.about,
        'image': lang_arg.name + '.png',
        'add_language': add_language,
        'link_1': lang_arg.href
    }
    return render_template('languages.html', **args)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.get('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_page'))


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    args = {
        'title': 'Регистрация',
        'form': form
    }
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            args['message'] = 'Пароли не совпадают'
            return render_template('register.html', **args)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            args['message'] = 'Такой пользователь уже есть'
            return render_template('register.html', **args)
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect(url_for('login'))
    return render_template('register.html', **args)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    args = {
        'title': 'Авторизация',
        'form': form
    }
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("main_page"))
        args['message'] = 'Неправильный логин или пароль'
        return render_template('login.html', **args)
    return render_template('login.html', **args)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
