# Laplace in a rectangular region

import matplotlib
import numpy as np
import pylab as plt
from matplotlib import animation
import sys

plt.rcParams.update({'font.size': 14})

# Linear dimension
L = 10

# The grid spacing is L/n
# The grid is n+1 points along x and y, including boundary points 0 and n
n = 10

# The number of iterations
# nsteps = 10
nsteps_list = range(1,250)
error_max_list = []         # should have the same size as nsteps_list
v_exact = 10

# Initialize the grid to 0
v = np.ones((n+1, n+1)) * 9
vold = np.zeros((n+1, n+1)) * 9
vnew = np.zeros((n+1, n+1)) * 9

# # 10.10b
# for i in v:
#     i[5] += 4

# Set the boundary conditions
for i in range(1,n):
    v[0,i] = 10
    v[n,i] = 10
    v[i,0] = 10
    v[i,n] = 10


# checker=1: no checkboard, checker=2: checkerboard (note: n should be even)
checker = 2


# perform one step of relaxation
def relax(n, v, checker):
    
    error_list = []
    for check in range(0,checker):
        for x in range(1,n):
            for y in range(1,n):
                if (x*(n+1) + y) % checker == check:
                    v[x,y] = (v[x-1][y] + v[x+1][y] + v[x][y-1] + v[x][y+1])*0.25
                    #vold[x,y] = v[x,y]
                    error = abs(v_exact-v[x,y])
                    error_list.append(error)
        error_max_list.append(max(error_list))


        # Copy back the new values to v
        # Note that you can directly store in v instead of vnew with Gauss-Seidel or checkerboard
        
        #error_list = []
        # for x in range(1,n):
        #     for y in range(1,n):
        #         if (x*(n+1) + y) % checker == check:
        #             v[x,y] = vnew[x,y]

                    # Check 1% accuracy
                    #error = abs(v[x,y]-vold[x,y])

                    # average = (1/4) * (v[x+1, y] + v[x-1, y] + v[x, y+1] + v[x, y-1])
                    # error = abs(average - v[x,y])
                    # print("error:", error)
                    # if error > maximumerror:
                    #     maximumerror = error
                    #     print(maximumerror)
                        

def update(step):
    #print(step)
    global n, v, checker

    # FuncAnimation calls update several times with step=0,
    # so we needs to skip the update with step=0 to get
    # the correct number of steps 
    if step > 0:
        relax(n, v, checker)
        


def main():
    for step in nsteps_list:
        update(step)

main()   
new = error_max_list[:len(error_max_list)//2]
print(len(new))
plt.figure(1)
plt.title("Accuracy with different grid sizes")
plt.xlabel("Number of iterations")
plt.ylabel("Error")
plt.plot(nsteps_list, new, "b", label="Grid size "+ str(L/n))
plt.plot(nsteps_list, [0.1]*len(nsteps_list), 'r', label="1%")
plt.legend()
plt.show()










