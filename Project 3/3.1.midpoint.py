# Computes the volume of a 10-dimensional sphere using midpoint integration

import math as math
import numpy as np
from time import process_time
import matplotlib.pyplot as plt

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
            if (dim == 10):
                None
                #print(x)
            partIntegral += recursiveIntegral(radius2 - x * x, volume2, dim - 1, n)
    else:
        partIntegral = math.sqrt(volume2) * n

    return partIntegral

# The number of dimensions
numDims = 10

# The number of points in the midpoint method along one dimension.
# Anything above 6 takes ages to compute.
numPointsPerDim_list = [2, 3, 4, 5, 6]
errors = [0]*len(numPointsPerDim_list)
run_times = [0]*len(numPointsPerDim_list)

analytical = math.pi**(numDims / 2) / math.factorial(numDims / 2)

for i in range(len(numPointsPerDim_list)):
    t = process_time()
    integral = recursiveIntegral(1, 1, numDims, numPointsPerDim_list[i])
    t = process_time() - t
    run_times[i] = t
    errors[i] = abs(integral - analytical)
    print('################# numPointsPerDim =', numPointsPerDim_list[i], '#################')
    # print('time =', t)
    # print('integral   =', integral)
    # print('analytical =', analytical)

plt.figure()
plt.title("Error time dependence - Midpoint")
plt.plot(errors,run_times,  "bo-")
plt.xlabel("Absolute error [m^10]")
plt.ylabel("Time")
plt.show()