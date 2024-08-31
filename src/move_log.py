import pygame
import pygame.font
from . import pieces

class MoveLog:
    def __init__(self, screen):
        self.screen = screen
        self.moves = []
        self.font = pygame.font.SysFont("Arial", 18)
        self.log_width = 150
        self.log_height = screen.get_height()
        self.log_bg_color = pygame.Color(225, 225, 200)
        self.white_text_color = pygame.Color('white')
        self.black_text_color = pygame.Color('black')
        self.scroll_offset = 0

    def add_move(self, move_str, color):
        self.moves.append((move_str, color))
        self.scroll_offset = max(0, (len(self.moves) * (self.font.get_height() + 10)) - self.log_height)

    def draw(self):
        log_rect = pygame.Rect(800, 0, self.log_width, self.log_height)
        pygame.draw.rect(self.screen, self.log_bg_color, log_rect)

        padding = 10
        y_offset = padding - self.scroll_offset
        for move, color in self.moves:
            move_text = self.font.render(move, True, self.white_text_color if color == pieces.Piece.WHITE else self.black_text_color)
            self.screen.blit(move_text, (810, y_offset))
            y_offset += move_text.get_height() + padding
