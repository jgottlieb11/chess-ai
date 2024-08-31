from . import ai
from .move import Move

class Piece:
    WHITE = "W"
    BLACK = "B"
    
    PAWN = "P"
    KNIGHT = "N"
    BISHOP = "B"
    ROOK = "R"
    QUEEN = "Q"
    KING = "K"

    def __init__(self, x, y, color, piece_type, value):
        self.x = x
        self.y = y
        self.color = color
        self.piece_type = piece_type
        self.value = value

    def get_possible_moves(self, board):
        
        moves = self.get_all_possible_moves(board)
        
        valid_moves = [move for move in moves if not board.is_check_after_move(move, self.color)]
        return valid_moves

    def get_all_possible_moves(self, board):
        """This method should return all possible moves for the piece without considering check"""
        if self.piece_type == Piece.PAWN:
            return self.get_possible_pawn_moves(board)
        elif self.piece_type == Piece.ROOK:
            return self.get_possible_horizontal_moves(board)
        elif self.piece_type == Piece.KNIGHT:
            return self.get_possible_knight_moves(board)
        elif self.piece_type == Piece.BISHOP:
            return self.get_possible_diagonal_moves(board)
        elif self.piece_type == Piece.QUEEN:
            return self.get_possible_diagonal_moves(board) + self.get_possible_horizontal_moves(board)
        elif self.piece_type == Piece.KING:
            return self.get_possible_king_moves(board)
        return []

    def get_possible_diagonal_moves(self, board):
        moves = []
        for i in range(1, 8):
            if not board.in_bounds(self.x + i, self.y + i):
                break
            piece = board.get_piece(self.x + i, self.y + i)
            moves.append(self.get_move(board, self.x + i, self.y + i))
            if piece != 0:
                break

        for i in range(1, 8):
            if not board.in_bounds(self.x + i, self.y - i):
                break
            piece = board.get_piece(self.x + i, self.y - i)
            moves.append(self.get_move(board, self.x + i, self.y - i))
            if piece != 0:
                break

        for i in range(1, 8):
            if not board.in_bounds(self.x - i, self.y - i):
                break
            piece = board.get_piece(self.x - i, self.y - i)
            moves.append(self.get_move(board, self.x - i, self.y - i))
            if piece != 0:
                break

        for i in range(1, 8):
            if not board.in_bounds(self.x - i, self.y + i):
                break
            piece = board.get_piece(self.x - i, self.y + i)
            moves.append(self.get_move(board, self.x - i, self.y + i))
            if piece != 0:
                break

        return self.remove_null_from_list(moves)

    def get_possible_horizontal_moves(self, board):
        moves = []

        
        for i in range(1, 8 - self.x):
            piece = board.get_piece(self.x + i, self.y)
            moves.append(self.get_move(board, self.x + i, self.y))
            if piece != 0:
                break

        
        for i in range(1, self.x + 1):
            piece = board.get_piece(self.x - i, self.y)
            moves.append(self.get_move(board, self.x - i, self.y))
            if piece != 0:
                break

        
        for i in range(1, 8 - self.y):
            piece = board.get_piece(self.x, self.y + i)
            moves.append(self.get_move(board, self.x, self.y + i))
            if piece != 0:
                break

        
        for i in range(1, self.y + 1):
            piece = board.get_piece(self.x, self.y - i)
            moves.append(self.get_move(board, self.x, self.y - i))
            if piece != 0:
                break

        return self.remove_null_from_list(moves)

    def get_possible_knight_moves(self, board):
        moves = []

        
        knight_moves = [
            (self.x + 2, self.y + 1), (self.x + 2, self.y - 1),
            (self.x - 2, self.y + 1), (self.x - 2, self.y - 1),
            (self.x + 1, self.y + 2), (self.x + 1, self.y - 2),
            (self.x - 1, self.y + 2), (self.x - 1, self.y - 2)
        ]

        for xto, yto in knight_moves:
            moves.append(self.get_move(board, xto, yto))

        return self.remove_null_from_list(moves)

    def get_possible_king_moves(self, board):
        moves = []

        
        king_moves = [
            (self.x + 1, self.y), (self.x + 1, self.y + 1),
            (self.x, self.y + 1), (self.x - 1, self.y + 1),
            (self.x - 1, self.y), (self.x - 1, self.y - 1),
            (self.x, self.y - 1), (self.x + 1, self.y - 1)
        ]

        for xto, yto in king_moves:
            moves.append(self.get_move(board, xto, yto))

        
        moves.append(self.get_castle_kingside_move(board))
        moves.append(self.get_castle_queenside_move(board))

        return self.remove_null_from_list(moves)

    def get_possible_pawn_moves(self, board):
        moves = []
        direction = -1 if self.color == Piece.WHITE else 1

       
        if board.get_piece(self.x, self.y + direction) == 0:
            moves.append(self.get_move(board, self.x, self.y + direction))
        
        
        if self.is_starting_position() and board.get_piece(self.x, self.y + direction) == 0 and board.get_piece(self.x, self.y + direction * 2) == 0:
            moves.append(self.get_move(board, self.x, self.y + direction * 2))

        
        for dx in [-1, 1]:
            piece = board.get_piece(self.x + dx, self.y + direction)
            if piece != 0 and piece.color != self.color:
                moves.append(self.get_move(board, self.x + dx, self.y + direction))

        
        if board.last_move and isinstance(board.chesspieces[board.last_move.xto][board.last_move.yto], Pawn):
            if abs(board.last_move.yfrom - board.last_move.yto) == 2:
                if board.last_move.xto in [self.x + 1, self.x - 1] and board.last_move.yto == self.y:
                    moves.append(self.get_move(board, board.last_move.xto, self.y + direction))

        return self.remove_null_from_list(moves)

    def get_move(self, board, xto, yto):
        move = 0
        if board.in_bounds(xto, yto):
            piece = board.get_piece(xto, yto)
            if piece == 0 or piece.color != self.color:
                move = Move(self.x, self.y, xto, yto)
        return move

    def remove_null_from_list(self, l):
        return [move for move in l if move != 0]

    def to_string(self):
        return self.color + self.piece_type + " "

    def is_starting_position(self):
        if self.piece_type == Piece.PAWN:
            return (self.color == Piece.BLACK and self.y == 1) or (self.color == Piece.WHITE and self.y == 6)

    
    def get_castle_kingside_move(self, board):
        piece_in_corner = board.get_piece(self.x + 3, self.y)
        if piece_in_corner == 0 or piece_in_corner.piece_type != Piece.ROOK or piece_in_corner.color != self.color:
            return 0

        if (self.color == Piece.WHITE and board.white_king_moved) or (self.color == Piece.BLACK and board.black_king_moved):
            return 0

        if board.get_piece(self.x + 1, self.y) != 0 or board.get_piece(self.x + 2, self.y) != 0:
            return 0
    
        return Move(self.x, self.y, self.x + 2, self.y)  

    def get_castle_queenside_move(self, board):
        piece_in_corner = board.get_piece(self.x - 4, self.y)
        if piece_in_corner == 0 or piece_in_corner.piece_type != Piece.ROOK or piece_in_corner.color != self.color:
            return 0

        if (self.color == Piece.WHITE and board.white_king_moved) or (self.color == Piece.BLACK and board.black_king_moved):
            return 0

        if board.get_piece(self.x - 1, self.y) != 0 or board.get_piece(self.x - 2, self.y) != 0 or board.get_piece(self.x - 3, self.y) != 0:
            return 0
        
        return Move(self.x, self.y, self.x - 2, self.y)

    def clone(self):
        return self.__class__(self.x, self.y, self.color)

class Rook(Piece):

    PIECE_TYPE = Piece.ROOK
    VALUE = 500

    def __init__(self, x, y, color):
        super(Rook, self).__init__(x, y, color, Rook.PIECE_TYPE, Rook.VALUE)

    def get_possible_moves(self, board):
        return self.get_possible_horizontal_moves(board)

    def clone(self):
        return Rook(self.x, self.y, self.color)

class Knight(Piece):

    PIECE_TYPE = Piece.KNIGHT
    VALUE = 320

    def __init__(self, x, y, color):
        super(Knight, self).__init__(x, y, color, Knight.PIECE_TYPE, Knight.VALUE)

    def get_possible_moves(self, board):
        return self.get_possible_knight_moves(board)

    def clone(self):
        return Knight(self.x, self.y, self.color)

class Bishop(Piece):

    PIECE_TYPE = Piece.BISHOP
    VALUE = 330

    def __init__(self, x, y, color):
        super(Bishop, self).__init__(x, y, color, Bishop.PIECE_TYPE, Bishop.VALUE)

    def get_possible_moves(self, board):
        return self.get_possible_diagonal_moves(board)

    def clone(self):
        return Bishop(self.x, self.y, self.color)

class Queen(Piece):

    PIECE_TYPE = Piece.QUEEN
    VALUE = 900

    def __init__(self, x, y, color):
        super(Queen, self).__init__(x, y, color, Queen.PIECE_TYPE, Queen.VALUE)

    def get_possible_moves(self, board):
        diagonal = self.get_possible_diagonal_moves(board)
        horizontal = self.get_possible_horizontal_moves(board)
        return horizontal + diagonal

    def clone(self):
        return Queen(self.x, self.y, self.color)

class King(Piece):

    PIECE_TYPE = Piece.KING
    VALUE = 20000

    def __init__(self, x, y, color):
        super(King, self).__init__(x, y, color, King.PIECE_TYPE, King.VALUE)

    def get_possible_moves(self, board):
        return self.get_possible_king_moves(board)

    def clone(self):
        return King(self.x, self.y, self.color)

class Pawn(Piece):

    PIECE_TYPE = Piece.PAWN
    VALUE = 100

    def __init__(self, x, y, color):
        super(Pawn, self).__init__(x, y, color, Pawn.PIECE_TYPE, Pawn.VALUE)

    def is_starting_position(self):
        return (self.color == Piece.BLACK and self.y == 1) or (self.color == Piece.WHITE and self.y == 6)

    def get_possible_moves(self, board):
        return self.get_possible_pawn_moves(board)

    def clone(self):
        return Pawn(self.x, self.y, self.color)
