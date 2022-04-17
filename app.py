from flask import Flask, render_template, redirect, request, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_babelex import Babel

from data import db_session
from data.users import User
from data.olympiads import Olympiad
from forms.user import RegisterForm, LoginForm
from views import UserViews, OlympiadsViews
from profile1.routes import profile
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
            return redirect('/login')
        if current_user.admin != 'Администратор':
            return redirect('/')
        return super(MyAdminIndexView, self).index()


admin = Admin(app, index_view=MyAdminIndexView(), name='Кабинет Администратора', template_mode='bootstrap4', base_template='my_master.html')
admin.add_view(UserViews(User, db_session.create_session(), name='Пользователи'))
admin.add_view(OlympiadsViews(Olympiad, db_session.create_session(), name='Олимпиады'))


@app.route('/')
def main_page():
    lang = ''
    button = True
    if current_user.__class__.__name__ != 'AnonymousUserMixin':
        db_sess = db_session.create_session()
        lang = db_sess.query(User).filter(User.id == current_user.id).first().programming_languages.strip().split(' ')
        lang = choice(lang)
        button = False

    return render_template('main.html', programming_lang=lang, button=button)


@app.get('/technical_class')
def technical_class():
    # Расписание
    # Замены
    # Календарь событий
    # return render_template('technical_class.html')
    pass


'''
@app.get('/news')
def news():
    return render_template('news.html', title='Новости IT', news=parse_news())

'''


@app.get('/olympiads')
def olympiads():
    db_sess = db_session.create_session()
    olympiads_list = db_sess.query(Olympiad).order_by(Olympiad.type).all()
    return render_template('olympiads.html', title='Уголок Олимпиадника', olympiads=olympiads_list)


@app.get('/tests')
def tests():
    return render_template('tests.html', title='Тесты')


@app.get('/tests/1/<name>')
def tests_1(name):
    args_pages = {
        'Какой_ЯП_твой': [('/languages/python', 'обработка_данных.png', 'Обработка данных'),
                          ('/languages/python', 'создание_искусственного_интеллекта.png', 'Создание исскуственного интеллекта'),
                          ('/tests/1/софт_для_ПК', 'софт_для_ПК.png', 'Софт для ПК'),
                          ('/tests/1/веб_разработка', 'веб_разработка.png', 'Веб-разработка'),
                          ('/tests/1/мобильные_приложения', 'мобильные_приложения.png', 'Мобильные приложения'),
                          ('/tests/1/разработка_игр', 'разработка_игр.png', 'Разработка игр')],
        'софт_для_ПК': [('/languages/java', 'все_платформы.png', 'Все платформы'),
                        ('/languages/c_sharp', 'windows.png', 'Windows'),
                        ('/languages/swift', 'mac.png', 'Mac')],
        'веб_разработка':  [('/languages/javascript', 'внешний_вид_сайта.png', 'Внешний вид сайта'),
                            ('/languages/python', 'работа_с_сервером.png', 'Работа с сервером')],  # при работе с сервером можно ещё и учитывать масштаб проекта
        'мобильные_приложения': [('/languages/swift', 'ios.png', 'IOS'),
                                 ('/languages/java', 'андроид.png', 'Андроид')],
        'разработка_игр': [('/languages/c_sharp', 'небольшие_игры.png', 'Небольшие проекты'),
                                 ('/languages/c++', 'крупные_игры.png', 'Крупные проекты')]
    }
    name_pages = {
        'Какой_ЯП_твой': render_template('tests_1.html', title='Какой ЯП?', sp=args_pages[name]),
        'софт_для_ПК': render_template('tests_1.html', title='Софт для ПК', sp=args_pages[name]),
        'веб_разработка': render_template('tests_1.html', title='Веб-Разработка', sp=args_pages[name]),
        'мобильные_приложения': render_template('tests_1.html', title='Мобильные приложения', sp=args_pages[name]),
        'разработка_игр': render_template('tests_1.html', title='Разработка игр', sp=args_pages[name])
    }
    return name_pages[name]


@app.route('/languages/<name>', methods=['GET', 'POST'])
def languages(name):
    args_pages = {
        'python': ('Python — это высокоуровневый язык программирования, который используется в различных сферах IT, '
                   'таких как машинное обучение, разработка приложений, web, парсинг и другие. '
                   'В 2019 году Python стал самым популярным языком программирования, обогнав Java на 10%. '
                   'Это обусловлено многими причинами, одна из которых — высокая оплата труда квалифицированных специалистов (около 100 тысяч долларов в год).',
                   'python.png', ['https://stepik.org/course/67/promo'], '"Простой Python. Современный стиль программирования"\nЛюбанович Билл'),
        'c++': ('С++ — производительный язык, он помогает дорожным картам в GPS не тупить и строить оптимальные маршруты, '
                'любимым играм — не лагать и выдавать максимальное качество с выкрученными до предела настройками графики, банковским сервисам — быть круглосуточными, а переводам — моментальными. '
                'Все потому, что на C++ можно использовать объектно-ориентированное программирование, а когда понадобится — обратиться к низкоуровневым возможностям языка.',
                'c++.png', ['https://stepik.org/course/363/promo']),
        'java': ('Java – это язык программирования общего назначения. '
                 'То есть язык, который применяется в разработке различных программных продуктов, без четкой специализации в конкретной сфере. Он во многом похож на Python, JavaScript и другие языки того же уровня, что и Java. '
                 'Кроме того, Java заимствует массу синтаксических конструкций из C и C++. А еще Java выступает в роли платформы. '
                 'Код, написанный на этом языке, запускается в виртуальной машине JVM и без проблем инициализируются в любой системе, где поддерживается соответствующая виртуальная машина.',
                 'java.png', ['https://stepik.org/course/187/promo']),
        'swift': ('Swift — открытый мультипарадигмальный компилируемый язык программирования общего назначения, '
                  'а также это надёжный и интуитивно понятный язык программирования от Apple, при помощи которого можно создавать приложения для iOS, Mac, Apple TV и Apple Watch. '
                  'Он предоставляет разработчикам небывалую свободу творчества. Благодаря этому простому и удобному языку с открытым кодом вам достаточно просто интересной идеи, чтобы создать нечто невероятное.',
                  'swift.png', ['https://stepik.org/course/89377/promo']),
        'javascript': ('Инструмент JavaScript (сокращенно JS) относится к языкам программирования высокого уровня с возможностью встраивания в другие приложения.'
                       'Интерактивные элементы сайтов и мобильных приложений часто выполняются на языке JavaScript. Он хорошо интегрируется с кодом HTML/CSS, поддерживается основными браузерами и включен в них по умолчанию. '
                       'Поэтому никаких вопросов с запуском веб-ресурсов не возникает, они работают без участия пользователя.',
                       'javascript.png', ['https://stepik.org/course/2223/promo']),
        'c_sharp': ('С# («Си Шарп») – один из наиболее быстро растущих, востребованных и при этом «удобных»  языков программирования. '
               'Это модификация фундаментального языка С от компании Microsoft, призванная создать наиболее универсальное средство для разработки программного обеспечения для большого количества устройств и операционных систем. '
               'Язык C# практически универсален. Можно использовать его для создания любого ПО: продвинутых бизнес-приложений, видеоигр, функциональных веб-приложений, приложений для Windows, macOS, мобильных программ для iOS и Android.',
                    'c_sharp.png', ['https://stepik.org/course/99426/promo'])
    }
    add_language = None
    if current_user.__class__.__name__ != 'AnonymousUserMixin':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if request.method == 'POST':
            if name in str(user.programming_languages):
                user.programming_languages = user.programming_languages.replace(f'{name} ', '')
            else:
                user.programming_languages = user.programming_languages + name + ' '
            db_sess.commit()
        add_language = False if name in str(user.programming_languages) else True
    return render_template('languages.html', title=name.replace('_', ' ').title(), language=name.replace('_', ' ').title(), about=args_pages[name][0], image=args_pages[name][1], add_language=add_language, link_1=args_pages[name][2][0])


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.get('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':

    app.run(port=8080, host='127.0.0.1')