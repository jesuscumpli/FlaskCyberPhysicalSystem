import hashlib
from flask import render_template, session, redirect, request, flash
from utils import is_logged
from . import routes
from repositories.users import *
from repositories.devices import *
from repositories.logs_users import *
from encryption.functions import *
import socket
from flask import jsonify


@routes.route('/devices', methods=["GET"])
def devices():
    if not is_logged():
        return redirect("/login")
    devices = get_all_devices()
    return render_template("devices.html", devices=devices)


@routes.route('/delete/device/<device_id>', methods=["POST"])
def delete_device_by_id(device_id):
    if not is_logged():
        return redirect("/login")
    device_data = get_device_by_id(device_id)
    if device_data:
        result = delete_device(device_id)
        insert_log_user(session["username"], "delete_device",
                        "Ha eliminado el dispositivo '" + device_data["name"] + "' en el sistema")
        return jsonify(success=True, status_code=200)

    return jsonify({'error': 'No se ha podido eliminar correctamente'}), 400


@routes.route('/new_device', methods=["GET", "POST"])
def new_device():
    if not is_logged():
        return redirect("/login")
    if request.method == "GET":
        return render_template("new_device.html")
    elif request.method == "POST":
        form_data = request.form
        files = request.files

        name = form_data.get("name")
        type = form_data.get("type")
        IP = form_data.get("ip")
        public_key = files.get("public_key")
        longitude = form_data.get("longitude")
        latitude = form_data.get("latitude")

        if not name or name == "":
            flash("Nombre del dispoisitivo no válido")
            return redirect(request.url)
        if not type or type == "":
            flash("Tipo no definido. Por favor, selecciona el tipo de dispositivo.")
            return redirect(request.url)
        if not IP or IP == "":
            flash("IP no válida. Por favor, define la IP del dispositivo.")
            return redirect(request.url)
        try:
            socket.inet_aton(IP)
        except socket.error:
            flash("IP no válida. Por favor, define la IP del dispositivo.")
            return redirect(request.url)

        if not public_key:
            flash("Clave pública no seleccionada. Por favor, seleccione la clave pública del dispositivo.")
            return redirect(request.url)
        public_key_bytes = public_key.read()
        try:
            public_key = load_public_key_from_bytes(public_key_bytes)
        except:
            flash("Clave pública no válida. Por favor, define la clave pública del dispositivo.")
            return redirect(request.url)

        if not longitude or longitude == "":
            flash("Longitud no válida. Por favor, define la localización correcta del dispositivo.")
            return redirect(request.url)

        if not latitude or latitude == "":
            flash("Latitud no válida. Por favor, define la localización correcta del dispositivo.")
            return redirect(request.url)

        inserted = insert_device(name, type, IP, public_key_bytes, longitude, latitude, session["username"])
        if inserted:
            insert_log_user(session["username"], "register_device",
                            "Ha registrado el dispositivo '" + name + "' en el sistema")
            return redirect("/devices")
        else:
            flash("No se ha insertado correctamente. Por favor, vuelve a añadir el dispositivo.")
            return redirect(request.url)

    return redirect("/login")
