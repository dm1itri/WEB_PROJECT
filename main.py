from flask import Flask, render_template
from additional_functions import parse_news
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/news')
def news():

    return render_template('news.html', news=parse_news())


@app.route('/competitions')
def competitions():
    return render_template('competitions.html')


@app.route('/tests')
def tests():
    return render_template('tests.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')