from werkzeug.exceptions import BadRequestKeyError
from flask import render_template, request


def home_cogs(database):
    try:
        if request.args['from'] == 'qr-code':
            database.exec('''INSERT INTO telemetry(nom_telemetry, data_telemetry) VALUES (%s, %s)''',
                          ('user_origin', 'qr-code'))  # Add value 'qrcode' to the table telemetry
        elif request.args['from'] == 'insta':
            database.exec('''INSERT INTO telemetry(nom_telemetry, data_telemetry) VALUES (%s, %s)''',
                          ('user_origin', 'insta'))  # Add value 'insta' to the table telemetry
    except BadRequestKeyError as e:
        database.exec('''INSERT INTO telemetry(nom_telemetry, data_telemetry) VALUES (%s, %s)''',
                      ('user_origin', 'strangers'))  # Add value 'strangers' to the table telemetry

    return render_template('home-no-login.html')
