import matplotlib.pyplot as plt
import numpy as np
import math, pylab

def rw(n):
    # Arrays with the same size as the number of steps
    x = np.zeros(n)
    y = np.zeros(n)

    # Random-walk generator
    for i in range(n):
        n = np.random.randint(0,3)

        if n == 0:
            x[i] = x[i-1] + 1
            y[i] = y[i-1] 

        elif n == 1:
            x[i] = x[i-1] - 1
            y[i] = y[i-1] 

        elif n == 2: 
            x[i] = x[i-1] 
            y[i] = y[i-1] + 1

        elif n == 3:
            x[i] = x[i-1] 
            y[i] = y[i-1] - 1

    # Distances R^2, R
    d = x[-1]**2 + y[-1]**2
    dsqrt = math.sqrt(x[-1]**2 + y[-1]**2)

    return d, dsqrt

def saw(n):   
    x, y = [0], [0]
    positions = [(0,0)]                                                             # Stores all coordinates visited by the walk
    for i in range(n):
        deltas = [(1,0), (0,1), (-1,0), (0,-1)]                                     # Directions to go
        deltas_possible = []                                                        # Possible directions given condition

        for dx, dy in deltas:
            if (x[-1] + dx, y[-1] + dy) not in positions:                           # If we haven't already visited this coordinate
                deltas_possible.append((dx,dy))
        if deltas_possible:                                                         # Checks if there is one or more directions to go
            dx, dy = deltas_possible[np.random.randint(0,len(deltas_possible))]     # Randomly choose one of the possible directions
            positions.append((x[-1] + dx, y[-1] + dy))                              # Save the new coordinate
            x.append(x[-1] + dx)
            y.append(y[-1] + dy)
        else:                                                                       # In that case the walk is stuck
            break 

        # Distances R^2, R
        d = (x[-1]**2 + (y[-1])**2)
        dsqrt = math.sqrt((x[-1])**2 + (y[-1])**2)

    return d, dsqrt



N = range(1, 50)

rmsd_list_saw = []
rmsf_list_saw = []
see_list_saw = []

rmsd_list_rw = []
rmsf_list_rw = []
see_list_rw = []

for step in N:                               # For step N
    d_list_rw = []
    dsqrt_list_rw = []

    d_list_saw = []
    dsqrt_list_saw = []

    for walk in range(1000):                 # Generate 100 different walks per step
        d, dsqrt = saw(step)
        d_list_saw.append(d)
        dsqrt_list_saw.append(dsqrt)

        d1, dsqrt1 = rw(step)
        d_list_rw.append(d1)
        dsqrt_list_rw.append(dsqrt1)

    # Average <R^2>, <R>
    d_mean_saw = np.average(d_list_saw)
    dsqrt_mean_saw = np.average(dsqrt_list_saw)

    d_mean_rw = np.average(d_list_rw)
    dsqrt_mean_rw = np.average(dsqrt_list_rw)
    
    # Variance V = <R^2> - <R>^2
    var_saw = d_mean_saw - dsqrt_mean_saw**2
    var_rw = d_mean_rw - dsqrt_mean_rw**2

    # Root-mean-square fluctuation 
    rmsf_saw = math.sqrt(var_saw * 1000 / 999)
    rmsf_list_saw.append(rmsf_saw)

    rmsf_rw = math.sqrt(var_rw * 1000 / 999)
    rmsf_list_rw.append(rmsf_rw)

# Plot rmsf and see against the step number 
plt.loglog(N, rmsf_list_saw,"b", label = "SARW")
plt.loglog(N, rmsf_list_rw, "r", label = "RW")
#plt.plot(step_list, R2_list,"g", label = r"$\sqrt{⟨R^2⟩}$")
pylab.xlabel("Steps")
pylab.legend()
pylab.title("Root-mean-square distance for random walk (RW) and self-avoiding random walk (SARW)")
pylab.show() 