import numpy as np

def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk)) 
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk)) 
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk)) 
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk)) 
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk)) 
  
prCyan("Hello World, ") 
prYellow("It's") 
prGreen("Geeks") 
prRed("For") 
prGreen("Geeks") 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
print(f"Warning: No active frommets remain. Continue?")

from colorama import init, Fore, Back, Style
init(convert=True)
print(Fore.RED + 'some red text')
print(Style.RESET_ALL,end="") 
#print(Back.GREEN + 'and with a green background') 
#print(Style.DIM + 'and in dim text') 
#print(Style.RESET_ALL) 
#print('back to normal now') 

a = [2,3,5,8,13]
aa = [2,2,3,3,5,5,8,8,8,13,13]
print("/////",aa.index(max(aa)))




b = 1
c = 2
d = [[1,2], [3,4]]
d.remove([1,2])
d.append([6,7])
print(d)
f = [5,4,8,1,3]
print(f.index(max(f)))
print([1,3])

def score_on_board(board,board_size, user_on_board,ai_on_board):
    ai_score = 0
    index_ai_on_board = []
    print(f'{board},{board_size},{user_on_board},{ai_on_board}')
    for i in range(len(ai_on_board)):
        for j in range(len(ai_on_board)):
            tmp = ai_on_board[i][0]*board_size+ai_on_board[i][1]
            index_ai_on_board.append(tmp)
    print(index_ai_on_board)
    for i in range(board_size):
        for j in range(board_size):
            print(i*board_size+j)
            if i*board_size+j in index_ai_on_board:
                print('ggggg')
                if board[i][j] != -1:
                    ai_score+=board[i][j]
    return ai_score




board = np.zeros((4,4), dtype=int)
board[1][1] = 3
board[2][3] = 5
board[2][0] = 2
print(board)
board_size = 4
user_on_board = [[1,1],[2,3]]
ai_on_board = [[2,0]]
ai = [3,5,8,13]

kk = [1,2,3,4,5]
gg = kk.copy()
kk.remove(3)
print(gg)
# print(position(board, ai, board_size, user_on_board, ai_on_board))
#print(score)

'''
def position(board, ai, board_size, user_on_board, ai_on_board):
    row, col = check_corner(board, board_size)
    if row == -2 and col == -2:  #corner都被下完了
        pos_score = []  #[[hand, row, col, user_score, ai_score],[]]
        for hand in range(len(ai)):
            tmp_board = board.copy()
            if ai[hand] < 13:
                for i in range(board_size):
                    for j in range(board_size):
                        if board[i][j] != -1 and board[i][j] == 0:
                            ai_on_board.append([i,j])
                            tmp_board[i][j] = ai[hand]
                            tmp_board = change_board_cond(tmp_board, i, j, ai[hand], board_size)
                            print(tmp_board)
                            user_score, ai_score = score_on_board(tmp_board, board_size, user_on_board, ai_on_board)
                            print("user_score: ",user_score)
                            print("ai_score: ", ai_score)
                            pos_score.append([ai[hand], i, j, user_score, ai_score])
                            ai_on_board.remove([i,j])
                            tmp_board[i][j] = 0
                row, col, weight = find_best_choice(pos_score)
                return row, col, weight
            else:
                for i in range(board_size):
                    for j in range(board_size):
                        if board[i][j] != -1 and board[i][j] == 0:
                            ai_on_board.append([i,j])
                            tmp_board[i][j] = ai[hand]
                            tmp_board = change_board_cond(tmp_board, i, j, ai[hand], board_size)
                            user_score, ai_score = score_on_board(tmp_board, board_size, user_on_board, ai_on_board)
                            pos_score.append([ai[hand], i, j, user_score, ai_score])
                            ai_on_board.remove([i,j])
                            tmp_board[i][j] = 0
                row, col, weight = find_best_choice(pos_score)
                return row, col, weight
    else:  # 要先出小於13但最大的
        max_chess_index = ai.index(max(ai))
        weight = ai[max_chess_index-1]
        return row, col, weight
'''



'''
row = 0
col = 3
surrounding = [[row-1, col-1],[row-1, col],[row-1, col+1],[row, col-1],[row, col+1],[row+1, col-1],[row+1, col],[row+1, col+1]]
print(surrounding)
in_bound = []
for i in range(8):
    if 4>surrounding[i][0] >= 0 and 4>surrounding[i][1]>=0 :
        in_bound.append(surrounding[i])

print(in_bound)
'''