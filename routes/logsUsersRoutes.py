import hashlib
from flask import render_template, session, redirect, request, flash
from utils import is_logged
from . import routes
from repositories.users import *
from repositories.devices import *
from repositories.logs_users import *
from repositories.logs_devices import *
from encryption.functions import *
import socket
from flask import jsonify

@routes.route('/logs_users', methods=["GET"])
def logs_users():
    if not is_logged():
        return redirect("/login")
    logs_users = get_all_logs_user_date_desc()
    return render_template("logs_users.html", logs_users=logs_users)