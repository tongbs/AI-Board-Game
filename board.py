import numpy as np

def check_chess(hands, chess):   # 檢查要出的牌是否在自已手上
    if chess in hands:
        return "yes"
    else: 
        return "no"

def print_board(board):     # 劃出目前局勢
    print(board)

def print_rest_chess(user, ai):    # 剩餘手牌
    print(f'User chess pieces: {user}')
    print(f'AI chess pieces: {ai}')


def user_chess(board, user, ai, board_size, user_on_board):  # 使用者下棋
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
        print_board(board)
        print_rest_chess(user,ai)
        return board, user, ai, user_on_board    
    else:
        print("You cannot put chess on that position!")
        print("Maybe the card is not in your hand!")

def ai_chess(board, ai, user, board_size, ai_on_board):  # AI 下棋
    row, col, weight = input("AI Input (row, col, weight): ").split()
    row = int(row)
    col = int(col)
    weight = int(weight)
    ai_on_board.append([row,col])
    in_hands = check_chess(ai, weight)
    if board[row][col] == 0 and in_hands == "yes":
        board[row][col] = weight
        ai.remove(weight)
        board = change_board_cond(board, row, col, weight, board_size)
        print_board(board)
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
        print(f'User chess pieces: {user}')
        print(f'AI chess pieces: {ai}')
        # 4x4 Game Start
        while True:
            if len(user) == 0 or len(ai) == 0:
                break
            else:
                if first == 1:     # user first
                    for i in range(5):  # 4x4下5次end game
                        board, user, ai, user_on_board = user_chess(board, user, ai, board_size, user_on_board)
                        board, ai, user, ai_on_board = ai_chess(board, ai, user, board_size, ai_on_board)
                    break
                else:              # ai first
                    print("AI first")
        print("End Game")
        print(user_on_board)
        print(ai_on_board)
        print(board)
    elif board_size == 6:
        board = np.zeros((6,6), dtype=int)
    else:
        print("Your enter wrong board size!")
