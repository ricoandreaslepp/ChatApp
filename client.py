from threading import Thread
from logger import log


class Client(Thread):

    def __init__(self, conn, addr, name):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.name = name  # currently used as the only identifier

    # 1) send client closing information
    # 2) remove client from Server.__connections
    # 3) log that client exited
    def disconnect(self):
        try:
            self.conn.send("\n\nServer closing connection...".encode())
        except BrokenPipeError:
            pass

        self.conn.close()

        Server.remove_connection(self)
        log.info(f"{self.name} {self.addr} closed connection")

    # check for messages while you were logged out
    def check_messages(self):
        pass

    # Thread method, that runs itself
    def run(self):
        self.conn.send("Successfully connected to server...\n\n".encode())
        Server.motd(self.conn)

        try:
            while True:
                self.conn.send(f"[{self.name}]: ".encode())
                data = self.conn.recv(1024).decode().strip()

                if data == "":
                    break

                # log names for localhost testing
                # log.data_transfer([self.name, "server", data])

                # do something
                for client in Server.connections():
                    if client.name != self.name:
                        client.conn.send(f"\r[{self.name}]: {data}\n".encode())
                        client.conn.send(f"[{client.name}]: ".encode())  # restore their screen
                        log.data_transfer([client.name, "server", data])

        except BrokenPipeError:
            pass
        except Exception as e:
            log.info(e)

        self.disconnect()
