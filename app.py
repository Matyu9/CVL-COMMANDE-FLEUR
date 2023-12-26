from flask import Flask, render_template
from cantinaUtils.Database import DataBase
from Cogs.login import login_cogs
from Cogs.commande import commande_cogs
from Cogs.panel import panel_index_cogs, panel_show_commande_cogs, panel_show_specifique_commande_cogs
import os
import json


file_path = os.path.abspath(os.path.join(os.getcwd(), "config.json"))

# Lecture du fichier JSON
with open(file_path, 'r') as file:
    config_data = json.load(file)

app = Flask(__name__)
database = DataBase(user=config_data['database_username'], password=config_data['database_password'], host="localhost",
                    port=3306, database=config_data['database_name'])
database.connection()
database.exec("""CREATE TABLE IF NOT EXISTS commande(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
nom_destinataire TEXT NOT NULL, prenom_destinataire TEXT NOT NULL, classe_destinataire TEXT NOT NULL, 
nom_envoyeur TEXT NOT NULL, prenom_envoyeur TEXT NOT NULL, classe_envoyeur TEXT NOT NULL, message TEXT(150), 
need_to_be_receive_by_cvl BOOL, paye BOOL DEFAULT FALSE, paye_at TIMESTAMP, 
commander_le TIMESTAMP DEFAULT CURRENT_TIMESTAMP, distribué BOOL DEFAULT FALSE NOT NULL, code_unique TEXT, 
prepare BOOL)""", None)


@app.route('/')
def home():
    return render_template('home-no-login.html')


@app.route('/commande', methods=['POST'])
def commande():
    return commande_cogs(database)


@app.route('/login', methods=['POST', 'GET'])
def login():
    return login_cogs(database)


@app.route('/panel', methods=['POST', 'GET'])
def panel_home():
    return panel_index_cogs(database)


@app.route('/panel/show_commande', methods=['POST', 'GET'])
def panel_show_commande():
    return panel_show_commande_cogs(database)


@app.route('/panel/show_commande/<id>', methods=['POST', 'GET'])
def panel_show_specifique_commande(id):
    return panel_show_specifique_commande_cogs(database, id)


if __name__ == '__main__':
    app.run(port=4998, host='0.0.0.0')
