PLAYER_1 = 'X'
PLAYER_2 = 'O'
TURN = 0
GAME_OVER = False
placement_list = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

def print_board(placement_list = []):
    print('\n' * 3)
    print(f' {placement_list[0]} | {placement_list[1]} | {placement_list[2]}')
    print('-----------')
    print(f' {placement_list[3]} | {placement_list[4]} | {placement_list[5]}')
    print('-----------')
    print(f' {placement_list[6]} | {placement_list[7]} | {placement_list[8]}')


print('Welcome to Tic Tac Toe!')
while not GAME_OVER:
    if TURN % 2 == 0:
        Move = int(input(f"Player {PLAYER_2}. Please choose a position on the board from 1 - 9. Starting from top left: "))
        if 0 < Move < 10:
            TURN += 1
            if TURN % 2 == 0:
                placement_list[Move - 1] = 'X'
                print_board(placement_list)
                print('\n')
            else:
                placement_list[Move - 1] = 'O'
                print_board(placement_list)
                print('\n')
        else:
            print("Please choose a value between 1 and 9.")

    else:
        Move = int(input(f"Player {PLAYER_1}. Please choose a position on the board from 1 - 9. Starting from top left: "))
        if 0 < Move < 10:
            TURN += 1
            if TURN % 2 == 0:
                placement_list[Move - 1] = 'X'
                print_board(placement_list)
                print('\n')
            else:
                placement_list[Move - 1] = 'O'
                print_board(placement_list)
                print('\n')
        else:
            print("Please choose a value between 1 and 9.")

    # Game Over conditions for X
    if placement_list[0] == PLAYER_1 and placement_list[1] == PLAYER_1 and placement_list[2] == PLAYER_1:
        GAME_OVER = True
        print(f'\n{PLAYER_1} wins!')
    elif placement_list[3] == PLAYER_1 and placement_list[4] == PLAYER_1 and placement_list[5] == PLAYER_1:
        GAME_OVER = True
        print(f'\n{PLAYER_1} wins!')
    elif placement_list[6] == PLAYER_1 and placement_list[7] == PLAYER_1 and placement_list[8] == PLAYER_1:
        GAME_OVER = True
        print(f'\n{PLAYER_1} wins!')
    elif placement_list[0] == PLAYER_1 and placement_list[3] == PLAYER_1 and placement_list[6] == PLAYER_1:
        GAME_OVER = True
        print(f'\n{PLAYER_1} wins!')
    elif placement_list[1] == PLAYER_1 and placement_list[4] == PLAYER_1 and placement_list[7] == PLAYER_1:
        GAME_OVER = True
        print(f'\n{PLAYER_1} wins!')
    elif placement_list[2] == PLAYER_1 and placement_list[5] == PLAYER_1 and placement_list[8] == PLAYER_1:
        GAME_OVER = True
        print(f'\n{PLAYER_1} wins!')
    elif placement_list[0] == PLAYER_1 and placement_list[4] == PLAYER_1 and placement_list[8] == PLAYER_1:
        GAME_OVER = True
        print(f'\n{PLAYER_1} wins!')
    elif placement_list[2] == PLAYER_1 and placement_list[4] == PLAYER_1 and placement_list[6] == PLAYER_1:
        GAME_OVER = True
        print(f'\n{PLAYER_1} wins!')

    # Game Over conditions for O
    if placement_list[0] == PLAYER_2 and placement_list[1] == PLAYER_2 and placement_list[2] == PLAYER_2:
        GAME_OVER = True
        print(f'\n{PLAYER_2} wins!')
    elif placement_list[3] == PLAYER_2 and placement_list[4] == PLAYER_2 and placement_list[5] == PLAYER_2:
        GAME_OVER = True
        print(f'\n{PLAYER_2} wins!')
    elif placement_list[6] == PLAYER_2 and placement_list[7] == PLAYER_2 and placement_list[8] == PLAYER_2:
        GAME_OVER = True
        print(f'\n{PLAYER_2} wins!')
    elif placement_list[0] == PLAYER_2 and placement_list[3] == PLAYER_2 and placement_list[6] == PLAYER_2:
        GAME_OVER = True
        print(f'\n{PLAYER_2} wins!')
    elif placement_list[1] == PLAYER_2 and placement_list[4] == PLAYER_2 and placement_list[7] == PLAYER_2:
        GAME_OVER = True
        print(f'\n{PLAYER_2} wins!')
    elif placement_list[2] == PLAYER_2 and placement_list[5] == PLAYER_2 and placement_list[8] == PLAYER_2:
        GAME_OVER = True
        print(f'\n{PLAYER_2} wins!')
    elif placement_list[0] == PLAYER_2 and placement_list[4] == PLAYER_2 and placement_list[8] == PLAYER_2:
        GAME_OVER = True
        print(f'\n{PLAYER_2} wins!')
    elif placement_list[2] == PLAYER_2 and placement_list[4] == PLAYER_2 and placement_list[6] == PLAYER_2:
        GAME_OVER = True
        print(f'\n{PLAYER_2} wins!')

