import pygame
from . import pieces

class Draw:
    def __init__(self, screen, chessboard):
        self.screen = screen
        self.chessboard = chessboard
        screen_height = screen.get_height()
        self.square_size = screen_height // 8
        self.offset_x = 0
        self.offset_y = 0
        self.font = pygame.font.SysFont("Arial", 16)

    def update(self, selected_piece=None, possible_moves=[]):
        self.draw_board()
        if selected_piece:
            self.highlight_square(selected_piece.x, selected_piece.y, color=(255, 255, 153))
        for move in possible_moves:
            self.glow_square(move.xto, move.yto)
        self.draw_pieces()
        self.draw_labels()

    def draw_board(self):
        dark_green = pygame.Color(118, 150, 86)
        light_green = pygame.Color(238, 238, 210)
        colors = [light_green, dark_green]
        for y in range(8):
            for x in range(8):
                color = colors[(x + y) % 2]
                pygame.draw.rect(self.screen, color, pygame.Rect(x * self.square_size + self.offset_x, y * self.square_size + self.offset_y, self.square_size, self.square_size))

    def glow_square(self, x, y):
        inner_color = self.get_square_color(x, y)
        inner_rect = pygame.Rect(x * self.square_size + self.offset_x, y * self.square_size + self.offset_y, self.square_size, self.square_size)
        pygame.draw.rect(self.screen, inner_color, inner_rect)
        pygame.draw.rect(self.screen, pygame.Color("white"), inner_rect, 4)

    def get_square_color(self, x, y):
        if (x + y) % 2 == 0:
            return pygame.Color(238, 238, 210)
        else:
            return pygame.Color(118, 150, 86)

    def highlight_square(self, x, y, color):
        highlight_rect = pygame.Rect(x * self.square_size + self.offset_x, y * self.square_size + self.offset_y, self.square_size, self.square_size)
        pygame.draw.rect(self.screen, color, highlight_rect)

    def draw_pieces(self):
        for y in range(8):
            for x in range(8):
                piece = self.chessboard.get_piece(x, y)
                if piece != 0:
                    piece_image = pygame.image.load(f"assets/{piece.color}{piece.piece_type}.png")
                    piece_image = pygame.transform.scale(piece_image, (int(self.square_size * 0.85), int(self.square_size * 0.85)))
                    piece_rect = piece_image.get_rect()
                    piece_rect.center = (x * self.square_size + self.offset_x + self.square_size // 2, y * self.square_size + self.offset_y + self.square_size // 2)
                    self.screen.blit(piece_image, piece_rect)

    def draw_labels(self):
        for y in range(8):
            label = self.font.render(str(8 - y), True, pygame.Color("black"))
            self.screen.blit(label, (self.offset_x + 5, y * self.square_size + self.offset_y + 5))

        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for x in range(8):
            label = self.font.render(letters[x], True, pygame.Color("black"))
            self.screen.blit(label, (x * self.square_size + self.offset_x + self.square_size - 20, self.offset_y + 8 * self.square_size - 20))
