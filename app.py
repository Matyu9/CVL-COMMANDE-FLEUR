import hashlib
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, make_response
from werkzeug.exceptions import BadRequestKeyError

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
        return redirect(url_for('no_ano'))
    if len(database.select("SELECT user_name FROM user WHERE token=? AND admin",
                           (request.cookies.get('userID'),), )) > 0:
        return render_template("choix-ano.html")
    else:
        return redirect(url_for('no_ano'))


@app.route('/no-ano')
def no_ano():
    return render_template('home-no-login.html')


@app.route('/ano')
def ano():
    if not request.cookies.get('userID'):
        return redirect(url_for('no_ano'))
    if len(database.select("SELECT user_name FROM user WHERE token=? AND admin",
                           (request.cookies.get('userID'),), )) > 0:
        return render_template("home-login-ano.html")
    else:
        return redirect(url_for('no_ano'))


@app.route('/commande', methods=['POST'])
def commande():
    if not request.form['nd'] or not request.form["pd"] or not request.form["cd"] or not request.form['message']:
        return redirect(url_for("home"))
    try:
        database.insert("""INSERT INTO commande(nom_destinataire, prenom_destinataire, classe_destinataire, 
        nom_envoyeur, prenom_envoyeur, classe_envoyeur, message) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (request.form['nd'], request.form['pd'], request.form['cd'], request.form['ne'],
                         request.form['pe'], request.form['ce'], request.form['message']))
    except BadRequestKeyError:
        database.insert("""INSERT INTO commande(nom_destinataire, prenom_destinataire, classe_destinataire, message) 
        VALUES (?, ?, ?, ?)""", (request.form['nd'], request.form['pd'], request.form['cd'], request.form['message']))

    return "Merci de votre commande, la fleur de {} {} sera remis le je sais plus quand".format(request.form["nd"],
                                                                                                request.form["pd"])


def hash_perso(passwordtohash):
    try:
        passw = passwordtohash.encode()
    except AttributeError:
        return None
    passw = hashlib.md5(passw).hexdigest()
    passw = passw.encode()
    passw = hashlib.sha256(passw).hexdigest()
    passw = passw.encode()
    passw = hashlib.sha512(passw).hexdigest()
    passw = passw.encode()
    passw = hashlib.md5(passw).hexdigest()
    return


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        passwd = request.form['passwd']
        row = database.select(f'''SELECT user_name, password, token FROM user WHERE password = ? AND user_name = ?''',
                              (hash_perso(passwd), user), 1)

        try:
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('userID', row[2])
            database.insert(f'''UPDATE user SET last_online=? WHERE token=?''', (datetime.datetime.now(), row[2]))
            return resp
        except Exception as e:
            print(e)
            return redirect(url_for("home"))

    elif request.method == 'GET':
        return render_template('login.html')


if __name__ == '__main__':
    app.run()
