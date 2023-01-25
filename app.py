from flask import Flask, render_template, request, redirect, url_for
from Utils import database
import sqlite3

app = Flask(__name__)
database = database.DataBase(user="cantina", password="LeMdPDeTest", host="localhost", port=3306,
                             database="cantina_db")
database.connection()
database.create_table("""CREATE TABLE IF NOT EXISTS commande(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
nom_destinataire TEXT NOT NULL, prenom_destinataire TEXT NOT NULL, classe_destinataire INT  NOT NULL, nom_envoyeur 
TEXT, prenom_envoyeur TEXT, classe_envoyeur INT, message TEXT(150))""")


@app.route('/')
def home():
    if not request.cookies.get('userID'):
        return render_template("home-no-login.html")
    if len(database.select("SELECT user_name FROM user WHERE token=? AND admin", (request.cookies.get('userID'),),)) > 0:
        return render_template("home-login.html")
    else:
        return render_template("home-no-login.html")


@app.route('/commande', methods=['POST'])
def commande():
    if not request.form['nd'] or not request.form["pd"] or not request.form["cd"]:
        return redirect(url_for("home"))
    return "Merci de votre commande, la fleur de {} {} sera remis le je sais plus quand".format(request.form["nd"],
                                                                                                request.form["pd"])


if __name__ == '__main__':
    app.run()
