import socket


class Connection:

    def __init__(self, tcp_ip, tcp_port):
        self.socket = None
        self.ip = tcp_ip
        self.port = int(tcp_port)
        self.buffer = 1024
        self.mapping = self.get_direction_mapping()
        self.data = None

    @staticmethod
    def get_direction_mapping():
        """
        Client -> Server (2 B)
            1 Byte Type: 0x1
            1 Byte Direction:
                Up: 0x0
                Right: 0x1
                Down: 0x2
                Left 0x3
                Quit: 0x4
        """
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
        self.data = self.socket.recv(self.buffer)

    def disconnect(self):
        self.socket.close()

    def sent_move(self, direction):
        self.socket.send(self.mapping[direction])

    @staticmethod
    def decode_server_message(byte_str):
        """
        Server -> Client (22 B)
            1 Byte Type: 0x0
            1 Byte State:
                Playing: 0x0
                Won: 0x1
                Lost: 0x2
            4 Byte Score: unsigned int
            16 Byte Board: exponent of powers of 2

        return :
            state   0 := playing
                    1 := won
                    2 := lost
            score  int
            board  list[int] with len(board) == 16
                    no value in a fild is represented as 1
        """
        board_bytes = byte_str[6:]
        state = int.from_bytes(byte_str[1:2], byteorder='little', signed=False)
        score = int.from_bytes(byte_str[2:6], byteorder='little', signed=False)
        board = [2 ** int(byte_str[i]) for i in range(len(board_bytes))]

        return state, score, board
