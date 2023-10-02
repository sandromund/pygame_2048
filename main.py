from dotenv import dotenv_values

from src.messages import Connection
from src.view import Game

if __name__ == '__main__':
    secrets = dotenv_values(".env")
    game = Game(connection=Connection(tcp_ip=secrets.get("TCP_IP"),
                                      tcp_port=secrets.get("TCP_PORT")))
    game.run()
