# Computes the volume of a 10-dimensional sphere using midpoint integration

import math as math
import numpy as np
from scipy.optimize import curve_fit
from time import process_time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator

# Returns a list of n equidistant points between -bound and bound
def discretization(bound, n):
	return np.linspace(-float(bound) + float(bound) / n, float(bound) + float(bound) / n, n, False)

# Recursively computes an integral of a dim-dimensonal sphere
# with radius sqrt(radius). Pass volume2 = 1 at start.
# n is the number of points used for the midpoint method.
def recursiveIntegral(radius2, volume2, dim, n):
    volume2 *= radius2 * 2 * 2  / (n * n)
    if (dim > 1):
        partIntegral = 0
        for x in discretization(math.sqrt(radius2), n):
            partIntegral += recursiveIntegral(radius2 - x * x, volume2, dim - 1, n)
    else:
        partIntegral = math.sqrt(volume2) * n

    return partIntegral


# Monte Carlo approximation of the volume of a dim-dimensonal sphere
# with radius sqrt(radius)
def montecarlo(dim, radius, N):
    count_in_sphere = 0

    for count_loops in range(N):
        point = np.random.uniform(-1.0, 1.0, dim)
        distance = np.linalg.norm(point)
        if distance < 1.0:
            count_in_sphere += 1

    return np.power(2.0, dim) * (count_in_sphere / N)

# The number of dimensions
numDims = 10

timelist = []
errorlist = []

def calculate(t, error):
    print('time =', t)
    print('error   =', error)
    print('')
    timelist.append(t)
    errorlist.append(error)

def graph(errorlist, timelist, col, title):
    fig, ax = plt.subplots()
    plt.title(title, fontsize = 15)
    ax.plot(errorlist, timelist, color = col)
    ax.plot(errorlist, timelist, 'o', color = col)
    plt.xlabel("Computational time", fontsize = 15)
    plt.ylabel("Integration error", fontsize = 15)
    ax.tick_params(axis='both', which='major', labelsize=14)
    plt.show()

# The number of points in the midpoint method along one dimension

pointlist = [2, 3, 4, 5]
analytical = math.pi**(numDims / 2) / math.factorial(numDims / 2)

iterationlist = [5000, 7500, 10000, 25000, 50000, 75000, 100000]

#for point in pointlist:
#    t = process_time()
#    integral = recursiveIntegral(1, 1, numDims, point)
#    t = process_time() - t
#    error = abs(integral- analytical)
#    calculate(t, error)

# for iteration in iterationlist:
#    f2 = []
#    t = process_time()
#    for i in range(100):
#        f2.append(montecarlo(numDims, 1, iteration))
#    t = (process_time() - t)/100

#      Calculates the standard error
#    f1 = [i**2 for i in f2]
#    sigma2 = sum(f1)/len(f1) - (sum(f2)/len(f2))**2
#    sigma = np.sqrt(sigma2)
#    error = sigma/np.sqrt(len(f1))

#    mean = np.mean(f2)
#    error = abs(mean-analytical)
#    calculate(t, error)

# print(timelist)
# print(errorlist)

# ----------------------- AFTER ALL CALCULATIONS ARE DONE ---------------------------

errorlist1 = [0.9682663823341708, 0.1660809555237166, 0.15717487652157347,
             0.1251325819655884, 0.09438377397356268] 
timelist1 = [0.10271, 0.429084, 3.925878, 23.295996, 111.834063] 

# # Standard error list
# errorlist2 = [0.06701029711439847, 0.05821125526539815, 0.05190892247928054, 0.030427628869670747, 0.02306146214604677, 0.016142397840023845, 0.01551060544035492]
# timelist2 = [0.09260907999999998, 0.14317546, 0.18596374000000002, 0.46080792000000004, 0.9639887399999999, 1.4544988000000003, 1.8853891599999997]

# Asbsolute error list 
errorlist2 = [0.010644039877344635, 0.09994796012265539, 0.010644039877344635, 0.050795960122655526, 0.0026568398773454405, 0.003817373210678543, 0.003885639877344804]
timelist2 = [0.09520641999999999, 0.13635329999999998, 0.17303387999999997, 0.4292304200000001, 0.8845998, 1.3460477999999998, 1.8017523599999998]

              
graph(timelist1,errorlist1, 'b', 'Midpoint method')  
graph(timelist2,errorlist2, 'r', 'Monte Carlo estimation')           
