# A 2D self-avoiding random walk with single steps along x or y

import pylab as plt
import numpy as np

# Self-avoiding random walk generator
def randomwalk(n):   
    x, y = [0], [0]
    positions = [(0,0)]                                                             # Stores all coordinates visited by the walk
    stuck = 0
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
            stuck = 1
            steps = i+1
            break  
        steps = n+1
    return x, y, stuck, steps

# Plot function
def plot(n):
    x, y, stuck, steps = randomwalk(n)
    plt.figure()
    plt.plot(x, y, 'bo-', linewidth = 1)
    plt.plot(0, 0, 'go', label = 'Start')
    plt.plot(x[-1], y[-1], 'ro', label = 'End')
    plt.axis('equal')
    plt.legend()
    if stuck:
        plt.title('Self avoiding walk stuck at step ' + str(steps))
    else:
        plt.title('Self avoiding random walk of length ' + str(n))
    plt.show()
    return steps

# Calculate the mean value of the step where the walk gets stuck 
#stuck_list = []
N = range(1, 201)
fraction_list = []
for j in N:
    stuck_counter = 0
    for i in range(100):
        x, y, stuck, steps = randomwalk(j)
        #stuck_list.append(stuck)
        if stuck != 0:                              # If non-successful walk
            stuck_counter += 1
    if stuck_counter != 0:                         
        fraction = (100-stuck_counter)/100            # Number of successful walks/Total walks
        fraction_list.append(fraction)
    else:                                   # Successful walk
        fraction_list.append(1)

plt.figure()
plt.title("Success rate dependence on step")
plt.xlabel("Step N")
plt.ylabel("Fraction of successful walks")
plt.plot(N, fraction_list, 'b')
plt.show()
            
# mean_step_stuck = np.average(stuck_list)
# print(mean_step_stuck)
