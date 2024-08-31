from . import board
from . import pieces
import numpy
from .checker import Checker

class Heuristics:
    PAWN_TABLE = numpy.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    KNIGHT_TABLE = numpy.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  15,  20,  20,  15,   5, -30],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    BISHOP_TABLE = numpy.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

    ROOK_TABLE = numpy.array([
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    QUEEN_TABLE = numpy.array([
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,   0,   5,  0,  0,   0,   0, -10],
        [-10,   5,   5,  5,  5,   5,   0, -10],
        [  0,   0,   5,  5,  5,   5,   0,  -5],
        [ -5,   0,   5,  5,  5,   5,   0,  -5],
        [-10,   0,   5,  5,  5,   5,   0, -10],
        [-10,   0,   0,  0,  0,   0,   0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ])

    KING_TABLE = numpy.array([
        [ 20,  30,  10,   0,   0,  10,  30,  20],
        [ 20,  20,   0,   0,   0,   0,  20,  20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30]
    ])

    @staticmethod
    def evaluate(board):
        material = Heuristics.get_material_score(board)

        pawns = Heuristics.get_piece_position_score(board, pieces.Pawn.PIECE_TYPE, Heuristics.PAWN_TABLE)
        knights = Heuristics.get_piece_position_score(board, pieces.Knight.PIECE_TYPE, Heuristics.KNIGHT_TABLE)
        bishops = Heuristics.get_piece_position_score(board, pieces.Bishop.PIECE_TYPE, Heuristics.BISHOP_TABLE)
        rooks = Heuristics.get_piece_position_score(board, pieces.Rook.PIECE_TYPE, Heuristics.ROOK_TABLE)
        queens = Heuristics.get_piece_position_score(board, pieces.Queen.PIECE_TYPE, Heuristics.QUEEN_TABLE)
        king = Heuristics.get_piece_position_score(board, pieces.King.PIECE_TYPE, Heuristics.KING_TABLE)

        center_control = Heuristics.evaluate_center_control(board)
        pawn_structure = Heuristics.evaluate_pawn_structure(board)
        mobility = Heuristics.get_mobility_score(board, pieces.Piece.WHITE) - Heuristics.get_mobility_score(board, pieces.Piece.BLACK)
        piece_coordination = Heuristics.evaluate_piece_coordination(board)
        king_safety = Heuristics.evaluate_king_safety(board)

        return material + pawns + knights + bishops + rooks + queens + king + center_control + pawn_structure + mobility + piece_coordination + king_safety

    @staticmethod
    def get_piece_position_score(board, piece_type, table):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
                if piece != 0:
                    if piece.piece_type == piece_type:
                        if piece.color == pieces.Piece.WHITE:
                            white += table[y][x]
                        else:
                            black += table[7 - y][x]
        return white - black

    @staticmethod
    def get_material_score(board):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
                if piece != 0:
                    if piece.color == pieces.Piece.WHITE:
                        white += piece.value
                    else:
                        black += piece.value
        return white - black

    @staticmethod
    def get_mobility_score(board, color):
        mobility = 0
        for move in board.get_possible_moves(color):
            mobility += 1
        return mobility

    @staticmethod
    def evaluate_center_control(board):
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        control_score = 0

        for (x, y) in center_squares:
            piece = board.chesspieces[x][y]
            if piece != 0:
                if piece.color == pieces.Piece.WHITE:
                    control_score += 10
                else:
                    control_score -= 10

        return control_score

    @staticmethod
    def evaluate_pawn_structure(board):
        white_penalty = 0
        black_penalty = 0

        for y in range(8):
            white_pawns = 0
            black_pawns = 0
            for x in range(8):
                piece = board.chesspieces[x][y]
                if piece != 0 and piece.piece_type == pieces.Pawn.PIECE_TYPE:
                    if piece.color == pieces.Piece.WHITE:
                        white_pawns += 1
                    else:
                        black_pawns += 1

            if white_pawns > 1:
                white_penalty += (white_pawns - 1) * 5
            if black_pawns > 1:
                black_penalty += (black_pawns - 1) * 5

        return black_penalty - white_penalty

    @staticmethod
    def evaluate_piece_coordination(board):
        coordination_score = 0
        white_rooks = [piece for row in board.chesspieces for piece in row if isinstance(piece, pieces.Rook) and piece.color == pieces.Piece.WHITE]
        black_rooks = [piece for row in board.chesspieces for piece in row if isinstance(piece, pieces.Rook) and piece.color == pieces.Piece.BLACK]

        if len(white_rooks) > 1:
            if abs(white_rooks[0].x - white_rooks[1].x) <= 1:
                coordination_score += 10
        if len(black_rooks) > 1:
            if abs(black_rooks[0].x - black_rooks[1].x) <= 1:
                coordination_score -= 10

        return coordination_score

    @staticmethod
    def evaluate_king_safety(board):
        white_king = board.get_king(pieces.Piece.WHITE)
        black_king = board.get_king(pieces.Piece.BLACK)
        safety_score = 0

        safety_score -= Heuristics.king_mobility_score(board, black_king)
        safety_score += Heuristics.king_mobility_score(board, white_king)

        return safety_score

    @staticmethod
    def king_mobility_score(board, king):
        if not king:
            return 0
        moves = king.get_possible_moves(board)
        return len(moves)

class AI:
    INFINITE = 10000000

    def __init__(self):
        self.previous_moves = []

    def get_ai_move(self, chessboard, invalid_moves):
        
        if Checker.is_in_checkmate(chessboard, pieces.Piece.BLACK):
            return "checkmate"

        best_move = None
        best_score = AI.INFINITE
        alternative_move = None
        alternative_score = AI.INFINITE

        
        if Checker.is_in_check(chessboard, pieces.Piece.BLACK):
            for move in chessboard.get_possible_moves(pieces.Piece.BLACK):
                if self.is_invalid_move(move, invalid_moves):
                    continue

                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                
                if not Checker.is_in_check(copy, pieces.Piece.BLACK):
                    score = AI.alphabeta(copy, 2, -AI.INFINITE, AI.INFINITE, True)
                    if score < best_score:
                        best_score = score
                        best_move = move

            return best_move if best_move else None

        for move in chessboard.get_possible_moves(pieces.Piece.BLACK):
            if self.is_invalid_move(move, invalid_moves):
                continue

            copy = board.Board.clone(chessboard)
            copy.perform_move(move)

            
            if Checker.is_in_check(copy, pieces.Piece.BLACK):
                continue

            score = AI.alphabeta(copy, 2, -AI.INFINITE, AI.INFINITE, True)

            if score < best_score:
                alternative_move = best_move
                alternative_score = best_score
                best_score = score
                best_move = move
            elif score < alternative_score:
                alternative_score = score
                alternative_move = move

        if best_move is None:
            return None

        if len(self.previous_moves) >= 8 and self.is_repetition(best_move):
            best_move = alternative_move or self.find_non_repetitive_move(chessboard, invalid_moves)

        self.previous_moves.append(best_move)
        if len(self.previous_moves) > 8:
            self.previous_moves.pop(0)

        return best_move

    def is_repetition(self, move):
        if len(self.previous_moves) < 8:
            return False
        count = sum(1 for m in self.previous_moves[-8:] if m.equals(move))
        return count >= 4

    def find_non_repetitive_move(self, chessboard, invalid_moves):
        for move in chessboard.get_possible_moves(pieces.Piece.BLACK):
            if not self.is_invalid_move(move, invalid_moves) and not self.is_repetition(move):
                return move
        return None

    @staticmethod
    def is_invalid_move(move, invalid_moves):
        for invalid_move in invalid_moves:
            if invalid_move.equals(move):
                return True
        return False

    @staticmethod
    def minimax(board, depth, maximizing):
        if depth == 0:
            return Heuristics.evaluate(board)

        if maximizing:
            best_score = -AI.INFINITE
            for move in board.get_possible_moves(pieces.Piece.WHITE):
                copy = board.Board.clone(board)
                copy.perform_move(move)

                score = AI.minimax(copy, depth-1, False)
                best_score = max(best_score, score)

            return best_score
        else:
            best_score = AI.INFINITE
            for move in board.get_possible_moves(pieces.Piece.BLACK):
                copy = board.Board.clone(board)
                copy.perform_move(move)

                score = AI.minimax(copy, depth-1, True)
                best_score = min(best_score, score)

            return best_score

    @staticmethod
    def alphabeta(chessboard, depth, a, b, maximizing):
        if depth == 0:
            return Heuristics.evaluate(chessboard)

        if maximizing:
            best_score = -AI.INFINITE
            for move in chessboard.get_possible_moves(pieces.Piece.WHITE):
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                best_score = max(best_score, AI.alphabeta(copy, depth-1, a, b, False))
                a = max(a, best_score)
                if b <= a:
                    break
            return best_score
        else:
            best_score = AI.INFINITE
            for move in chessboard.get_possible_moves(pieces.Piece.BLACK):
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                best_score = min(best_score, AI.alphabeta(copy, depth-1, a, b, True))
                b = min(b, best_score)
                if b <= a:
                    break
            return best_score
