import hashlib
from flask import render_template, session, redirect, request, flash
from utils import is_logged
from . import routes
from repositories.users import *

@routes.route('/home')
def home():
    if not is_logged():
        return redirect("/login")
    return render_template("home.html")
