from socketserver import TCPServer, StreamRequestHandler
import socket
import logging

import sys
sys.path.append("/opt/controlSystem")

import pymongo
logging.basicConfig(level=logging.INFO)
from repositories import devices as repo_devices
from repositories import heartbeats_devices as repo_heartbeats_device
import json

HOST, PORT = "localhost", 8885


class Handler(StreamRequestHandler):
    def handle(self):
        try:
            self.data = self.rfile.readline().strip()
            logging.info("HEARTBEAT FAILED FROM <%s>" % (self.client_address))
            self.get_device_by_IP_address()
            self.save_data()
            logging.info("Se ha guardado correctamente en Base de Datos \n")

        except Exception as e:
            logging.exception(str(e))

    def get_device_by_IP_address(self):
        try:
            self.device = repo_devices.get_device_by_IP(str(self.client_address[0]))
            if not self.device:
                raise Exception()
        except Exception as e:
            raise Exception("No existe el dispositivo con IP: " + self.client_address[0])

    def save_data(self):
        action = "failed"
        log = "heartbeat failed"
        repo_heartbeats_device.insert_heartbeat_device(self.device["_id"]["$oid"], self.device["name"],
                                                       self.device["IP_heartbeat"], action, log, success=False)


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
