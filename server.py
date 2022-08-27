# for future use
# import uuid; uuid = str(uuid.uuid4())
# import colorama

from config import HOST, PORT
from client import Client
from logger import log
import socket


class Server:

    __connections = []

    def __init__(self):
        self.IP = self.get_ip()
        self.run_server()

    def __del__(self):
        pass

    # methods related to the tracking of connections
    @classmethod
    def connections(cls):
        return cls.__connections

    @classmethod
    def add_connection(cls, client):
        cls.__connections.append(client)

    @classmethod
    def remove_connection(cls, client):
        cls.__connections.remove(client)
    # - - - - -

    # print the server's MOTD
    @staticmethod
    def motd(conn):
        msg = f"""
        not implemented yet
        
        
"""
        conn.send(msg.encode())

    # try to get LAN ip from router
    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
        s.close()
        return ip

    # needs some functionality
    # currently just a template
    def login_loop(self, conn):
        conn.send("login: ".encode())
        name = conn.recv(1024).decode().strip()
        return name

    # main server loops
    def run_server(self):
        try:
            self.server_loop()
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            pass

    def server_loop(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        log.info(f"Server with IP {self.IP} on port {PORT}...")

        server.listen(1000)
        log.info(f"Server listening for connections...")
        while True:
            conn, addr = server.accept()

            name = self.login_loop(conn)

            new_client = Client(conn, addr, name)
            new_client.start()

            log.info(f"{new_client.name} connected from {new_client.addr}.")

            self.add_connection(new_client)
            print(self.connections())


if __name__ == '__main__':
    s = Server()
