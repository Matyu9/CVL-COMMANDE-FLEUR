import werkzeug
from flask import request, redirect, url_for, render_template


def panel_cogs(database):
    if request.cookies.get('token') != "LOGGIN-SUCCESS":
        return redirect(url_for('login'))
    return "tteeedt"
