import werkzeug
from flask import request, redirect, url_for, render_template


def commande_cogs(database):
    if not request.form['nd'] or not request.form["pd"] or not request.form["cd"] or not request.form['message']:
        return redirect(url_for("home"))

    try:
        if request.form['themself'] == 'on':
            need_to_be_receive_by_cvl = False
        else:
            need_to_be_receive_by_cvl = True
    except werkzeug.exceptions.BadRequestKeyError:
        need_to_be_receive_by_cvl = True

    database.exec("""INSERT INTO commande(nom_destinataire, prenom_destinataire, classe_destinataire, 
    nom_envoyeur, prenom_envoyeur, classe_envoyeur, message, need_to_be_receive_by_cvl) VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s)""", (request.form['nd'], request.form['pd'], request.form['cd'],
                                          request.form['ne'], request.form['pe'], request.form['ce'],
                                          request.form['message'], need_to_be_receive_by_cvl))

    return render_template('commande.html', need_to_be_receive_by_cvl=need_to_be_receive_by_cvl,
                           nd=request.form['nd'], pd=request.form['pd'])
