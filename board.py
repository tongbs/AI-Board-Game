import numpy as np

def check_chess(hands, chess):
    if chess in hands:
        return True
    else 
        return False

def draw_board(board):
    print(board)

def user_chess(board, user):
    row, col, weight = int(input("Input (row, col, weight): "))
    in_hands = check_chess(user, weight)
    if board[row][col] == 0 and in_hands:
        board[row][col] = weihght
        user = user.remove(weight)
        
    else:
        print("You cannot put chess on that position!")

def ai_chess():

def rest_chess():




if __name__ == "__main__":
    first = int(input("User First? (0/1):"))
    board_size = int(input("Board Size? (4 or 6):"))
    #print(first, board_size)
    if board_size == 4:
        user = [2,3,5,8,13]
        ai = [2,3,5,8,13]
        board = np.zeros((4,4), dtype=int)
        print(board)
        print(f'User chess pieces: {user}')
        print(f'AI chess pieces: {ai}')
        while True:
            if len(user) == 0 or len(ai) == 0:
                break
            else:
                if first == 1:     # user first
                    user_chess(board, user)
     
                else:              # ai first
                    print("AI first")
    elif board_size == 6:
        board = np.zeros((6,6), dtype=int)
    else:
        print("Your enter wrong board size!")
