import numpy as np
from colorama import init, Fore, Back, Style
init(convert=True)
'''
print(Fore.RED + 'some red text') 
print(Back.GREEN + 'and with a green background') 
print(Style.DIM + 'and in dim text') 
print(Style.RESET_ALL) 
print('back to normal now') 
'''
def transfer_to_index(twodarray,board_size):
    index = []
    for i in range(len(twodarray)):
        tmp = twodarray[i][0]*board_size+twodarray[i][1]
        index.append(tmp)
    return index

def print_init_board(board, board_size):
    for i in range(board_size):
        for j in range(board_size):
            print(str(board[i][j])+'  ',end="")
            if (i*board_size+j+1)%board_size == 0:
                print('\n',end="")

def check_chess(hands, chess):   # 檢查要出的牌是否在自已手上
    if chess in hands:
        return "yes"
    else: 
        return "no"

def print_board(board, board_size, user_on_board, ai_on_board):     # 劃出目前局勢
    index_user_on_board, index_ai_on_board = [], []
    for i in range(len(user_on_board)):
        tmp = user_on_board[i][0]*board_size+user_on_board[i][1]
        index_user_on_board.append(tmp)
    for i in range(len(ai_on_board)):
        tmp = ai_on_board[i][0]*board_size+ai_on_board[i][1]
        index_ai_on_board.append(tmp)
    for i in range(board_size):
        for j in range(board_size):
            index = i*board_size+j
            if index in index_user_on_board:
                if board[i][j] == -1:
                    print(Fore.RED+'x  ',end="")
                    print(Style.RESET_ALL,end="")
                else:
                    print(Fore.RED+str(board[i][j])+'  ',end="")
                    print(Style.RESET_ALL,end="")
            elif index in index_ai_on_board:
                if board[i][j] == -1:
                    print(Fore.GREEN+'x  ',end="")
                    print(Style.RESET_ALL,end="")                    
                else:
                    print(Fore.GREEN+str(board[i][j])+'  ',end="")
                    print(Style.RESET_ALL,end="")
            else:
                print(str(board[i][j])+'  ',end="")
            if (index+1)%board_size == 0:
                print('\n',end="") 

def print_rest_chess(user, ai):    # 剩餘手牌
    print(Back.RED + 'User chess pieces: ',end="")
    print(Style.RESET_ALL,end="")
    print(user)
    print(Back.GREEN+'AI chess pieces: ',end="")
    print(Style.RESET_ALL,end="")
    print(ai)


def user_chess(board, user, ai, board_size, user_on_board, ai_on_board):  # 使用者下棋
    row, col, weight = input("User Input (row, col, weight): ").split()
    row = int(row)
    col = int(col)
    weight = int(weight)
    user_on_board.append([row,col])
    in_hands = check_chess(user, weight)
    if board[row][col] == 0 and in_hands == "yes":
        board[row][col] = weight
        user.remove(weight)
        board = change_board_cond(board, row, col, weight, board_size)
        print_board(board, board_size, user_on_board, ai_on_board)
        print_rest_chess(user,ai)
        return board, user, ai, user_on_board    
    else:
        print("You cannot put chess on that position!")
        print("Maybe the card is not in your hand!")

def ai_chess(board, ai, user, board_size, ai_on_board, user_on_board):  # AI 下棋
    row, col, weight = position(board, ai, board_size, user_on_board, ai_on_board)
    ai_on_board.append([row,col])
    in_hands = check_chess(ai, weight)
    if board[row][col] == 0 and in_hands == "yes":
        board[row][col] = weight
        ai.remove(weight)
        board = change_board_cond(board, row, col, weight, board_size)
        print_board(board, board_size, user_on_board, ai_on_board)
        print_rest_chess(user,ai)
        return board, ai, user, ai_on_board    
    else:
        print("You cannot put chess on that position!")
        print("Maybe the card is not in your hand!")
    

def find_surrounding(board, row, col, board_size):
    surrounding = [[row-1, col-1],[row-1, col],[row-1, col+1],[row, col-1],[row, col+1],[row+1, col-1],[row+1, col],[row+1, col+1]]
    in_bound = []
    for i in range(8):
        if 0<=surrounding[i][0]<board_size and 0<=surrounding[i][1]<board_size:
            in_bound.append(surrounding[i])
    return in_bound


def check_center(board, row, col, weight, board_size):  # 以某牌為中心和周圍牌的總和
    in_bound = find_surrounding(board, row, col, board_size)
    total = 0
    for i in range(len(in_bound)):
        tmp_row, tmp_col = in_bound[i][0], in_bound[i][1]
        if board[tmp_row][tmp_col] > 0:
            total += board[tmp_row][tmp_col]
    total += weight
    return total

def change_board_cond(board, row, col, weight, board_size):
    in_bound = find_surrounding(board, row, col, board_size)
    in_bound.append([row,col]) 
    mark = []
    for i in range(len(in_bound)):
        tmp_row, tmp_col = in_bound[i][0], in_bound[i][1]
        if board[tmp_row][tmp_col] > 0:
            limit = check_center(board, in_bound[i][0], in_bound[i][1], board[tmp_row][tmp_col], board_size)
            if limit > 15:
                mark.append([tmp_row,tmp_col])
    for i in range(len(mark)):
        board[mark[i][0]][mark[i][1]] = -1
    return board

def position(board, ai, board_size, user_on_board, ai_on_board):
    row, col = check_corner(board, board_size)
    if row == -2 and col == -2:  #corner都被下完了
        pos_score = []  #[[hand, row, col, user_score, ai_score],[]]
        for hand in range(len(ai)):
            for i in range(board_size):
                for j in range(board_size):
                    tmp_board = board.copy()
                    if board[i][j] != -1 and board[i][j] == 0:
                        ai_on_board.append([i,j])
                        tmp_board[i][j] = ai[hand]
                        tmp_board = change_board_cond(tmp_board, i, j, ai[hand], board_size)
                        #print(tmp_board)
                        user_score, ai_score = score_on_board(tmp_board, board_size, user_on_board, ai_on_board)
                        #print("user_score: ",user_score)
                        #print("ai_score: ", ai_score)
                        pos_score.append([ai[hand], i, j, user_score, ai_score])
                        ai_on_board.remove([i,j])
                        tmp_board[i][j] = 0
        row, col, weight = find_best_choice(pos_score)
        return row, col, weight
    else:  # 要先出小於13但最大的
        max_chess_index = ai.index(max(ai))
        weight = ai[max_chess_index-1]
        return row, col, weight
     
def score_on_board(board,board_size, user_on_board,ai_on_board):
    user_score = 0
    ai_score = 0
    index_user_on_board = transfer_to_index(user_on_board, board_size)
    index_ai_on_board = transfer_to_index(ai_on_board, board_size)
    for i in range(board_size):
        for j in range(board_size):
            index = i*board_size+j
            if index in index_user_on_board:
                if board[i][j] != -1:
                    user_score+=board[i][j]
            if index in index_ai_on_board:
                if board[i][j] != -1:
                    ai_score+=board[i][j]
    return user_score, ai_score

def check_corner(board, board_size):
    if board_size == 4:
        if board[3][3] == 0:
            return 3, 3
        elif board[3][0] == 0:
            return 3, 0
        elif board[0][3] == 0:
            return 0, 3
        elif board[0][0] == 0:
            return 0, 0
        else:
            return -2, -2
    else:
        if board[5][5] == 0:
            return 5, 5
        elif board[5][0] == 0:
            return 5, 0
        elif board[0][5] == 0:
            return 0, 5
        elif board[0][0] == 0:
            return 0, 0
        else:
            return -2, -2

def find_best_choice(pos_score):
    choice = []
    for i in range(len(pos_score)):
        ai_win_score = pos_score[i][4] - pos_score[i][3] # AI贏user幾分
        choice.append(ai_win_score)
    index = choice.index(max(choice))
    row = pos_score[index][1]
    col = pos_score[index][2]
    weight = pos_score[index][0]
    return row, col, weight

def cal_final_score(board, board_size, user_on_board, ai_on_board):
    index_user_on_board = transfer_to_index(user_on_board, board_size)
    index_ai_on_board = transfer_to_index(ai_on_board, board_size)
    user_final_score, ai_final_score = [], []
    user_max_chess, ai_max_chess = 0, 0
    for i in range(board_size):
        for j in range(board_size):
            if i*board_size+j in index_user_on_board and board[i][j] != -1:
                user_final_score.append(board[i][j])
            if i*board_size+j in index_ai_on_board and board[i][j] != -1:
                ai_final_score.append(board[i][j])
    if len(user_final_score) != 0:
        user_max_chess = max(user_final_score)
    else:
        user_max_chess = 0
    if len(ai_final_score) != 0:
        ai_max_chess = max(ai_final_score)
    else:
        ai_max_chess = 0
    return sum(user_final_score), user_max_chess, sum(ai_final_score), ai_max_chess

def whoiswinner(user_final_score, user_max_chess, ai_final_score, ai_max_chess):
    print("User final score: ", user_final_score)
    print("AI final score: ", ai_final_score)
    if user_final_score == ai_final_score:
        if user_max_chess > ai_max_chess:
            print("User Win!")
        elif ai_max_chess > user_max_chess:
            print("AI Win!")
        else:
            print("Draw!")
    elif user_final_score > ai_final_score:
        print("User Win!")
    else:
        print("AI Win!")

if __name__ == "__main__":
    first = int(input("User First? (0/1):"))
    board_size = int(input("Board Size? (4 or 6):"))
    #print(first, board_size)
    if board_size == 4:
        user = [2,3,5,8,13]
        ai = [2,3,5,8,13]
        user_on_board = []
        ai_on_board = []
        board = np.zeros((4,4), dtype=int)
        print_init_board(board, board_size)
        print(Back.RED+'User chess pieces: ',end="")
        print(Style.RESET_ALL,end="")
        print(user)
        print(Back.GREEN+'AI chess pieces: ',end="")
        print(Style.RESET_ALL,end="")
        print(ai)
        # 4x4 Game Start
        while True:
            if len(user) == 0 or len(ai) == 0:
                break
            else:
                if first == 1:     # user first
                    for i in range(5):  # 4x4下5次end game
                        board, user, ai, user_on_board = user_chess(board, user, ai, board_size, user_on_board, ai_on_board)
                        board, ai, user, ai_on_board = ai_chess(board, ai, user, board_size, ai_on_board, user_on_board)
                    break
                else:              # ai first
                    print("AI first")
                    for i in range(5):  # 4x4下5次end game
                        board, ai, user, ai_on_board = ai_chess(board, ai, user, board_size, ai_on_board, user_on_board)
                        board, user, ai, user_on_board = user_chess(board, user, ai, board_size, user_on_board, ai_on_board)
                    break
        print("End Game")
        print_board(board, board_size, user_on_board, ai_on_board)
        user_final_score, user_max_chess, ai_final_score, ai_max_chess = cal_final_score(board, board_size, user_on_board, ai_on_board)
        whoiswinner(user_final_score, user_max_chess, ai_final_score, ai_max_chess) 
    elif board_size == 6:
        user = [2,2,3,3,5,5,8,8,8,13,13]
        ai = [2,2,3,3,5,5,8,8,8,13,13]
        user_on_board = []
        ai_on_board = []
        board = np.zeros((6,6), dtype=int)
        print_init_board(board, board_size)
        print(Back.RED+'User chess pieces: ',end="")
        print(Style.RESET_ALL,end="")
        print(user)
        print(Back.GREEN+'AI chess pieces: ',end="")
        print(Style.RESET_ALL,end="")
        print(ai)
        # 6x6 Game Start
        while True:
            if len(user) == 0 or len(ai) == 0:
                break
            else:
                if first == 1:     # user first
                    for i in range(11):  # 4x4下5次end game
                        board, user, ai, user_on_board = user_chess(board, user, ai, board_size, user_on_board, ai_on_board)
                        board, ai, user, ai_on_board = ai_chess(board, ai, user, board_size, ai_on_board, user_on_board)
                    break
                else:              # ai first
                    print("AI first")
                    for i in range(11):  # 4x4下5次end game
                        board, ai, user, ai_on_board = ai_chess(board, ai, user, board_size, ai_on_board, user_on_board)
                        board, user, ai, user_on_board = user_chess(board, user, ai, board_size, user_on_board, ai_on_board)
                    break
        print("End Game")
        print_board(board, board_size, user_on_board, ai_on_board)
        user_final_score, user_max_chess, ai_final_score, ai_max_chess = cal_final_score(board, board_size, user_on_board, ai_on_board)
        whoiswinner(user_final_score, user_max_chess, ai_final_score, ai_max_chess)
    else:
        print("Your enter wrong board size!")