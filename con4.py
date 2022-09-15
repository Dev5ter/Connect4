from random import choice
from copy import deepcopy

start_board = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ']
]

class consts:
    #START SCREEN
    LWS = (170,100) #LOGO WORD START
    LDWT = (520, 40) #LOGO DISTANCE BETWEEN WORD AND TOKEN

    #Board
    DBT = 90 #DISTANT Between tokens


def coor_add(a: tuple([int, int]), b: tuple([int, int])) -> tuple([int, int]):
    return (a[0]+b[0], a[1]+b[1])

colors = {
    "R": (255, 0, 0),
    "Y": (255, 255, 0),
    "Dark Yellow": (238, 231, 32),
    "Blue": (0, 0, 255),
    "Wood": (243, 201, 118),
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Light Gray": (160, 160, 160),
    "Dark Gray": (100, 100, 100)
}

def xy_to_row(x: int, y: int) -> int:
    return (x+50) // 90

def place_token(board, col: int, player: str):
    if not is_col_full(board, col):
        board[first_slot_on_row(board, col)][col] = player

def first_slot_on_row(board, row: int) -> int:
    slot = 0

    while(slot < 6 and board[slot][row] == ' '):
        slot += 1

    return slot-1

def is_col_full(board, col: int) -> bool:
    return board[0][col] != ' '

def is_board_full(board):
    for i in range(7):
        if not is_col_full(board, i):
            return False
    return True

def any_winners(board, player) -> bool:
    #Horizontal Lines
    for i in range(6):
        for x in range(4):
            if board[i][x] == board[i][x+1] and \
               board[i][x+1] == board[i][x+2] and \
               board[i][x+2] == board[i][x+3] and \
               board[i][x+3] == player:
               return True

    #Vertical Lines
    for i in range(7):
        for x in range(3):
            if board[x][i] == board[x+1][i] and \
                board[x+1][i] == board[x+2][i] and \
                board[x+2][i] == board[x+3][i] and \
                board[x+3][i] == player:
                return True

    #TL-BR Diagnols
    for x in range(4):
        for i in range(3):
            if board[i][x] == board[i+1][x+1] and \
                board[i+1][x+1] == board[i+2][x+2] and \
                board[i+2][x+2] == board[i+3][x+3] and \
                board[i+3][x+3] == player:
                return True

    #BL-TR Diagnols
    for i in range(6, 2, -1):
        for x in range(3):
            if board[x][i] == board[x+1][i-1] and \
                board[x+1][i-1] == board[x+2][i-2] and \
                board[x+2][i-2] == board[x+3][i-3] and \
                board[x+3][i-3] == player:
                return True

    return False

def comp_move_points(board, player='R', comp='Y') -> int:
    points = [5, 5, 5, 5, 5, 5, 5]
    for i in range(len(points)):
        #Immidiate win is max points
        test_board = deepcopy(board)
        place_token(test_board, i, comp)
        if any_winners(test_board, comp):
            points[i] += 100

        #Block Win
        test_board = deepcopy(board)
        place_token(test_board, i, player)
        if any_winners(test_board, player):
            points[i] += 45

        #Stack give him win
        test_board = deepcopy(board)
        place_token(test_board, i, comp)
        place_token(test_board, i, player)
        if any_winners(test_board, player):
            points[i] -= 30

        #Dont give up comp win too easily
        test_board = deepcopy(board)
        place_token(test_board, i, comp)
        place_token(test_board, i, comp)
        if any_winners(test_board, comp):
            points[i] -= 20


        #Column Full
        if is_col_full(board, i):
            points[i] -= 100

    #Check for Empty 2
    check_block  = [' ', player, player, ' ', ' ']
    check_block2 = [' ', ' ', player, player, ' ']
    check_win  = [' ', comp, comp, ' ', ' ']
    check_win2 = [' ', ' ', comp, comp, ' ']
    for i in range(5, -1, -1):
        for x in range(3):
            if first_slot_on_row(board, x) == i and first_slot_on_row(board, x+3) == i and first_slot_on_row(board, x+4) == i:
                if board[i][x:x+5] == check_win:
                    points[x] += 35
                    points[x+3] += 35
                elif board[i][x:x+5] == check_block:
                    points[x] += 40
                    points[x+3] += 40
            elif first_slot_on_row(board, x) == i and first_slot_on_row(board, x+1) == i and first_slot_on_row(board, x+4) == i:
                if board[i][x:x+5] == check_win2:
                    points[x+1] += 35
                    points[x+4] += 35
                elif board[i][x:x+5] == check_block2:
                    points[x+1] += 40
                    points[x+4] += 40
                
            


    print(points)
    if points.count(max(points)) > 1:
        top = []
        for p in range(len(points)):
            if points[p] == max(points):
                top.append(p)
        return choice(top)
    else:
        return points.index(max(points))

