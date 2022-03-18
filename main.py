from flask import Flask, render_template
from additional_functions import parse_news
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/news')
def news():

    return render_template('news.html', title='Новости IT', news=parse_news())


@app.route('/competitions')
def competitions():
    return render_template('competitions.html', title='Олимпиады')


@app.route('/tests')
def tests():
    return render_template('tests.html', title='Тесты')


@app.route('/tests/1/<name>')
def tests_1(name):
    args_pages = {
        'start': [('/languages/python', 'обработка_данных.png', 'Обработка данных'),
                  ('/languages/python', 'создание_искусственного_интеллекта.png', 'Создание исскуственного интеллекта'),
                  ('/tests/1/софт_для_ПК', 'софт_для_ПК.png', 'Софт для ПК'),
                  ('/tests/1/веб_разработка', 'веб_разработка.png', 'Веб-разработка'),
                  ('/tests/1/мобильные приложения', 'мобильные_приложения.png', 'Мобильные приложения'),
                  ('/tests/1/разработка_игр', 'разработка_игр.png', 'Разработка игр')],
        'софт_для_ПК': [('/languages/java', 'все_платформы.png', 'Все платформы'),
                        ('/languages/c#', 'windows.png', 'Windows'),
                        ('/languages/swift', 'mac.png', 'Mac')],
        'веб_разработка':  [('/languages/javascript', 'внешний_вид_сайта.png', 'Внешний вид сайта'),
                            ('********', 'работа_с_сервером.png', 'Работа с сервером')],  # при работе с сервером можно ещё и учитывать масштаб проекта
        '': [] ### !!! МНЕ ОГРАНИЧИЛИ ЗАГРУЗКУ ФОТОГРАФИЙ, жду до завтра
    }
    name_pages = {
        'start': render_template('tests_1.html', title='Какой ЯП?', sp=args_pages['start']),
        'обработка_данных': render_template('base.html', title='Обработка данных'),
        'создание_исскуственного_интеллекта': render_template('base.html', title='Создание Исскуственного интеллекта'),
        'софт_для_ПК': render_template('tests_1.html', title='Софт для ПК', sp=args_pages['софт_для_ПК']),
        'веб_разработка': render_template('tests_1.html', title='Софт для ПК', sp=args_pages['веб_разработка']),
    }
    return name_pages[name]




if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')