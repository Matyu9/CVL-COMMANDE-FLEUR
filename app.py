from flask import Flask, render_template, request, redirect, url_for
from cantinaUtils.Database import DataBase
import os
import json
import werkzeug.exceptions


file_path = os.path.abspath(os.path.join(os.getcwd(), "config.json"))

# Lecture du fichier JSON
with open(file_path, 'r') as file:
    config_data = json.load(file)

app = Flask(__name__)
database = DataBase(user=config_data['database_username'], password=config_data['database_password'],
                                   host="localhost", port=3306, database=config_data['database_name'])
database.connection()
database.exec("""CREATE TABLE IF NOT EXISTS commande(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
nom_destinataire TEXT NOT NULL, prenom_destinataire TEXT NOT NULL, classe_destinataire TEXT NOT NULL, 
nom_envoyeur TEXT NOT NULL, prenom_envoyeur TEXT NOT NULL, classe_envoyeur TEXT NOT NULL, message TEXT(150), 
need_to_be_receive_by_cvl BOOL, commander_le TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""", None)


@app.route('/')
def home():
    return render_template('home-no-login.html')


@app.route('/commande', methods=['POST'])
def commande():
    if not request.form['nd'] or not request.form["pd"] or not request.form["cd"] or not request.form['message']:
        return redirect(url_for("home"))

    try:
        if request.form['themself'] == 'on':
            need_to_be_receive_by_cvl = True
        else:
            need_to_be_receive_by_cvl = False
    except werkzeug.exceptions.BadRequestKeyError:
        need_to_be_receive_by_cvl = False

    database.exec("""INSERT INTO commande(nom_destinataire, prenom_destinataire, classe_destinataire, 
    nom_envoyeur, prenom_envoyeur, classe_envoyeur, message, need_to_be_receive_by_cvl) VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s)""", (request.form['nd'], request.form['pd'], request.form['cd'],
                                          request.form['ne'], request.form['pe'], request.form['ce'],
                                          request.form['message'], need_to_be_receive_by_cvl))

    return render_template('commande.html', need_to_be_receive_by_cvl=need_to_be_receive_by_cvl,
                           nd=request.form['nd'], pd=request.form['pd'])


if __name__ == '__main__':
    app.run(port=4998, host='0.0.0.0')
