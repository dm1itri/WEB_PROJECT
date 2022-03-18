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
    name_pages = {
        'start': render_template('tests_1.html', title='Какой ЯП?'),
        'обработка_данных': render_template('base.html', title='Главная'),
        'создание_исскуственного_интеллекта': render_template('base.html', title='Главная'),
        'софт_для_ПК': render_template('base.html', title='Главная'),
    }
    return name_pages[name]


'''
@app.route('/tests/1/<name>')
def tests_1(name):
    name_pages = {
        'разработка_игр': {'title':'Тесты'}
    }
    return render_template('base.html', **name_pages[name])
'''

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')