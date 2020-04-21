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
def check_chess(hands, chess):   # 檢查要出的牌是否在自已手上
    if chess in hands:
        return "yes"
    else: 
        return "no"

def print_board(board, board_size, user_on_board, ai_on_board):     # 劃出目前局勢
    print(board)
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
    print(Back.BLUE+'AI chess pieces: ',end="")
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
    pos_score = []
    pos = []
    for hand in range(len(ai)):
        tmp_board = board.copy()
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] != -1 and board[i][j] == 0:
                    ai_on_board.append([i,j])
                    pos.append([i,j,ai[hand]])
                    #print(f'{board}, {i}, {j}, {ai[hand]}, {board_size}')
                    tmp_board[i][j] = ai[hand]
                    tmp_board = change_board_cond(tmp_board, i, j, ai[hand], board_size)
                    #print(tmp_board)
                    tmp_score = score_on_board(tmp_board, board_size, user_on_board,ai_on_board)
                    #print(tmp_score)
                    ai_on_board.remove([i,j])
                    tmp_board[i][j] = 0
                    pos_score.append(tmp_score)

    best_pos_index = pos_score.index(max(pos_score))
    row = int(pos[best_pos_index][0])
    col = int(pos[best_pos_index][1])
    weight = int(pos[best_pos_index][2])
    return row,col,weight
     
def score_on_board(board,board_size, user_on_board,ai_on_board):
    ai_score = 0
    index_ai_on_board = []
    for i in range(len(ai_on_board)):
        for j in range(len(ai_on_board)):
            tmp = ai_on_board[i][0]*board_size+ai_on_board[i][1]
            index_ai_on_board.append(tmp)
    for i in range(board_size):
        for j in range(board_size):
            if i*board_size+j in index_ai_on_board:
                if board[i][j] != -1:
                    ai_score+=board[i][j]
    return ai_score

def cal_final_score(board, ai_on_board, user_on_board):

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
        print(board)
        print(Back.RED+'User chess pieces: ',end="")
        print(Style.RESET_ALL,end="")
        print(user)
        print(Back.BLUE+'AI chess pieces: ',end="")
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
        print("End Game")
        print_board(board, board_size, user_on_board, ai_on_board)

    elif board_size == 6:
        board = np.zeros((6,6), dtype=int)
    else:
        print("Your enter wrong board size!")
