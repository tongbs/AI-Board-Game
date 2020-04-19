import numpy as np
a = [1,2,3,4,2,4]

board = np.zeros((4,4), dtype=int)
print(board)

a.remove(1)


b = 1
c = 2
d = [[1,2], [3,4]]
d.append([6,7])
print(d)

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