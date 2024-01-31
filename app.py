from flask import Flask
from cantinaUtils.Database import DataBase
from Cogs.home import home_cogs
from Cogs.login import login_cogs
from Cogs.commande import commande_cogs
from Cogs.panel import (panel_index_cogs, panel_show_commande_cogs, panel_show_specifique_commande_cogs,
                        panel_edit_commande_cogs, panel_edit_commande_back_cogs, panel_chart_cogs,
                        panel_delete_commande_cogs, panel_stock_cogs, panel_stock_add_cogs)
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
prepare BOOL DEFAULT FALSE)""", None)
database.exec("""CREATE TABLE IF NOT EXISTS stock(item_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
item_name TEXT NOT NULL, item_beggining_value INT NOT NULL, item_current_value INT NOT NULL, 
last_update TIMESTAMP DEFAULT current_timestamp)""", None)
database.exec("""CREATE TABLE IF NOT EXISTS telemetry(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
nom_telemetry TEXT NOT NULL, data_telemetry TEXT NOT NULL)""", None)


@app.route('/')
def home():
    return home_cogs(database)


@app.route('/commande', methods=['POST'])
def commande():
    return commande_cogs(database)


@app.route('/login', methods=['POST', 'GET'])
def login():
    return login_cogs(config_data['login_password'], config_data['login_cookie'])


@app.route('/panel', methods=['POST', 'GET'])
def panel_home():
    return panel_index_cogs(database, config_data['login_cookie'])


@app.route('/panel/show_commande', methods=['POST', 'GET'])
def panel_show_commande():
    return panel_show_commande_cogs(database, config_data['login_cookie'])


@app.route('/panel/show_commande/<id>', methods=['POST', 'GET'])
def panel_show_specifique_commande(id):
    return panel_show_specifique_commande_cogs(database, id, config_data['login_cookie'])


@app.route('/panel/edit_commande', methods=['POST', 'GET'])
def panel_edit_commande():
    return panel_edit_commande_cogs(database, config_data['login_cookie'])


@app.route('/panel/edit_commande/edit', methods=['POST'])
def panel_edit_commande_back():
    return panel_edit_commande_back_cogs(database, config_data['login_cookie'])


@app.route('/panel/delete_commande/', methods=['POST'])
def panel_delete_commande():
    return panel_delete_commande_cogs(database, config_data['login_cookie'])


@app.route('/panel/stock', methods=['GET'])
def panel_stock():
    return panel_stock_cogs(database, config_data['login_cookie'])


@app.route('/panel/stock/add', methods=['POST', 'GET'])
def panel_stock_add():
    return panel_stock_add_cogs(database, config_data['login_cookie'])


@app.route('/panel/chart')
def panel_chart():
    return panel_chart_cogs(database, config_data['login_cookie'])


if __name__ == '__main__':
    app.run(port=config_data['database_port'], host='0.0.0.0', debug=True)
