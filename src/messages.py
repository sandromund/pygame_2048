import socket


class Connection:

    def __init__(self, tcp_ip: str, tcp_port: int):
        self.socket = None
        self.ip = tcp_ip
        self.port = tcp_port
        self.buffer = 1024
        self.mapping = self.get_direction_mapping()
        self.data = None

    @staticmethod
    def get_direction_mapping():
        return {
            "up": b"\x01\x00",
            "right": b"\x01\x01",
            "left": b"\x01\x02",
            "down": b"\x01\x03",
            "quit": b"\x01\x04"
        }

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        self.data = self.socket.recv(self.buffer)

    def disconnect(self):
        self.socket.close()

    def sent_move(self, direction):
        self.socket.send(self.mapping[direction])


if __name__ == '__main__':
    conn = Connection(tcp_ip='depenbrock.ddns.net',
                      tcp_port=48080)
    conn.connect()
    print(conn.data)
    conn.sent_move("up")
