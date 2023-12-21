from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, make_response
from werkzeug.exceptions import BadRequestKeyError
from cantinaUtils.Database import DataBase
import hashlib
import os
import json


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
    return passw


file_path = os.path.abspath(os.path.join(os.getcwd(), "config.json"))

# Lecture du fichier JSON
with open(file_path, 'r') as file:
    config_data = json.load(file)

app = Flask(__name__)
database = DataBase(user=config_data['database_username'], password=config_data['database_password'],
                                   host="localhost", port=3306, database=config_data['database_name'])
database.connection()
database.exec("""CREATE TABLE IF NOT EXISTS commande(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
nom_destinataire TEXT NOT NULL, prenom_destinataire TEXT NOT NULL, classe_destinataire INT  NOT NULL, nom_envoyeur 
TEXT, prenom_envoyeur TEXT, classe_envoyeur INT, message TEXT(150), need_to_be_receive_by_cvl BOOL)""", None)


@app.route('/')
def home():
    return render_template('home-no-login.html')


@app.route('/commande', methods=['POST'])
def commande():
    if (not request.form['nd'] or not request.form["pd"] or not request.form["cd"] or not request.form['message']
            or not request.form['themself']):
        return redirect(url_for("home"))

    if request.form['themself'] == 'Oui':
        need_to_be_receive_by_cvl = True
    else:
        need_to_be_receive_by_cvl = False

    database.exec("""INSERT INTO commande(nom_destinataire, prenom_destinataire, classe_destinataire, 
    nom_envoyeur, prenom_envoyeur, classe_envoyeur, message, need_to_be_receive_by_cvl) VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s)""", (request.form['nd'], request.form['pd'], request.form['cd'],
                                          request.form['ne'], request.form['pe'], request.form['ce'],
                                          request.form['message'], need_to_be_receive_by_cvl))

    if need_to_be_receive_by_cvl:
        return "Merci de votre commande, la fleur de {} {} sera remis le je sais plus quand".format(request.form["nd"],
                                                                                                    request.form["pd"])
    else:
        return ("Merci de votre commande, votre fleur vous sera remis le je sais plus quand, vers le stand tenu par le "
                "CVL")


if __name__ == '__main__':
    app.run(port=4998, host='0.0.0.0')
