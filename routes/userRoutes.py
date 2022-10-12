import hashlib
from flask import render_template, session, redirect, request, flash
from utils import is_logged
from . import routes
from repositories.users import *
from repositories.logs_users import *
import os

'''
FILE WITH ROUTES ABOUT LOGIN, REGISTER AND LOGOUT USERS FROM WEB PAGE
'''


@routes.route('/')
def index():
    if not is_logged():
        return redirect("/login")
    return redirect("/home")


@routes.route('/logout', methods=["GET"])
def logout():
    session["username"] = None
    return redirect("/login")


@routes.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        username = form.get("username")
        password = form.get("password")
        # Check data
        if username is None:
            flash("Nombre de usuario no definido")
        elif password is None:
            flash("Contraseña no definida")
        else:

            result = find_user_by_username(username)
            if result:
                # Get user info
                salt = result["salt"]
                password_salted = password.encode() + salt
                password_hashed = hashlib.sha256(password_salted).hexdigest()
                password_correct = result["password"]

                if password_hashed == password_correct:
                    update_user_login_date(username)
                    insert_log_user(username, "login", "Ha iniciado sesión")
                    session["username"] = username
                    return redirect("/home")
                else:
                    flash("Los datos introducidos son incorrectos.")
            else:
                flash("Los datos introducidos son incorrectos.")
    return render_template("login.html")


@routes.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = request.form
        username = form.get("username")
        password1 = form.get("password1")
        password2 = form.get("password2")
        # Check data
        if username is None:
            flash("Nombre de usuario no definido")
        elif password1 is None or password2 is None:
            flash("Contraseña no definida")
        elif password1 != password2:
            flash("Las contraseñas no coinciden")
        elif find_user_by_username(username):
            flash("Usuario ya existe")
        else:
            # Create user
            salt = os.urandom(16)
            password_salted = password1.encode() + salt
            password_hashed = hashlib.sha256(password_salted).hexdigest()
            inserted = insert_user(username, salt, password_hashed)
            # Register Success
            if inserted:
                insert_log_user(username, "register", "Se ha registrado en el sistema")
                session["username"] = username
                return redirect("/home")
            # Error inserting the values
            else:
                flash("Error interno: No se ha podido crear el usuario. Por favor, vuelve a intentarlo.")
    return render_template("register.html")
