import os
import pyodbc
import SQL.queries
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
conn_str = str(SQL.queries.Server1)
port = os.environ.get("PORT", "5000")  # Get from env, if not - use 5000

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/all_dives")
def all_dives():
    return render_template("all_dives.html")


@app.route("/data")
def data():
    return render_template("data.html")


@app.route("/data/combat")
def data_combat():
    return render_template("combat.html")


@app.route("/data/currency_gained")
def data_currency():
    return render_template("currency_gained.html")


@app.route("/data/objectives")
def data_objectives():
    return render_template("objectives_completed.html")


@app.route("/data/samples")
def data_samples():
    return render_template("samples_gained.html")


# This works statically
@app.route("/display_table")
def display_table():
    return render_template("display_table.html")


@app.route("/dive")
def dive():
    return render_template("dive.html")


@app.route("/input")
def input():
    return render_template("input.html")


if __name__ == "__main__":
    app.run(debug=True)
