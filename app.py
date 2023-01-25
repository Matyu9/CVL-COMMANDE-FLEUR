from flask import Flask, render_template, request, redirect, url_for
from Utils import database
import sqlite3

app = Flask(__name__)
database_user = database.DataBase(user="cantina", password="LeMdPDeTest", host="localhost", port=3306,
                                        database="cantina_db")
database_command = sqlite3.connect('database.db')
database_command_cursor = database_command.cursor()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/commande', methods=['POST'])
def commande():
    if not request.form['nd'] or not request.form["pd"] or not request.form["cd"]:
        return redirect(url_for("home"))
    database_command_cursor.execute()
    return "Merci de votre commande, la fleur de {} {} sera remis le je sais plus quand".format(request.form["nd"],
                                                                                                request.form["pd"])


if __name__ == '__main__':
    app.run()
