import werkzeug
from flask import request, redirect, url_for, render_template, make_response


def login_cogs(database):
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        password = request.form["passwd"]

        # Je fais juste une verification d'un password pour pas me casser le crane
        if password == "CVL-rosa-STVALENTIN2023!":
            resp = make_response(redirect(url_for("panel")))
            resp.set_cookie("token", "LOGGIN-SUCCESS")
            return resp
        else:
            return redirect(url_for('login'))
