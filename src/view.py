import pygame
from messages import Connection


class Game:

    def __init__(self):
        self.board = None
        self.connection: Connection = None

        self.board_background_color = (255, 255, 255)
        self.tile_size = 250
        self.fps = 60

        pygame.init()

        self.screen = pygame.display.set_mode((self.tile_size * 4, self.tile_size * 4))
        self.clock = pygame.time.Clock()

    def draw_board(self):
        for i in range(4):
            for j in range(4):
                tile_value = self.board[(i*4 + j)]
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
        pygame.display.set_caption('2048 Game')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                direction = 'up'
            elif keys[pygame.K_DOWN]:
                direction = 'down'
            elif keys[pygame.K_LEFT]:
                direction = 'left'
            elif keys[pygame.K_RIGHT]:
                direction = 'right'
            else:
                direction = 'quit'

            self.screen.fill(self.board_background_color)
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    game = Game()
    game.board = [1, 1, 4, 1,
                  1, 2, 1, 1,
                  16, 1, 2, 1,
                  1, 8, 1, 1]
    game.run()
