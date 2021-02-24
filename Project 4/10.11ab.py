# Laplace in a rectangular region, solved by Gauss-Seidel and "checkboard"

import matplotlib
import numpy as np
import pylab as plt
from matplotlib import animation
import time

# Linear dimension
L = 10

# The grid spacing is L/n
# The grid is n+1 points along x and y, including boundary points 0 and n
n_list = [10, 20]

# The number of iterations
nsteps_list = [29, 113]
# # The number of iterations
# nsteps_list = range(1,150)
error_max_list = []         # should have the same size as nsteps_list
v_exact = 10

for nsteps, n in zip(nsteps_list, n_list):
    start_time = time.time()        # start time

    # Initialize the grid to 0
    v = np.ones((n+1, n+1)) * 9

    # Set the boundary conditions
    for i in range(1,n):
        v[0,i] = 10
        v[n,i] = 10
        v[i,0] = 10
        v[i,n] = 10

    # print(v)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(v, cmap=None, interpolation='nearest')
    fig.colorbar(im)

    # checker=1: no checkboard, checker=2: checkerboard (note: n should be even)
    checker = 2

    # perform one step of relaxation
    error_list = []
    def relax(n, v, checker):
        for check in range(0,checker):
            for x in range(1,n):
                for y in range(1,n):
                    if (x*(n+1) + y) % checker == check:
                        v[x,y] = (v[x-1][y] + v[x+1][y] + v[x][y-1] + v[x][y+1])*0.25
                        error = abs(v_exact-v[x,y])
                    error_list.append(error)
        error_max_list.append(max(error_list))

    def update(step):
        #print(step)
        global n, v, checker

        # FuncAnimation calls update several times with step=0,
        # so we needs to skip the update with step=0 to get
        # the correct number of steps 
        if step > 0:
            relax(n, v, checker)

        im.set_array(v)
        return im,

    # we generate nsteps+1 frames, because frame=0 is skipped (see above)
    anim = animation.FuncAnimation(fig, update, frames=nsteps+1, interval=200, blit=True, repeat=False)
    plt.show()

    # Calculate execution time
    end_time = time.time()              # end time
    ex_time = end_time-start_time
    print("No. of iterations:", nsteps, "took time:", ex_time)

## Plotting
# new = error_max_list[:len(error_max_list)//2]
# print(len(new))
# plt.figure(1)
# plt.title("Accuracy with different grid sizes")
# plt.xlabel("Number of iterations")
# plt.ylabel("Error")
# plt.plot(nsteps_list, new, "b", label="Grid size "+ str(L/n))
# plt.plot(nsteps_list, [0.1]*len(nsteps_list), 'r', label="1%")
# plt.legend()
# plt.show()
    
    # 10.11a
    # # The center of the matrix represents the desired potential 
    # v_list = v[int(n/2)].tolist()
    # desired = v_list[int(n/2)]
    # print(desired)

    # # Condition to achieve 1% accuracy of the desired potential
    # if desired >= 9.9:
    #     print("1 percent accuracy after:", nsteps, "iterations")
    #     break




