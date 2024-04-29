import numpy as np
num = 0
arr = np.zeros((8,4))
for i in range(len(arr)):
    for j in range(len(arr[0])):
        arr[i][j] = num
        num += 1
print(arr)
X = len(arr)
Y = len(arr[0])
x = y = 0
dx = 0
dy = -1
for i in range(max(X, Y)**2):
    if (-X/2 < x <= X/2) and (-Y/2 < y <= Y/2):
        xcoord = int(x-1+X/2)
        ycoord = int(y-1+Y/2)
        #print(xcoord, ycoord)
        print(arr[xcoord][ycoord])
        # DO STUFF...
    if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
        dx, dy = -dy, dx
    x, y = x+dx, y+dy
