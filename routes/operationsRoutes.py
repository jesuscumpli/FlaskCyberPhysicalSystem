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
from encryption.functions import *
from encryption.encryption import *
from encryption.config import *
import logging
logging.basicConfig(level=logging.INFO)

def send_data(data, ip_to_send, port_to_send, encrypt_operation=False, public_key_objective=None):
    result = False
    if encrypt_operation:
        data = encrypt_message(data, public_key_objective)
    else:
        data = data.encode("ISO-8859-1")

    private_key = load_private_key("/opt/controlSystem/encryption/PRIVATE_KEY")
    signature = firm_data(data, private_key)
    message = {"ip_control_system": IP_CONTROL_SYSTEM, "data": data.decode("ISO-8859-1"), "signature": signature.decode("ISO-8859-1")}
    message = json.dumps(message)
    message += "\n"
    message = message.encode("ISO-8859-1")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip_to_send, port_to_send))
        s.sendall(message)
        response = s.recv(1024)
        logging.info("ACK: " + str(response))
        if "OK" in response.decode():
            result = True
        # result = True
    return result


def encrypt_message(message_decrypted, public_key_objective):
    private_key = load_private_key("/opt/controlSystem/encryption/PRIVATE_KEY")
    public_key = load_public_key("/opt/controlSystem/encryption/PUBLIC_KEY")

    encryptor = Encryption(private_key, public_key)
    encrypted_msg = encryptor.encrypt(message_decrypted, public_key_objective)
    return encrypted_msg


@routes.route('/send_operation/<device_id>', methods=["POST"])
def send_operation(device_id):
    if not is_logged():
        return redirect("/login")
    device = get_device_by_id(device_id)
    type_device = device["type"]
    form_data = request.form
    data_to_send = {}
    if type_device == "temperature":
        data_to_send["scale_temperature"] = form_data["scale_temperature"]
    elif type_device == "humidity":
        data_to_send["scale_humidity"] = form_data["scale_humidity"]
    elif type_device == "smart_meter":
        data_to_send["scale_smart_meter"] = form_data["scale_smart_meter"]

    ip_operation = device["IP_operation"]
    port_operation = device["port_operation"]
    encrypt_operation = device["encrypt_operation"]
    data_to_send = json.dumps(data_to_send)

    public_key_objective_bytes = device["public_key"]["$binary"]["base64"]
    public_key_objective_bytes = base64.b64decode(public_key_objective_bytes)
    public_key_objective = load_public_key_from_bytes(public_key_objective_bytes)

    result = send_data(data_to_send, ip_operation, port_operation, encrypt_operation=encrypt_operation, public_key_objective=public_key_objective)
    if not result:
        flash("ERROR: No se ha enviado correctamente el resultado")
    else:
        flash("SUCCESS: Operacion realizado con éxito!")
    return redirect("/logs_device/" + device_id)
