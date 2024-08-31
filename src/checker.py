from .board import Board

class Checker:

    @staticmethod
    def is_in_check(board, color):
        """Returns True if the player with the given color is in check."""
        from .pieces import Piece
        king_position = Checker.find_king_position(board, color)
        if not king_position:
            raise ValueError(f"King of color {color} not found on the board!")

        opponent_color = Piece.BLACK if color == Piece.WHITE else Piece.BLACK
        for move in board.get_possible_moves(opponent_color):
            if move.xto == king_position[0] and move.yto == king_position[1]:
                return True
        return False

    @staticmethod
    def is_in_checkmate(board, color):
        """Returns True if the player with the given color is in checkmate."""
        from .pieces import Piece
        if not Checker.is_in_check(board, color):
            return False
        for move in board.get_possible_moves(color):
            board_clone = Board.clone(board)
            board_clone.perform_move(move)
            if not Checker.is_in_check(board_clone, color):
                return False
        return True

    @staticmethod
    def find_king_position(board, color):
        """Finds and returns the position of the king of the given color."""
        from .pieces import Piece  
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = board.get_piece(x, y)
                if piece and piece.color == color and piece.piece_type == Piece.KING:
                    return (x, y)
        return None
