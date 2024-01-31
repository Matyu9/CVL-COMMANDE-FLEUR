from flask import request, redirect, url_for, render_template


def panel_index_cogs(database, cookie_config_value):
    if request.cookies.get('token') != cookie_config_value:
        return redirect(url_for('login'))

    commande_value = {
        'nb_commande': len(database.select(body='SELECT * FROM commande', args=None)),
        'nb_fleur_restante': database.select(body='SELECT item_current_value FROM stock WHERE item_name="fleur-1"',
                                             args=None, number_of_data=1)[0],
        'nb_commande_impayée': len(database.select(body='SELECT * FROM commande WHERE paye=FALSE', args=None)),
        'nb_commande_a_distrib_en_classe': len(database.select(body='SELECT * FROM commande WHERE paye=TRUE & '
                                                                    'commande.need_to_be_receive_by_cvl=TRUE',
                                                               args=None))
    }

    list_commandes = database.select(body='SELECT * FROM commande', args=None, number_of_data=10)
    status_commande = database.select(body='SELECT * FROM config WHERE config_name="can_order"', args=None)

    return render_template('panel/index.html', commande_value=commande_value,
                           list_commandes=list_commandes, status_commande=status_commande)


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

    action = request.form.get('action')

    if action == 'paye':
        database.exec("""UPDATE commande SET paye=%s WHERE code_unique=%s""",
                      (1, request.form.get('uniqueID')))
        database.exec("""UPDATE commande SET paye_at=CURRENT_TIMESTAMP WHERE code_unique=%s""",
                      request.form.get('uniqueID'))
        database.exec("""UPDATE stock SET item_current_value=item_current_value-1 WHERE item_name='fleur-1'""", None)
    elif action == 'distrib':
        database.exec("""UPDATE commande SET distribué=%s WHERE code_unique=%s""",
                      (1, request.form.get('uniqueID')))
    elif action == 'prepa':
        database.exec("""UPDATE commande SET prepare=%s WHERE code_unique=%s""",
                      (1, request.form.get('uniqueID')))

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


def panel_stock_cogs(database, cookie_config_value):
    if request.cookies.get('token') != cookie_config_value:
        return redirect(url_for('login'))

    if request.method == 'GET':
        data1 = database.select(body='SELECT item_beggining_value FROM stock WHERE item_name="fleur-1"', args=None,
                                number_of_data=1)
        data2 = database.select(body='SELECT item_current_value FROM stock WHERE item_name="fleur-1"', args=None,
                                number_of_data=1)
        data3 = database.select(body='SELECT item_name FROM stock', args=None)

        stock_value = {
            'nb_fleur1_start': data1[0] if data1 is not None else 'Aucune donnée',
            'nb_fleur1_restante': data2[0] if data2 is not None else 'Aucune donnée',
            'item_name': data3
        }

        return render_template('panel/stock.html', stock_value=stock_value)

    elif request.method == 'POST':
        database.exec('UPDATE stock SET item_current_value=item_current_value+%s, '
                      'item_beggining_value=item_beggining_value+%s, last_update=CURRENT_TIMESTAMP WHERE item_name=%s',
                      (request.form.get('item_to_add'), request.form.get('item_to_add'), request.form.get('item_name')))

        return redirect(url_for('panel_home'))


def panel_status_order_cogs(database, cookie_config_value):
    if request.cookies.get('token') != cookie_config_value:
        return redirect(url_for('login'))

    database.exec("""UPDATE config SET config_data=NOT config_data WHERE config_name='can_order'""", None)

    return redirect(url_for('panel_home'))
