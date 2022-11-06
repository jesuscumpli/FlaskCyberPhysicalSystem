import sys

from repositories.heartbeats_devices import get_last_heartbeat_from_device
from repositories.logs_devices import get_last_log_device_from_device

sys.path.append("/opt/controlSystem")

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


@routes.route('/api/devices/info', methods=["GET"])
def api_devices_info():
    if not is_logged():
        return redirect("/login")
    devices = get_all_devices()
    for device in devices:
        last_heartbeat = get_last_heartbeat_from_device(device["_id"]["$oid"])
        last_log = get_last_log_device_from_device(device["_id"]["$oid"])
        device["last_heartbeat"] = last_heartbeat
        device["last_log"] = last_log
    return jsonify({"devices": devices})


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
        IP_heartbeat = form_data.get("ip_heartbeat")
        IP_data = form_data.get("ip_data")
        port_data = form_data.get("port_data")
        IP_operation = form_data.get("ip_operation")
        port_operation = form_data.get("port_operation")
        public_key = files.get("public_key")
        longitude = form_data.get("longitude")
        latitude = form_data.get("latitude")

        if not name or name == "":
            flash("Nombre del dispoisitivo no válido")
            return redirect(request.url)
        if not type or type == "":
            flash("Tipo no definido. Por favor, selecciona el tipo de dispositivo.")
            return redirect(request.url)
        if not IP_heartbeat or IP_heartbeat == "":
            flash("IP Heartbeat no válida. Por favor, define la IP del dispositivo.")
            return redirect(request.url)
        if not IP_data or IP_data == "":
            flash("IP Data no válida. Por favor, define la IP del dispositivo.")
            return redirect(request.url)
        if not port_data or port_data == "":
            flash("Puerto de datos no definido. Por favor, defina el puerto.")
            return redirect(request.url)
        if not IP_operation or IP_operation == "":
            flash("IP Operation no válida. Por favor, define la IP del dispositivo.")
            return redirect(request.url)
        if not port_operation or port_operation == "":
            flash("Puerto de operaciones no definido. Por favor, defina el puerto.")
            return redirect(request.url)
        try:
            socket.inet_aton(IP_heartbeat)
            socket.inet_aton(IP_data)
            socket.inet_aton(IP_operation)
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

        port_data = int(port_data)
        port_operation = int(port_operation)
        inserted = insert_device(name, type, IP_heartbeat, IP_data, port_data, IP_operation, port_operation, public_key_bytes, longitude, latitude, session["username"])
        if inserted:
            insert_log_user(session["username"], "register_device",
                            "Ha registrado el dispositivo '" + name + "' en el sistema")
            return redirect("/devices")
        else:
            flash("No se ha insertado correctamente. Por favor, vuelve a añadir el dispositivo.")
            return redirect(request.url)

    return redirect("/login")


@routes.route('/edit_device/<device_id>', methods=["GET", "POST"])
def edit_device(device_id):
    if not is_logged():
        return redirect("/login")
    if request.method == "GET":
        device = get_device_by_id(device_id)
        return render_template("edit_device.html", device=device)

    elif request.method == "POST":

        form_data = request.form
        files = request.files

        name = form_data.get("name")
        type = form_data.get("type")
        IP_heartbeat = form_data.get("ip_heartbeat")
        IP_data = form_data.get("ip_data")
        port_data = form_data.get("port_data")
        IP_operation = form_data.get("ip_operation")
        port_operation = form_data.get("port_operation")
        public_key = files.get("public_key")
        longitude = form_data.get("longitude")
        latitude = form_data.get("latitude")

        if not name or name == "":
            flash("Nombre del dispoisitivo no válido")
            return redirect(request.url)
        if not type or type == "":
            flash("Tipo no definido. Por favor, selecciona el tipo de dispositivo.")
            return redirect(request.url)
        if not IP_heartbeat or IP_heartbeat == "":
            flash("IP Heartbeat no válida. Por favor, define la IP del dispositivo.")
            return redirect(request.url)
        if not IP_data or IP_data == "":
            flash("IP Data no válida. Por favor, define la IP del dispositivo.")
            return redirect(request.url)
        if not port_data or port_data == "":
            flash("Puerto de datos no definido. Por favor, defina el puerto.")
            return redirect(request.url)
        if not IP_operation or IP_operation == "":
            flash("IP Operation no válida. Por favor, define la IP del dispositivo.")
            return redirect(request.url)
        if not port_operation or port_operation == "":
            flash("Puerto de operaciones no definido. Por favor, defina el puerto.")
            return redirect(request.url)
        try:
            socket.inet_aton(IP_heartbeat)
            socket.inet_aton(IP_data)
            socket.inet_aton(IP_operation)
        except socket.error:
            flash("IP no válida. Por favor, define la IP del dispositivo.")
            return redirect(request.url)

        public_key_bytes = None
        if public_key:
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

        port_data = int(port_data)
        port_operation = int(port_operation)
        updated = update_device(device_id, name, type, IP_heartbeat, IP_data, port_data, IP_operation, port_operation, public_key_bytes, longitude, latitude, session["username"])
        if updated:
            insert_log_user(session["username"], "update_device",
                            "Ha cambiado la configuración del dispositivo '" + name + "'")
            return redirect("/devices")
        else:
            flash("No se ha actualizado correctamente. Por favor, vuelve a intentarlo.")
            return redirect(request.url)

    return redirect("/login")
