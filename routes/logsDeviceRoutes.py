import sys
sys.path.append("/opt/controlSystem")

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

@routes.route('/logs_device/<device_id>', methods=["GET"])
def logs_device(device_id):
    if not is_logged():
        return redirect("/login")
    device = get_device_by_id(device_id)
    logs_device = get_all_logs_from_device(device_id)
    for log in logs_device:
        log = json.loads(log)
        log = log["message"]

    return render_template("logs_device.html", device=device, logs_device=logs_device)