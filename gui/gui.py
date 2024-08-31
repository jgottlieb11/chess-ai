import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from src.draw import Draw
from src.players import HumanPlayer, AIPlayer
from src.board import Board
from src.checker import Checker
from src.move_log import MoveLog
import src.pieces as pieces


def show_game_over(screen, winner, board_width, board_height):
    pygame.time.wait(3000)
    
    
    popup_width = 300
    popup_height = 100
    popup_x = (board_width - popup_width) // 2
    popup_y = (board_height - popup_height) // 2
    
   
    pygame.draw.rect(screen, (0, 0, 0), (popup_x, popup_y, popup_width, popup_height))
    
    
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Game Over! {winner} wins!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height // 2))
    screen.blit(text, text_rect)
    
    pygame.display.flip()

    pygame.time.wait(3000)
    pygame.quit()
    exit()

def main():
    pygame.init()
    screen_info = pygame.display.Info()
    screen_height = int(screen_info.current_h * 0.718)
    screen_width = int(screen_height * 9 / 8)
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chess AI")

    chessboard = Board.new()
    draw = Draw(screen, chessboard)
    move_log = MoveLog(screen)

    human = HumanPlayer(screen, chessboard, move_log)
    human.draw = draw

    ai_player = AIPlayer(chessboard, move_log)

    running = True
    player_turn = True

    board_width = int(screen_height * 8 / 9)
    board_height = screen_height

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw.update()

        if player_turn:
            move_result = human.make_move()
            if move_result == "checkmate":
                
                show_game_over(screen, "White", board_width, board_height)
                running = False
            elif move_result == "in_check":
                
                continue
            elif move_result:
                player_turn = False

        else:
            ai_move = ai_player.get_move()
            if ai_move == "checkmate":
                show_game_over(screen, "Checkmate! You win!", board_width, board_height)
                running = False
            elif ai_move == "draw":
                show_game_over(screen, "Draw by repetition", board_width, board_height)
                running = False
            elif ai_move:
                chessboard.perform_move(ai_move)
                if Checker.is_in_check(chessboard, pieces.Piece.WHITE):
                    if Checker.is_in_checkmate(chessboard, pieces.Piece.WHITE):
                        draw.update()
                        pygame.display.flip()
                        show_game_over(screen, "Black", board_width, board_height)
                        running = False
                player_turn = True

        move_log.draw()  
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
