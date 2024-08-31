from .move import Move
from .board import Board
from .checker import Checker

class AvailableMoves:
    def __init__(self, board, piece):
        self.board = board
        self.piece = piece

    def get_moves(self):
        if not self.piece:
            return []
        possible_moves = self.piece.get_all_possible_moves(self.board)
        valid_moves = []

        for move in possible_moves:
            board_clone = Board.clone(self.board)
            board_clone.perform_move(move)
            if not Checker.is_in_check(board_clone, self.piece.color):
                valid_moves.append(move)

        return valid_moves
