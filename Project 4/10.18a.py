# Random walk solution of Laplace's equation, calculating Greens function

import pylab as plt
import numpy as np
import random as rnd

plt.rcParams.update({'font.size': 14})

# Linear dimension
L = 10

# The grid spacing is L/n
# The grid is n+1 points along x and y, including boundary points 0 and n
n = 10

# Initialize the grid to 0
v = np.zeros((n+1, n+1))
G = []

# Set the boundary conditions
for i in range(1,n):
    v[0,i] = 10
    v[n,i] = 10
    v[i,0] = 5
    v[i,n] = 5

def randomwalk(step, xstart, ystart):
    # Random-walk generator
    x = xstart                                      # initial point in matrix
    y = ystart

    for i in range(step):
        if x == 9:                                  # wanted it to be/it should be 10 but throws IndexError when getting v[x,y]
            return [x+1,y]
            break

        elif y == 9:
            return [x,y+1]
            break

        elif x == 0 or y == 0: 
            return [x,y]
            break
        
        else:
            numb = rnd.randint(0,3)
            if numb == 0:
                x += 1
                y = y
                v[x,y] = v[x+1][y]

            elif numb == 1:
                x -= 1
                y = y
                v[x,y] = v[x-1][y] 

            elif numb == 2: 
                x = x
                y += 1
                v[x,y] = v[x][y+1]

            elif numb == 3:
                x = x
                y -= 1
                v[x,y] = v[x][y-1]


""" ------------------------ PSEUDOCODE 

boundary = [all the boundary elements]
for every point in the matrix:
    for range(#walkers):
        boundarypoint = perform random walk and registrer (return) boundary point 
        for i in len(boundary):
            checklist = [0]*len(boundary)
            if boundary[i] == boundarypoint:
                checklist[i] += 1

"""

boundary = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], 
            [1, 10], [2, 10], [3,10], [4, 10], [5, 10], [6, 10], [7, 10], [8, 10], [9, 10], [10, 10],
            [10, 9], [10, 8], [10, 7], [10, 6], [10, 5], [10, 4], [10, 3], [10, 2], [10, 1], [10, 0],
            [9, 0], [8, 0], [7, 0], [6, 0], [5, 0], [4, 0], [3, 0], [2, 0], [1, 0]]

step = 100

def Greens(walkers):
    global boundary, step, n
    for x in range(1,n):
        for y in range(1,n):
            checklist = [0]*len(boundary)
            for i in range(walkers):
                boundary_point = randomwalk(step, x, y)
                for j in range(len(boundary)):
                    if boundary[j] == boundary_point:
                        checklist[j] += 1
                        
            print("Greens for point "+str((x,y))+" is:", checklist)
                
            
Greens(500)
















# ---------------------- EXCESS CODE THAT MIGHT BE OF USE
 
# # Creating ugly list of boundary points cuz im lazy 
# boundary = []
# for y in range(11):
#     boundary.append([0,y])
#     boundary.append([10,y])

# for x in range(1,10):
#     boundary.append([x,0]) 
#     boundary.append([x,10]) 

# boundary = sorted(boundary, key=lambda x: x[0])

# print(boundary)

# count = [] 
# def counting(G):
#     for value in boundary:
#         c = 0
#         for greens in G:
#             if value == greens:
#                 c += 1
#         count.append(c)
#         print("Det finns "+str(c)+" st av:", value)

# # Test for one point
# x = y = 1
# checklist = [0]*len(boundary)
# for i in range(10):
#     boundary_point = randomwalk(step, x, y)
#     for j in range(len(boundary)):
#         if boundary[j] == boundary_point:
#             checklist[j] += 1

# print("Greens for point "+str((x,y))+" is:", checklist)
