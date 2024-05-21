from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/input')
def input():
    return render_template('input.html')


@app.route('/dive')
def dive():
    return render_template('dive.html')


@app.route('/all_dives')
def all_dives():
    return render_template('all_dives.html')


@app.route('/display_table')
def display_table():
    return render_template('display_table.html')


@app.route('/data')
def data():
    return render_template('data.html')


@app.route('/combat')
def data_option1():
    return render_template('data/combat.html')


@app.route('/currency_gained')
def data_option2():
    return render_template('data/currency_gained.html')


@app.route('/objectives_completed')
def data_option3():
    return render_template('data/objectives_completed.html')


@app.route('/samples_gained')
def data_option4():
    return render_template('data/samples_gained.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
