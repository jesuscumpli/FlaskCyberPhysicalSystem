from socketserver import TCPServer, StreamRequestHandler
import socket
import logging

import sys
sys.path.append("/opt/controlSystem")

logging.basicConfig(level=logging.INFO)
from repositories import devices as repo_devices
from repositories import logs_devices as repo_logs_device
import json
from encryption.encryption import Encryption
from encryption.functions import *
import base64

HOST, PORT = "localhost", 8887


class Handler(StreamRequestHandler):
    def handle(self):
        try:
            self.data = self.rfile.readline().strip()
            logging.info("DATOS RECIBIDOS DE <%s>: %s" % (self.client_address, self.data))
            self.decode_message_info()
            logging.info("MENSAJE: <%s>" % self.message)
            self.get_device_by_IP_address()
            self.verify_data()
            self.data = self.message["data"]
            self.normalize_data()
            self.save_data()
            logging.info("Se ha guardado correctamente en Base de Datos \n")

        except Exception as e:
            logging.exception(str(e))

    def decode_message_info(self):
        message = self.data
        message = message.decode("ISO-8859-1")
        message = json.loads(message)
        self.message = message

    def get_device_by_IP_address(self):
        try:
            # self.device = repo_devices.get_device_by_IP(str(self.client_address[0]))
            # if not self.device:
            #     raise Exception()
            self.device = repo_devices.get_device_by_IP_data(str(self.message["IP_data"]))
            if not self.device:
                raise Exception()
        except Exception as e:
            raise Exception("No existe el dispositivo con IP: " + self.message["IP_data"])

    def verify_data(self):
        signature = self.message["signature"].encode("ISO-8859-1")
        public_key_objective_bytes = self.device["public_key"]["$binary"]["base64"]
        public_key_objective_bytes = base64.b64decode(public_key_objective_bytes)
        public_key_objective = load_public_key_from_bytes(public_key_objective_bytes)
        data = self.message["data"].encode("ISO-8859-1")
        verify_signature(signature, data, public_key_objective)
    def normalize_data(self):
        data = self.data
        try:
            data = json.loads(data)
        except Exception as e:
            logging.exception(str(e))

        if isinstance(data, str):
            data = {"message": data, "json": None, "list": None}
        elif isinstance(data, dict):
            data = {"message": data, "json": data, "list": None}
        elif isinstance(data, list):
            data = {"message": None, "json": None, "list": data}
        self.data = json.dumps(data)

    def save_data(self):
        action = "data"
        repo_logs_device.insert_log_device(self.device["_id"]["$oid"], self.device["name"], self.device["IP"], action,
                                           self.data)


class Server(TCPServer):
    SYSTEMD_FIRST_SOCKET_FD = 3

    def __init__(self, server_address, handler_cls):
        TCPServer.__init__(self, server_address, handler_cls, bind_and_activate=False)
        self.socket = socket.fromfd(self.SYSTEMD_FIRST_SOCKET_FD, self.address_family, self.socket_type)


if __name__ == "__main__":
    server = Server((HOST, PORT), Handler)
    print("Loading server")
    server.serve_forever()
    logging.info("Success")
    print("Successs")
