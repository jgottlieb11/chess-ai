from .move import Move
from . import pieces

class Board:
    WIDTH = 8
    HEIGHT = 8

    def __init__(self, chesspieces, white_king_moved, black_king_moved):
        self.chesspieces = chesspieces
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved
        self.last_move = None

    @classmethod
    def clone(cls, chessboard):
        chesspieces = [[0 for x in range(Board.WIDTH)] for y in range(Board.HEIGHT)]
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = chessboard.chesspieces[x][y]
                if piece != 0:
                    chesspieces[x][y] = piece.clone()
        board = cls(chesspieces, chessboard.white_king_moved, chessboard.black_king_moved)
        board.last_move = chessboard.last_move
        return board

    @classmethod
    def new(cls):
        chess_pieces = [[0 for x in range(Board.WIDTH)] for y in range(Board.HEIGHT)]
        
        for x in range(Board.WIDTH):
            chess_pieces[x][Board.HEIGHT-2] = pieces.Pawn(x, Board.HEIGHT-2, pieces.Piece.WHITE)
            chess_pieces[x][1] = pieces.Pawn(x, 1, pieces.Piece.BLACK)
        
        chess_pieces[0][Board.HEIGHT-1] = pieces.Rook(0, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-1][Board.HEIGHT-1] = pieces.Rook(Board.WIDTH-1, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[0][0] = pieces.Rook(0, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-1][0] = pieces.Rook(Board.WIDTH-1, 0, pieces.Piece.BLACK)
        
        chess_pieces[1][Board.HEIGHT-1] = pieces.Knight(1, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-2][Board.HEIGHT-1] = pieces.Knight(Board.WIDTH-2, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[1][0] = pieces.Knight(1, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-2][0] = pieces.Knight(Board.WIDTH-2, 0, pieces.Piece.BLACK)
        
        chess_pieces[2][Board.HEIGHT-1] = pieces.Bishop(2, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-3][Board.HEIGHT-1] = pieces.Bishop(Board.WIDTH-3, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[2][0] = pieces.Bishop(2, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-3][0] = pieces.Bishop(Board.WIDTH-3, 0, pieces.Piece.BLACK)
        
        chess_pieces[4][Board.HEIGHT-1] = pieces.King(4, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[3][Board.HEIGHT-1] = pieces.Queen(3, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[4][0] = pieces.King(4, 0, pieces.Piece.BLACK)
        chess_pieces[3][0] = pieces.Queen(3, 0, pieces.Piece.BLACK)
        return cls(chess_pieces, False, False)

    def get_possible_moves(self, color):
        moves = []
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = self.chesspieces[x][y]
                if piece != 0 and piece.color == color:
                    moves += piece.get_possible_moves(self)
        return moves

    def perform_move(self, move):
        piece = self.chesspieces[move.xfrom][move.yfrom]
        self.move_piece(piece, move.xto, move.yto)

        
        if piece.piece_type == pieces.Pawn.PIECE_TYPE:
            if abs(move.xto - move.xfrom) == 1 and abs(move.yto - move.yfrom) == 1:
                last_move_piece = self.chesspieces[self.last_move.xto][self.last_move.yto]
                if isinstance(last_move_piece, pieces.Pawn):
                    if move.xto == self.last_move.xto and move.yto == self.last_move.yto + (1 if piece.color == pieces.Piece.BLACK else -1):
                        self.chesspieces[self.last_move.xto][self.last_move.yto] = 0

        
        self.last_move = move

        
        if piece.piece_type == pieces.Pawn.PIECE_TYPE:
            if piece.y == 0 or piece.y == Board.HEIGHT - 1:
                self.chesspieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)

        if piece.piece_type == pieces.King.PIECE_TYPE:
            
            if piece.color == pieces.Piece.WHITE:
                self.white_king_moved = True
            else:
                self.black_king_moved = True

            
            if move.xto - move.xfrom == 2:
                rook = self.chesspieces[move.xfrom + 3][move.yfrom]
                self.move_piece(rook, move.xfrom + 1, move.yfrom)

            
            if move.xto - move.xfrom == -2:
                rook = self.chesspieces[move.xfrom - 4][move.yfrom]
                self.move_piece(rook, move.xfrom - 1, move.yfrom)

    def move_piece(self, piece, xto, yto):
        self.chesspieces[piece.x][piece.y] = 0
        piece.x = xto
        piece.y = yto
        self.chesspieces[xto][yto] = piece

    def get_king(self, color):
        for x in range(8):
            for y in range(8):
                piece = self.chesspieces[x][y]
                if piece != 0 and piece.piece_type == pieces.King.PIECE_TYPE and piece.color == color:
                    return piece
        return None  

    def is_check(self, color):
        other_color = pieces.Piece.WHITE if color == pieces.Piece.WHITE else pieces.Piece.BLACK
        for move in self.get_possible_moves(other_color):
            copy = Board.clone(self)
            copy.perform_move(move)
            if not copy.get_king(color):
                return True
        return False

    def is_check_after_move(self, move, color):
        copy = self.clone()
        copy.perform_move(move)
        return copy.is_check(color)

    def get_piece(self, x, y):
        if not self.in_bounds(x, y):
            return 0
        return self.chesspieces[x][y]

    def in_bounds(self, x, y):
        return 0 <= x < Board.WIDTH and 0 <= y < Board.HEIGHT

    def to_string(self):
        string =  "    A  B  C  D  E  F  G  H\n"
        string += "    -----------------------\n"
        for y in range(Board.HEIGHT):
            string += str(8 - y) + " | "
            for x in range(Board.WIDTH):
                piece = self.chesspieces[x][y]
                if piece != 0:
                    string += piece.to_string()
                else:
                    string += ".. "
            string += "\n"
        return string + "\n"
