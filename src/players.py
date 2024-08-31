import time
import pygame
from . import pieces
from . import ai
from .move import Move
from .available_moves import AvailableMoves
from .checker import Checker

class HumanPlayer:
    def __init__(self, screen, chessboard, move_log):
        self.screen = screen
        self.chessboard = chessboard
        self.selected_piece = None
        self.draw = None
        self.move_log = move_log

    def make_move(self):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            x, y = pos[0] // 100, pos[1] // 100
            piece = self.chessboard.get_piece(x, y)

            if piece and piece.color == pieces.Piece.WHITE:
                self.selected_piece = piece
            elif self.selected_piece:
                move = Move(self.selected_piece.x, self.selected_piece.y, x, y)
                valid_moves = AvailableMoves(self.chessboard, self.selected_piece).get_moves()
                if any(move.equals(m) for m in valid_moves):
                    self.chessboard.perform_move(move)
                    self.move_log.add_move(move.to_string(), self.selected_piece.color)
                    self.selected_piece = None

                    
                    self.draw.update()
                    pygame.display.flip()

                    
                    if Checker.is_in_check(self.chessboard, pieces.Piece.BLACK):
                        if Checker.is_in_checkmate(self.chessboard, pieces.Piece.BLACK):
                            return "checkmate"

                    
                    if Checker.is_in_check(self.chessboard, pieces.Piece.WHITE):
                        if not Checker.is_in_checkmate(self.chessboard, pieces.Piece.WHITE):
                            
                            self.selected_piece = None
                            return "in_check"

                    return True

        
        valid_moves = AvailableMoves(self.chessboard, self.selected_piece).get_moves() if self.selected_piece else []
        self.draw.update(self.selected_piece, valid_moves)
        return False


class AIPlayer:
    def __init__(self, chessboard, move_log):
        self.chessboard = chessboard
        self.move_log = move_log
        self.ai = ai.AI()

    def get_move(self):
        invalid_moves = []
        move = self.ai.get_ai_move(self.chessboard, invalid_moves)
        if move:
            piece = self.chessboard.get_piece(move.xfrom, move.yfrom)
            self.move_log.add_move(move.to_string(), piece.color)  
        return move
