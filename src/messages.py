import socket


class Connection:

    def __init__(self, tcp_ip, tcp_port):
        self.socket = None
        self.ip = tcp_ip
        self.port = int(tcp_port)
        self.buffer = 1024
        self.mapping = self.get_direction_mapping()

    @staticmethod
    def get_direction_mapping():
        return {
            "up": b"\x01\x00",
            "right": b"\x01\x01",
            "left": b"\x01\x03",
            "down": b"\x01\x02",
            "quit": b"\x01\x04"
        }

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        return self.socket.recv(self.buffer)

    def disconnect(self):
        self.socket.close()

    def sent_move(self, direction):
        self.socket.send(self.mapping[direction])
        return self.socket.recv(self.buffer)

    @staticmethod
    def decode_server_message(byte_str):
        board_bytes = byte_str[6:]
        state = int.from_bytes(byte_str[1:2], byteorder='little', signed=False)
        score = int.from_bytes(byte_str[2:6], byteorder='little', signed=False)
        board = [2 ** int(board_bytes[i]) for i in range(len(board_bytes))]
        return state, score, board
