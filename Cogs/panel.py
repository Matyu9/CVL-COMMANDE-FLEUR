from flask import request, redirect, url_for, render_template


def panel_index_cogs(database, cookie_config_value):
    if request.cookies.get('token') != cookie_config_value:
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

    return render_template('panel/index.html', commande_value=commande_value,
                           list_commandes=list_commandes)


def panel_show_commande_cogs(database, cookie_config_value):
    if request.cookies.get('token') != cookie_config_value:
        return redirect(url_for('login'))

    list_commandes = database.select('SELECT * FROM commande', None)

    return render_template('panel/show_commande.html', list_commandes=list_commandes, alert=request.args.get('alert'))


def panel_show_specifique_commande_cogs(database, id, cookie_config_value):
    if request.cookies.get('token') != cookie_config_value:
        return redirect(url_for('login'))

    specifique_commande = database.select('''SELECT * FROM commande WHERE id=%s''', id, number_of_data=1)

    return render_template('panel/show_special_commande.html', specifique_commande=specifique_commande)


def panel_edit_commande_cogs(database, cookie_config_value):
    if request.cookies.get('token') != cookie_config_value:
        return redirect(url_for('login'))

    if request.method == 'POST':
        uniqueID = request.form.get('uniqueID')
    else:
        uniqueID = None

    if uniqueID is None:
        # Render la page avec le form
        return render_template('panel/edit_commande.html', specifique_commande=None, uniqueID=None)

    elif uniqueID is not None:
        commande = database.select('''SELECT * FROM commande WHERE code_unique=%s''', uniqueID, 1)
        return render_template('panel/edit_commande.html', specifique_commande=commande,
                               uniqueID=uniqueID)

    return 'Edit Command'


def panel_edit_commande_back_cogs(database, cookie_config_value):
    if request.cookies.get('token') != cookie_config_value:
        return redirect(url_for('login'))

    is_paye = request.form.get('flexCheckPaye') is not None if True else False
    is_distribue = request.form.get('flexCheckDistrib') is not None if True else False
    is_prepare = request.form.get('flexCheckPrepa') is not None if True else False

    database.exec("""UPDATE commande SET paye=%s, distribué=%s, prepare=%s WHERE code_unique=%s""",
                  (is_paye, is_distribue, is_prepare, request.form.get('uniqueID')))

    if is_paye:
        database.exec("""UPDATE commande SET paye_at=CURRENT_TIMESTAMP WHERE code_unique=%s""",
                      request.form.get('uniqueID'))

    return redirect(url_for("panel_edit_commande"), code=307)


def panel_delete_commande_cogs(database, cookie_config_value):
    if request.cookies.get('token') != cookie_config_value:
        return redirect(url_for('login'))

    commande = database.exec('''DELETE FROM commande WHERE code_unique=%s''', request.form.get('uniqueID'))
    return redirect(url_for('panel_show_commande', alert='delete-success'))


def panel_chart_cogs(database, cookie_config_value):
    if request.cookies.get('token') != cookie_config_value:
        return redirect(url_for('login'))

    # Get les datas en fonction des classes
    commande = database.select('''SELECT * FROM commande''', args=None)
    customer_by_classes = {
        'seconde': 0,
        'premiere': 0,
        'term': 0
    }
    nb_command_per_day = {}
    for element in commande:
        if element[6].startswith('2'):
            customer_by_classes['seconde'] += 1
        elif element[6].startswith('1'):
            customer_by_classes['premiere'] += 1
        elif element[6].startswith('T'):
            customer_by_classes['term'] += 1

        date = element[11].strftime("%Y-%m-%d").encode('utf-8').decode('unicode-escape')    # Récupération de la date sans l'heure
        if date in nb_command_per_day:
            nb_command_per_day[date] += 1
        else:
            nb_command_per_day[date] = 1

    print(nb_command_per_day)
    return render_template('panel/chart.html', customer_by_classes=customer_by_classes,
                           nb_command_per_day=nb_command_per_day)
