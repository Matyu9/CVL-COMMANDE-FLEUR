from werkzeug.exceptions import BadRequestKeyError
from flask import request, redirect, url_for, render_template
from uuid import uuid3, uuid1


def commande_cogs(database):
    if not request.form['nd'] or not request.form["pd"] or not request.form["cd"] or not request.form['message']:
        return redirect(url_for("home"))

    try:
        if request.form['themself'] == 'on':
            need_to_be_receive_by_cvl = False
        else:
            need_to_be_receive_by_cvl = True
    except BadRequestKeyError:
        need_to_be_receive_by_cvl = True

    code_unique = str(uuid3(uuid1(), str(uuid1())))
    code_unique = code_unique[9]+code_unique[10]+code_unique[11]+code_unique[12]

    database.exec("""INSERT INTO commande(nom_destinataire, prenom_destinataire, classe_destinataire, 
    nom_envoyeur, prenom_envoyeur, classe_envoyeur, message, need_to_be_receive_by_cvl, code_unique) VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (request.form['nd'], request.form['pd'], request.form['cd'],
                                              request.form['ne'], request.form['pe'], request.form['ce'],
                                              request.form['message'], need_to_be_receive_by_cvl, code_unique))

    return render_template('commande.html', need_to_be_receive_by_cvl=need_to_be_receive_by_cvl,
                           nd=request.form['nd'], pd=request.form['pd'], code_unique=code_unique)
