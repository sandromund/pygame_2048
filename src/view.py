import logging
import time

import pygame
from src.messages import Connection
import numpy as np


class Game:

    def __init__(self, connection):
        self.board = None
        self.connection: Connection = connection
        self.board_background_color = (255, 255, 255)
        self.tile_size = 250
        self.fps = 20
        self.state = None
        self.score = None
        self.board = None

        pygame.init()

        self.screen = pygame.display.set_mode((self.tile_size * 4, self.tile_size * 4))
        self.clock = pygame.time.Clock()

    def draw_board(self):
        self.board = np.array(self.board).reshape((4, 4))
        for i in range(4):
            for j in range(4):
                tile_value = self.board[i][j]
                pygame.draw.rect(surface=self.screen,
                                 color=self.get_tile_color(tile_value),
                                 rect=(j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size))
                if tile_value > 1:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(tile_value), True, (0, 0, 0))
                    text_rect = text.get_rect(
                        center=(j * self.tile_size + self.tile_size // 2, i * self.tile_size + self.tile_size // 2))
                    self.screen.blit(text, text_rect)

    @staticmethod
    def get_tile_color(tile_value):
        return {
            1: (205, 192, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46)
        }.get(tile_value, (0, 0, 0))

    def run(self):

        logging.info("Connecting to server...")
        answer = self.connection.connect()
        logging.info("Connection successful.")

        self.state, self.score, self.board = self.connection.decode_server_message(answer)

        pygame.display.set_caption('2048 Game')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            keys = pygame.key.get_pressed()
            delay = 0.1
            if keys[pygame.K_UP]:
                answer = self.connection.sent_move(direction='up')
                time.sleep(delay)
            elif keys[pygame.K_DOWN]:
                answer = self.connection.sent_move(direction='down')
                time.sleep(delay)
            elif keys[pygame.K_LEFT]:
                answer = self.connection.sent_move(direction='left')
                time.sleep(delay)
            elif keys[pygame.K_RIGHT]:
                answer = self.connection.sent_move(direction='right')
                time.sleep(delay)
            elif keys[pygame.K_ESCAPE]:
                self.connection.sent_move(direction='quit')
                break

            self.state, self.score, self.board = self.connection.decode_server_message(answer)

            if self.state == 1:
                print("Won! -> Score:", self.score)
                exit()

            if self.state > 1:
                print("Game Over! -> Score:", self.score)
                exit()

            self.screen.fill(self.board_background_color)
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(self.fps)

