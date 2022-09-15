import pygame
import sys
from con4 import *
from time import sleep
from copy import deepcopy

def main():
    pygame.init()
    pygame.display.set_caption("Connect 4")
    screen = pygame.display.set_mode((930,650))
    font = pygame.font.Font('freesansbold.ttf', 32)

    board = deepcopy(start_board)
    player_token = 'R'
    comp_token = 'Y'
    game_over = False
    game_started = False
    player_score = 0
    comp_score = 0
    
    winner = None

    #Main Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if not game_started:
                start_screen(screen, font, player_token)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Click Start
                    if event.pos[0] >= 390 and event.pos[0] <= 540 and \
                       event.pos[1] >= 500 and event.pos[1] <= 575:
                       game_started = True
                       draw_board(screen)
                       print_score(screen, player_score, comp_score, font, player_token)
                       continue

                    #Player Click Red as Yellow
                    if event.pos[0] >= 325 and event.pos[0] <= 445 and \
                       event.pos[1] >= 210 and event.pos[1] <= 325 and \
                       player_token == 'Y':

                       player_token = 'R'
                       comp_token = 'Y'
                       start_screen(screen, font, player_token)

                    if event.pos[0] >= 475 and event.pos[0] <= 590 and \
                       event.pos[1] >= 210 and event.pos[1] <= 325 and \
                       player_token == 'R':

                       player_token = 'Y'
                       comp_token = 'R'
                       start_screen(screen, font, player_token)


            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and game_started:

                col = xy_to_row(event.pos[0], event.pos[1])
                if col > 0 and col < 8 and not is_col_full(board, col-1):
                    place_token(board, col-1, player_token)
                    #place_token(board, comp_move_points(board, player='Y', comp='R'), 'R')
                    if any_winners(board, player_token):
                        game_over = True
                        player_score += 1
                        print_score(screen, player_score, comp_score, font, player_token)
                        winner = player_token
                    else: 
                        place_token(board, comp_move_points(board), comp_token)
                        if any_winners(board, comp_token):
                            game_over = True
                            comp_score += 1
                            print_score(screen, player_score, comp_score, font, player_token)
                            winner = comp_token
                    draw_tokens(screen, board)

                if game_over:
                    print_winner(screen, font, winner, player_token, comp_token)

                if is_board_full(board) and not game_over:
                    game_over = True
                    print_winner(screen, font, 'T')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    screen.fill(colors['Wood'])
                    draw_board(screen)
                    print_score(screen, player_score, comp_score, font, player_token)
                    board = deepcopy(start_board)
                    game_over = False

        pygame.display.update()


def draw_board(screen):
    screen.fill(colors["Wood"])
    offset = 50

    #vertical
    for i in range(8):
        pygame.draw.line(screen, colors['Blue'], (consts.DBT*i + offset, offset), (consts.DBT*i + offset, 590), 10)

    #horizontal
    for x in range(7):
        pygame.draw.line(screen, colors['Blue'], (offset, consts.DBT*x + offset), (680, consts.DBT*x + offset), 10)


def draw_tokens(screen, board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != ' ':
                pygame.draw.circle(screen, colors[board[row][col]], (6.5+(col+1)*consts.DBT, 6.5+(row+1)*consts.DBT), 39.0, 45)

def start_screen(screen, font, pt):
    #Logo
    screen.fill(colors["Blue"])
    title_font = pygame.font.Font('freesansbold.ttf', 90)
    title = title_font.render("Connect 4", True, colors["Y"], None)
    screen.blit(title, consts.LWS)
    pygame.draw.circle(screen, colors["R"], coor_add(consts.LWS, consts.LDWT), 45, 50)

    #Start Button
    start_button = font.render("Start", True, colors["Black"], None)
    pygame.draw.rect(screen, colors["Light Gray"], pygame.Rect(390, 500, 150, 75))
    screen.blit(start_button, (425, 520))

    #Color Picker
    if pt == 'R':
        pygame.draw.rect(screen, colors["Dark Gray"], pygame.Rect(325, 210, 115, 115))
        pygame.draw.rect(screen, colors["Light Gray"], pygame.Rect(475, 210, 115, 115))
    else: #pt == 'Y'
        pygame.draw.rect(screen, colors["Light Gray"], pygame.Rect(325, 210, 115, 115))
        pygame.draw.rect(screen, colors["Dark Gray"], pygame.Rect(475, 210, 115, 115))

    #Tokens over selction
    pygame.draw.circle(screen, colors['R'], (382.5, 267.5), 45, 45)
    pygame.draw.circle(screen, colors['Y'], (532.5, 267.5), 45, 45)


def print_score(screen, ps, cs, font, pt):
    score_text = font.render("Score", True, colors["Blue"], colors["Wood"])
    screen.blit(score_text, (750, 70))
    pygame.draw.line(screen, colors["Blue"], (740, 101), (850, 101), 7)
    pygame.draw.line(screen, colors['Blue'], (795, 101), (795, 200), 7)

    p_text = font.render("R", True, colors["R"], colors["Wood"])
    c_text = font.render("Y", True, colors["Y"], colors["Wood"])

    if pt == 'R':
        ps_text = font.render(str(ps), True, colors["R"], colors["Wood"])
        cs_text = font.render(str(cs), True, colors["Y"], colors["Wood"])
    else:
        ps_text = font.render(str(cs), True, colors["R"], colors["Wood"])
        cs_text = font.render(str(ps), True, colors["Y"], colors["Wood"])

    screen.blit(p_text, (760, 110))
    screen.blit(ps_text, (760, 160))
    screen.blit(c_text, (810, 110))
    screen.blit(cs_text, (810, 160))

def print_winner(screen, font, winner, player_token, comp_token):
    if winner == player_token and winner == 'Y':
        w_text = font.render("You Win!", True, colors["White"], colors["Dark Yellow"])
        r_text = font.render("Restart? (r)", True, colors["White"], colors["Dark Yellow"])
    elif winner == comp_token and winner == 'Y':
        w_text = font.render("You Lost!", True, colors["White"], colors["Dark Yellow"])
        r_text = font.render("Restart? (r)", True, colors["White"], colors["Dark Yellow"])
    elif winner == player_token:
        w_text = font.render("You Win!", True, colors["White"], colors['R'])
        r_text = font.render("Restart? (r)", True, colors["White"], colors['R'])
    elif winner == comp_token:
        w_text = font.render("You Lost!", True, colors["White"], colors["R"])
        r_text = font.render("Restart? (r)", True, colors["White"], colors["R"])
    else: #winner == 'T' (for tie)
        w_text = font.render("Tied Game!", True, colors["White"], colors["Black"])
        r_text = font.render("Restart? (r)", True, colors["White"], colors["Black"])

    screen.blit(w_text, (300, 200))
    screen.blit(r_text, (282, 250))
    

if __name__ == "__main__":
    main()