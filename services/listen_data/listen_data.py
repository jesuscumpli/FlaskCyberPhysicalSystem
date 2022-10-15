from socketserver import TCPServer, StreamRequestHandler
import socket
import logging
logging.basicConfig(level=logging.INFO)

HOST, PORT = "localhost", 8887

class Handler(StreamRequestHandler):
    def handle(self):
        try:
            self.data = self.rfile.readline().strip()
            logging.info("From <%s>: %s" % (self.client_address, self.data))
        except Exception as e:
            logging.exception(str(e))

class Server(TCPServer):
    SYSTEMD_FIRST_SOCKET_FD = 3

    def __init__(self, server_address, handler_cls):
        TCPServer.__init__(self, server_address, handler_cls, bind_and_activate=False)
        self.socket = socket.fromfd(self.SYSTEMD_FIRST_SOCKET_FD, self.address_family, self.socket_type)


if __name__ == "__main__":
    server = Server((HOST, PORT), Handler)
    server.serve_forever()
    logging.info("Success")
    print("Successs")