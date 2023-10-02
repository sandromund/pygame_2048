from dotenv import dotenv_values

from src.messages import Connection

if __name__ == '__main__':
    secrets = dotenv_values(".env")
    tcp_ip = secrets.get("TCP_IP")
    tcp_port = secrets.get("TCP_PORT")

    conn = Connection(tcp_ip=tcp_ip, tcp_port=tcp_port)
    conn.connect()
    conn.sent_move("quit")
    state, score, board = conn.decode_server_message(conn.data)
    conn.disconnect()
