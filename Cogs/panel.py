import werkzeug
from flask import request, redirect, url_for, render_template


def panel_index_cogs(database):
    if request.cookies.get('token') != "LOGGIN-SUCCESS":
        return redirect(url_for('login'))

    commande_value = {
        'nb_commande': len(database.select(body='SELECT * FROM commande', args=None)),
        'nb_commande_distribuée': len(database.select(body='SELECT * FROM commande WHERE distribué=TRUE', args=None)),
        'nb_commande_impayée': len(database.select(body='SELECT * FROM commande WHERE paye=FALSE', args=None)),
        'nb_commande_a_distrib_en_classe': len(database.select(body='SELECT * FROM commande WHERE paye=TRUE & '
                                                                    'commande.need_to_be_receive_by_cvl=TRUE',
                                                               args=None))
    }

    list_commandes = database.select(body='SELECT * FROM commande', args=None, number_of_data=10)

    return render_template('panel/index.html', commande_value=commande_value, list_commandes=list_commandes)


def panel_show_commande_cogs(database):
    if request.cookies.get('token') != "LOGGIN-SUCCESS":
        return redirect(url_for('login'))

    list_commandes = database.select('SELECT * FROM commande', None)

    return render_template('panel/show_commande.html', list_commandes=list_commandes)


def panel_show_specifique_commande_cogs(database, id):
    if request.cookies.get('token') != "LOGGIN-SUCCESS":
        return redirect(url_for('login'))

    specifique_commande = database.select('''SELECT * FROM commande WHERE id=%s''', id, number_of_data=1)

    return render_template('panel/show_special_commande.html', specifique_commande=specifique_commande)

